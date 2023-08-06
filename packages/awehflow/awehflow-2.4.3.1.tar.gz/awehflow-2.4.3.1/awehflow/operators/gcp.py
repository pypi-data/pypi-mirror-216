from typing import Optional
import re

from airflow.version import version as airflow_version
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.exceptions import AirflowException
from airflow.models.baseoperator import BaseOperator
from airflow.models.skipmixin import SkipMixin
from airflow.utils.decorators import apply_defaults

from awehflow.operators.flow import EventEmittingOperator
from awehflow.utils import utc_now
from typing import Iterable
import time

class BigQueryJobOperator(BigQueryExecuteQueryOperator):
    """Exactly like BigQueryOperator, except that it pushes the job_id to xcom"""
        
    template_fields = ('cleanup_query', 'sql', 'destination_dataset_table', 'labels', "query_params", "impersonation_chain")
    def __init__(self,
                 cleanup_query: str = None, # type: ignore
                 *args,
                 **kwargs):
        super(BigQueryJobOperator, self).__init__(*args, **kwargs)
        self.cleanup_query = cleanup_query 
                

    def execute(self, context):
        if self.hook is None:
            hook_kwargs=dict()
            hook_kwargs['gcp_conn_id'] = self.gcp_conn_id
            hook_kwargs['use_legacy_sql'] = self.use_legacy_sql
            hook_kwargs['location'] = self.location

            if int(re.sub('[^0-9]', '', airflow_version)) < 240:
                hook_kwargs['delegate_to'] = self.delegate_to
            else:
                hook_kwargs['impersonation_chain'] = self.impersonation_chain

            self.hook = BigQueryHook(
                **hook_kwargs
            )
            credential_email = self.hook._get_credentials_email()
            self.log.info(f"Created BigQueryHook with account: {credential_email}")

        if self.cleanup_query:
            if self.destination_dataset_table == None:
                raise ValueError('No destination_dataset_table was given, set a destination_dataset_table in the following format: project_id.dataset_id.table_id')
            
            replaced_destination_dataset_table = self.destination_dataset_table.replace(':', '.')
            split_destination_dataset_table = replaced_destination_dataset_table.split(".")

            if len(split_destination_dataset_table) != 3:
                raise ValueError('Please set a destination_dataset_table in the following format: project_id.dataset_id.table_id')
        
            project_id = split_destination_dataset_table[0]
            dataset_id = split_destination_dataset_table[1]
            table_id = split_destination_dataset_table[2]
            
            self.log.info('Checking if table exist: {}.{}.{}'.format(project_id, dataset_id, table_id))
            
            if self.hook.table_exists(project_id=project_id, dataset_id=dataset_id, table_id=table_id):
                self.log.info('Table exists')

                self.log.info('Executing cleanup query: {}'.format(self.cleanup_query))
                cleanup_job_id = self.hook.run_query(sql=self.cleanup_query)
            
                qj = self.hook.get_job(job_id=cleanup_job_id)
                while not qj.done():
                    self.log.info(f'Waiting for job [{cleanup_job_id}] to complete...')
                    time.sleep(1)

                self.log.info('Completed execution of cleanup query')   
            else:
                self.log.info('Table does not exist, cleanup query was not executed') 

        if isinstance(self.sql, str):
            self.sql = [self.sql]
        
        job_id = []
        if isinstance(self.sql, Iterable):
            for s in self.sql:
                self.log.info('Executing: %s', self.sql)
                query_job_id = self.hook.run_query(
                    sql=s,
                    destination_dataset_table=self.destination_dataset_table,
                    write_disposition=self.write_disposition,
                    allow_large_results=self.allow_large_results,
                    flatten_results=self.flatten_results,
                    udf_config=self.udf_config,
                    maximum_billing_tier=self.maximum_billing_tier,
                    maximum_bytes_billed=self.maximum_bytes_billed,
                    create_disposition=self.create_disposition,
                    query_params=self.query_params,
                    labels=self.labels,
                    schema_update_options=self.schema_update_options,
                    priority=self.priority,
                    time_partitioning=self.time_partitioning,
                    api_resource_configs=self.api_resource_configs,
                    cluster_fields=self.cluster_fields,
                    encryption_configuration=self.encryption_configuration,
                )
                job_id.append(query_job_id)
                qj = self.hook.get_job(job_id=query_job_id)
                while not qj.done():
                    self.log.info(f'Waiting for job [{query_job_id}] to complete...')
                    time.sleep(1)
        else:
            raise AirflowException(f"argument 'sql' of type {type(self.sql)} is neither a string nor an iterable")
        
        self.log.info('Completed BigQuery jobs: {}'.format(job_id))
        return job_id


class BigQueryJobTaskMetricOperator(EventEmittingOperator):
    """
    Neeeds help
    """

    @apply_defaults
    def __init__(
            self,
            task_ids: list=[],
            xcom_key: str='return_value',
            bigquery_conn_id: str=None, # type: ignore
            gcp_conn_id: str='google_cloud_default',
            *args, **kwargs):
        """
        :param task_ids: List of task_ids saying which tasks to sink their job_metrics for
        :param xcom_key: XCOM key used to pull the bigquery job id from the specified tasks
        """
        self.task_ids = task_ids
        self.xcom_key = xcom_key
        self.gcp_conn_id = gcp_conn_id
        if bigquery_conn_id:
            self.gcp_conn_id = bigquery_conn_id

        super(BigQueryJobTaskMetricOperator, self).__init__(*args, **kwargs)


    def execute(self, context):
        if int(re.sub('[^0-9]', '', airflow_version)) < 220:
            next_execution_date = context['next_execution_date']
        else:
            next_execution_date = context['data_interval_end']
    
        hook = BigQueryHook(
            gcp_conn_id=self.gcp_conn_id
        )
        credential_email = hook._get_credentials_email()
        self.log.info(f"Created BigQueryHook with account: {credential_email}")

        jobs = hook.get_service().jobs()

        for task_id in self.task_ids:
            job_id = context['task_instance'].xcom_pull(key=self.xcom_key, task_ids=task_id)

            if isinstance(job_id, str):
                job_id = [job_id]

            if job_id:
                for jid in job_id:
                    job = jobs.get(
                        projectId=hook.project_id,
                        jobId=jid
                    ).execute()
                    self.emit_event('task_metric', {
                        'run_id': context['dag_run'].run_id,
                        'dag_id': self.dag.dag_id,
                        'job_name': context['task'].params.get('job_name', ''),
                        'task_id': task_id,
                        'value': job,
                        'created_time': utc_now(),
                        'reference_time': next_execution_date
                    })


class BigQueryShortCircuitOperator(BaseOperator, SkipMixin):
    """
    A "short circuit" operator that can be used a a "pre check" system.  The supplied sql statement should turn a single BOOL column.

    If the BOOL value is TRUE then downstream processors will execute as normal.
    If the BOOL value is FALSE then any downstream processors will be skipped.

    """

    template_fields = ('sql',)
    template_ext = ('.sql',)

    @apply_defaults
    def __init__(
            self,
            sql: str,
            gcp_conn_id: str='google_cloud_default',
            bigquery_conn_id: str=None, # type: ignore
            use_legacy_sql: bool=True,
            *args, **kwargs):
        
        self.sql = sql
        self.gcp_conn_id = gcp_conn_id
        if bigquery_conn_id:
            self.gcp_conn_id = bigquery_conn_id
        self.use_legacy_sql = use_legacy_sql

        super(BigQueryShortCircuitOperator, self).__init__(*args, **kwargs)


    def execute(self, context):
        records = self.db_hook.get_first(self.sql)
        success = records and all([bool(r) for r in records])

        if success:
            return

        self.log.info('Skipping downstream tasks...')

        downstream_tasks = context['task'].get_flat_relatives(upstream=False)
        self.log.debug("Downstream task_ids %s", downstream_tasks)

        if downstream_tasks:
            self.skip(context['dag_run'], context['ti'].execution_date, downstream_tasks)

        self.log.info("Done.")

    @property
    def db_hook(self):
        hook = BigQueryHook(gcp_conn_id=self.gcp_conn_id, use_legacy_sql=self.use_legacy_sql)
        credential_email = hook._get_credentials_email()
        self.log.info(f"Created BigQueryHook with account: {credential_email}")
        return hook


class BigQueryPushFirstResultToXComOperator(BaseOperator):
    template_fields = ('sql',)

    @apply_defaults
    def __init__(
            self,
            sql,
            gcp_conn_id: str='gcp_default',
            bigquery_conn_id: Optional[str] = None,
            use_legacy_sql=True,
            *args, **kwargs):
        """
        :param sql: Source table name that has been materialized (:project_id.:dataset_id.:table_name)
        :param use_legacy_sql: Whether to execute the query in legacy SQL mode or not
        """
        if bigquery_conn_id:
            gcp_conn_id = bigquery_conn_id

        super(BigQueryPushFirstResultToXComOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.use_legacy_sql = use_legacy_sql
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = BigQueryHook(gcp_conn_id=self.gcp_conn_id, use_legacy_sql=self.use_legacy_sql)
        result = hook.get_first(self.sql)
        if not result:
            raise Exception("No materialized date found")
        return result

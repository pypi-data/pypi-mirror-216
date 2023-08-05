from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_result, retry_if_exception_type, \
    RetryError, retry_any
from stratus_api.core.settings import get_settings

CHUNK_FILE_GCS_PATH_FORMAT = get_settings()['service_name'] + "/{job_uuid}/ready.{chunk_number}.csv"
CHUNK_FILE_URI_FORMAT = "gs://{bucket_name}/" + CHUNK_FILE_GCS_PATH_FORMAT
UPLOADED_FILE_GCS_PATH_FORMAT = "{year}/{month}/{day}/{hour}/{segment_uuid}/{job_uuid}/uploaded.{chunk_number}.csv"

DELIVERED_SCHEMA = [
    dict(name='segment_uuid', type='STRING'),
    dict(name='internal_user_id', type='STRING'),
    dict(name='external_user_id', type='STRING'),
    dict(name='id_type', type='STRING'),
    dict(name='operation', type='BOOLEAN'),
    dict(name='integration_job_uuid', type='STRING'),
    dict(name='policy_uuid', type='STRING'),
    dict(name='created_ts', type='TIMESTAMP'),
]

INTEGRATION_LOG_SCHEMA = [
    dict(name='integration_job_uuid', type='STRING'),
    dict(name='segment_uuid', type='STRING'),
    dict(name='file_pattern', type='STRING'),
    dict(name='created_ts', type='TIMESTAMP'),
    dict(name='id_type', type='STRING', mode='REPEATED'),
    dict(name='operation', type='STRING', mode='REPEATED'),
    # dict(name='id_type', type='STRING'),
    # dict(name='operation', type='STRING'),
    dict(name='status', type='STRING'),
]


def log_integration(rows):
    from stratus_api.core.settings import get_settings
    from stratus_api.bigquery import stream_records_to_bigquery
    from stratus_api.bigquery.bigquery import create_table
    from stratus_api.events import publish_event, create_topic

    errors = stream_records_to_bigquery(rows=rows, row_ids=None,
                                        project_id=get_settings()['integration_log_project_id'],
                                        table_name=get_settings()['integration_log_table'],
                                        dataset_name=get_settings()['integration_log_dataset'])
    if errors:
        raise Exception(errors)

    for row in rows:
        publish_event(topic_name=get_settings()['integration_log_topic'], attributes=dict(),
                      event_type='integration', payload=row)


def compose_integration_logs(job_uuid, segments, file_pattern, time, id_types, operations, status):
    rows = []
    for segment in segments:
        rows.append(dict(
            integration_job_uuid=job_uuid,
            segment_uuid=segment['segment_uuid'],
            file_pattern=file_pattern,
            created_ts=time,
            id_type=id_types,
            operation=operations,
            status=status
        ))
    return rows


def get_delivery_error_type(exception):
    from .exceptions import AuthenticationError, ConfigurationError, NotFoundError
    if isinstance(exception, AuthenticationError):
        error_type = 'Authentication Error'
    elif isinstance(exception, ConfigurationError):
        error_type = 'Configuration Error'
    elif isinstance(exception, NotFoundError):
        error_type = 'Not Found Error'
    else:
        error_type = 'Delivery Failure'
    return error_type


# TODO: deprecate when moving to v2
def deliver_data(job_uuid, bucket_name, file_pattern, platform_name, destination, file_headers, segments, id_types,
                 operations, chunk_start_number, start_time=None, **kwargs):
    from stratus_api.integrations import get_integration_settings
    from stratus_api.integrations.chunks import create_file_chunks
    from datetime import datetime
    from stratus_api.integrations.chunks import get_file_checkpoint
    if start_time is None:
        start_time = datetime.utcnow()
    else:
        start_time = datetime.utcfromtimestamp(start_time)
    if '*' in file_pattern and get_file_checkpoint(file_pattern=file_pattern, job_uuid=job_uuid) is None:
        rows = compose_integration_logs(job_uuid, segments, file_pattern, int(start_time.timestamp()), id_types,
                                        operations, 'started')
        log_integration(rows)

    segment_mapping = {i['segment_uuid']: i for i in segments}
    for local_path, delivered_paths, chunk_number, in create_file_chunks(
            bucket_name=bucket_name,
            file_pattern=file_pattern,
            integration_settings=get_integration_settings(),
            file_headers=file_headers,
            job_uuid=job_uuid,
            chunk_number=chunk_start_number
    ):
        chunk_start = datetime.utcnow()
        tb = None
        error_type = None
        try:
            success = distribution_retry_wrapper(
                destination=destination, platform_name=platform_name, segments=segment_mapping, local_path=local_path,
                chunk_number=chunk_number, start_time=start_time, id_types=id_types, operations=operations
            )
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            success = False
            error_type = get_delivery_error_type(exception=e)
            if get_settings()['environment'] not in {'qa', 'prod'}:
                raise e
        if success:
            for segment_uuid, delivered_path in delivered_paths.items():
                load_delivered_data(
                    local_path=delivered_path,
                    job_uuid=job_uuid,
                    chunk_number=chunk_number,
                    segment_uuid=segment_uuid
                )
        log_chunk_delivery(success=success, start=chunk_start, chunk_number=chunk_number, destination=destination,
                           segments=segment_mapping, job_uuid=job_uuid, platform_name=platform_name, traceback=tb,
                           error_type=error_type)

    end_time = datetime.utcnow()

    rows = compose_integration_logs(job_uuid, segments, file_pattern, int(end_time.timestamp()), id_types, operations,
                                    'completed')
    if '*' in file_pattern:
        log_integration(rows)

    return dict(job_uuid=job_uuid, file_pattern=file_pattern, chunk_start_number=chunk_start_number)


def deliver_data_v2(job_uuid, bucket_name, file_pattern, platform_name, destination, file_headers, segments, id_types,
                    operations, chunk_start_number, start_time=None, **kwargs):
    from stratus_api.integrations import get_integration_settings
    from stratus_api.integrations.chunks import create_file_chunks
    from datetime import datetime
    from stratus_api.integrations.chunks import get_file_checkpoint
    if start_time is None:
        start_time = datetime.utcnow()
    else:
        start_time = datetime.utcfromtimestamp(start_time)
    if '*' in file_pattern and get_file_checkpoint(file_pattern=file_pattern, job_uuid=job_uuid) is None:
        rows = compose_integration_logs(job_uuid, segments, file_pattern, int(start_time.timestamp()), id_types,
                                        operations, 'started')
        log_integration(rows)

    segment_mapping = {i['segment_uuid']: i for i in segments}
    for local_path, delivered_paths, chunk_number, in create_file_chunks(
            bucket_name=bucket_name,
            file_pattern=file_pattern,
            integration_settings=get_integration_settings(),
            file_headers=file_headers,
            job_uuid=job_uuid,
            chunk_number=chunk_start_number
    ):
        chunk_start = datetime.utcnow()
        tb = None
        error_type = None
        try:
            success = upload_chunk_file_to_gcs(
                job_uuid=job_uuid, local_path=local_path, chunk_number=chunk_number
            )
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            success = False
            error_type = get_delivery_error_type(exception=e)
            if get_settings()['environment'] not in {'qa', 'prod'}:
                raise e
        if success:
            publish_chunk(job_uuid=job_uuid, bucket_name=bucket_name, file_pattern=file_pattern,
                          platform_name=platform_name, destination=destination, file_headers=file_headers,
                          segments=segments, id_types=id_types, operations=operations, start_time=start_time,
                          chunk_number=chunk_number, )
        #     for segment_uuid, delivered_path in delivered_paths.items():
        #         load_delivered_data(
        #             local_path=delivered_path,
        #             job_uuid=job_uuid,
        #             chunk_number=chunk_number,
        #             segment_uuid=segment_uuid
        #         )
        # log_chunk_delivery(success=success, start=chunk_start, chunk_number=chunk_number, destination=destination,
        #                    segments=segment_mapping, job_uuid=job_uuid, platform_name=platform_name, traceback=tb,
        #                    error_type=error_type)
        log_chunk_creation(success=success, start=chunk_start, chunk_number=chunk_number, segments=segment_mapping,
                           job_uuid=job_uuid, platform_name=platform_name, traceback=tb, error_type=error_type)

    end_time = datetime.utcnow()

    rows = compose_integration_logs(job_uuid, segments, file_pattern, int(end_time.timestamp()), id_types, operations,
                                    'completed')
    if '*' in file_pattern:
        log_integration(rows)

    return dict(job_uuid=job_uuid, file_pattern=file_pattern, chunk_start_number=chunk_start_number)


def log_chunk_delivery(success, start, destination, chunk_number, segments, job_uuid, platform_name, error_type=None,
                       traceback=None):
    from stratus_api.core import log_event
    from datetime import datetime
    payload = dict(
        job_uuid=job_uuid,
        platform_name=platform_name,
        success=success,
        chunk_number=chunk_number,
    )
    if traceback:
        payload['traceback'] = traceback
    log_event(
        level='info',
        start=start,
        end=datetime.utcnow(),
        status='success' if success else 'failure',
        process_type='segment_delivery',
        failure_classification=error_type,
        payload=payload,
        attributes=dict(
            destination_uuid=destination['destination_uuid'],
            platform_uuid=destination['platform_uuid'],
            account_uuid=destination['account_uuid'],
            product_uuid=destination['product_uuid'],
            segment_uuids=list(segments.keys()),
            platform_name=platform_name
        ),
    )


def log_chunk_creation(success, start, chunk_number, segments, job_uuid, platform_name, error_type=None,
                       traceback=None):
    from stratus_api.core import log_event
    from datetime import datetime
    payload = dict(
        job_uuid=job_uuid,
        platform_name=platform_name,
        success=success,
        chunk_number=chunk_number
    )
    if traceback:
        payload['traceback'] = traceback
    log_event(
        level='info',
        start=start,
        end=datetime.utcnow(),
        status='success' if success else 'failure',
        process_type='segment_delivery',
        failure_classification=error_type,
        payload=payload,
        attributes=dict(
            segment_uuids=list(segments.keys()),
            platform_name=platform_name
        ),
    )


def publish_chunk(job_uuid, bucket_name, file_pattern, platform_name, destination, file_headers, segments, id_types,
                  operations, start_time, chunk_number):
    from stratus_api.events import publish_event

    payload = dict(
        job_uuid=job_uuid, bucket_name=bucket_name, file_pattern=file_pattern, platform_name=platform_name,
        destination=destination, file_headers=file_headers, segments=segments, id_types=id_types, operations=operations,
        chunk_number=chunk_number, start_time=start_time.timestamp()
    )
    publish_event(topic_name=get_settings()['integration_distribution_topic'], attributes=dict(),
                  event_type='integration', payload=payload)


def download_file_from_gcs(file_path, bucket_name):
    from stratus_api.storage.gcs import download_from_storage
    return download_from_storage(bucket_name, file_path=file_path)


def subscribe_to_chunk_delivery(body):
    from datetime import datetime
    import os
    chunk_start = datetime.utcnow()
    bucket_name = body.get('bucket_name')
    job_uuid = body.get('job_uuid')
    chunk_number = body.get('chunk_number')
    destination = body.get('destination')
    platform_name = body.get('platform_name')
    segment_mapping = body.get('segments')
    start_time = body.get('start_time')
    id_types = body.get('id_types')
    operations = body.get('operations')
    file_headers = body.get('file_headers')
    file_uri = CHUNK_FILE_URI_FORMAT.format(bucket_name=bucket_name, job_uuid=job_uuid, chunk_number=chunk_number)
    local_path = download_file_from_gcs(file_uri, bucket_name)
    tb = None
    error_type = None

    try:
        success = distribution_retry_wrapper(
            destination=destination, platform_name=platform_name, segments=segment_mapping, local_path=local_path,
            chunk_number=chunk_number, start_time=start_time, id_types=id_types, operations=operations
        )
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        success = False
        error_type = get_delivery_error_type(exception=e)
        if get_settings()['environment'] not in {'qa', 'prod'}:
            raise e
    if success:
        delivered_paths = create_delivered_files(local_path, file_headers, job_uuid, chunk_number)
        for segment_uuid, delivered_path in delivered_paths.items():
            load_delivered_data(
                local_path=delivered_path,
                job_uuid=job_uuid,
                chunk_number=chunk_number,
                segment_uuid=segment_uuid,
            )
    os.remove(local_path)
    log_chunk_delivery(success=success, start=chunk_start, chunk_number=chunk_number, destination=destination,
                       segments=segment_mapping, job_uuid=job_uuid, platform_name=platform_name, traceback=tb,
                       error_type=error_type)
    return job_uuid


def read_csv(local_path):
    import csv
    with open(local_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def create_delivered_files(local_path, file_headers, job_uuid, chunk_number):
    from datetime import datetime
    start = datetime.utcnow()
    delivered_file_paths = dict()
    delivered_pointers = dict()
    delivered_writers = dict()
    from stratus_api.integrations.chunks import add_row_to_delivered_path
    for row in read_csv(local_path):
        delivered_file_paths, delivered_pointers, delivered_writers = add_row_to_delivered_path(
            job_uuid=job_uuid, file_headers=file_headers, row=row, pointers=delivered_pointers,
            writers=delivered_writers, delivered_paths=delivered_file_paths,
            chunk_number=chunk_number, timestamp=start)
    return delivered_file_paths


def distribution_failed(value):
    return value is False


# TODO: deprecate when moving to v2
@retry(stop=stop_after_attempt(3), reraise=True, wait=wait_random_exponential(multiplier=.5, max=5),
       retry=retry_any(retry_if_result(distribution_failed), retry_if_exception_type(Exception)))
def distribution_retry_wrapper(**kwargs):
    from stratus_api.integrations import get_integration_function
    distribute_file = get_integration_function(function_name='distribute_file')
    return distribute_file(**kwargs)


def upload_chunk_file_to_gcs(local_path, job_uuid, chunk_number):
    from stratus_api.storage.gcs import upload_file_to_gcs
    upload_file_to_gcs(
        local_path=local_path,
        file_path=CHUNK_FILE_GCS_PATH_FORMAT.format(
            job_uuid=job_uuid,
            chunk_number=chunk_number,
        )
    )
    return True


def distribution_retry_logger(retry_state):
    pass


def load_delivered_data(job_uuid, local_path, chunk_number, segment_uuid):
    from stratus_api.storage.gcs import upload_file_to_gcs
    from datetime import datetime
    now = datetime.utcnow()
    upload_file_to_gcs(
        local_path=local_path,
        file_path=UPLOADED_FILE_GCS_PATH_FORMAT.format(
            job_uuid=job_uuid,
            chunk_number=chunk_number,
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            segment_uuid=segment_uuid
        )
    )
    return True


def close_delivery(job_uuid):
    return job_uuid, True

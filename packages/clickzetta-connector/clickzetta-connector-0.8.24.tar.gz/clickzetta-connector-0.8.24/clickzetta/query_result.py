import os.path

import io
import string
import base64
from time import sleep

import oss2
import pyarrow as pa
import logging
import enum
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

from qcloud_cos import CosConfig, CosS3Client

logger = logging.getLogger(__name__)
pool = ThreadPoolExecutor(10)


class QueryDataType(enum.Enum):
    Memory = 0
    File = 1


class QueryData(object):
    def __init__(self, data: list, data_type: QueryDataType, file_list: list = None):
        self.data = data
        self.data_type = data_type
        self.file_list = file_list

    def fetch_one(self) -> string:
        return list(self._fetch_one())

    def fetch_many(self, size: int):
        return self._fetch_many(size=size)

    def fetch_all(self):
        return self._fetch_all()

    def _fetch_many(self, size=None):
        if self.data_type == QueryDataType.Memory:
            if len(self.data) <= size:
                return self.data
            else:
                return self.data[0:size]
        elif self.data_type == QueryDataType.File:
            assert self.file_list is not None
            try:
                many_result = []
                for file in self.file_list:
                    while not os.path.exists(file):
                        sleep(0.1)
                    with pa.ipc.RecordBatchStreamReader(file) as reader:
                        for index, row in reader.read_pandas().iterrows():
                            many_result.append(tuple(row.to_list()))
                            if len(many_result) == size:
                                return many_result
            except Exception as e:
                logger.error(f'Error while converting from arrow to result: {e}')
                raise Exception(f'Error while converting from arrow to result: {e}')

    def _fetch_all(self):
        return list(self._fetch_one())

    def _fetch_one(self):
        if self.data_type == QueryDataType.Memory:
            for entry in self.data:
                yield entry
        elif self.data_type == QueryDataType.File:
            assert self.file_list is not None
            try:
                for file in self.file_list:
                    while not os.path.exists(file):
                        sleep(0.1)
                    with pa.ipc.RecordBatchStreamReader(file) as reader:
                        for index, row in reader.read_pandas().iterrows():
                            yield tuple(row.to_list())
            except Exception as e:
                logger.error(f'Error while converting from arrow to result: {e}')
                raise Exception(f'Error while converting from arrow to result: {e}')


class Field(object):
    def __init__(self):
        self.name = None
        self.field_type = None
        self.precision = None
        self.scale = None
        self.length = None
        self.nullable = None

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.field_type = type

    def set_precision(self, precision):
        self.precision = precision

    def set_scale(self, scale):
        self.scale = scale

    def set_length(self, length):
        self.length = length

    def set_nullable(self, nullable):
        self.nullable = nullable


class QueryResult(object):
    def __init__(self, total_msg):
        self.data = None
        self.state = None
        self.total_row_count = 0
        self.total_msg = total_msg
        self.schema = []
        self._parse_result_data()

    def _parse_field(self, field: str, schema_field: Field):
        schema_field.set_name(field['name'])
        if field['type'].__contains__('charTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) != 'False')
            schema_field.set_length(field['type']['charTypeInfo']['length'])
        elif field['type'].__contains__('decimalTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')
            schema_field.set_precision(field['type']['decimalTypeInfo']['precision'])
            schema_field.set_scale(field['type']['decimalTypeInfo']['scale'])
        else:
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')

    def get_result_state(self) -> string:
        return self.total_msg['status']['state']

    def get_arrow_result(self, arrow_buffer):
        try:
            buffer = base64.b64decode(arrow_buffer)
            with pa.ipc.RecordBatchStreamReader(io.BytesIO(buffer)) as reader:
                pandas_result = reader.read_all().to_pandas()
                result = []
                for index, row in pandas_result.iterrows():
                    result.append(tuple(row.tolist()))
                return result

        except Exception as e:
            logger.error(f'Error while converting from arrow to result: {e}')
            raise Exception(f'Error while converting from arrow to result: {e}')

    def get_result_schema(self):
        fields = self.total_msg['resultSet']['metadata']['fields']
        for field in fields:
            schema_field = Field()
            self._parse_field(field, schema_field)
            self.schema.append(schema_field)

    def download_object_files_to_local(self) -> list:
        job_id = self.total_msg['status']['jobId']['id']
        location_info = self.total_msg['resultSet']['location']
        object_storage_file_list = location_info['location']
        object_storage_type = location_info['fileSystem']
        local_file_list = []
        tasks = []
        if object_storage_type == 'OSS':
            id = location_info['stsAkId']
            secret = location_info['stsAkSecret']
            token = location_info['stsToken']
            endpoint = location_info['ossInternalEndpoint'] if not location_info[
                'ossInternalEndpoint'].empty() else location_info['ossEndpoint']
            path_info = object_storage_file_list[0].split('/', 3)
            bucket = path_info[2]
            auth = oss2.Auth(id, secret)
            bucket = oss2.Bucket(auth, endpoint, bucket)
            for file in object_storage_file_list:
                file_info = file.split('/', 3)
                path_info = '/tmp/object_storage_download/' + job_id + '/' + file_info[3]
                try:
                    tasks.append(pool.submit(self._oss_download, file, path_info, bucket, file_info))
                    local_file_list.append(path_info)
                except Exception as e:
                    logger.error(f'Error while downloading object storage file{file} from OSS: {e}')
                    raise Exception(f'Error while downloading object storage file{file} from OSS: {e}')

        elif object_storage_type == 'COS':
            region = location_info['objectStorageRegion']
            id = location_info['stsAkId']
            secret = location_info['stsAkSecret']
            token = location_info['stsToken']
            cos_config = CosConfig(Region=region, SecretId=id, SecretKey=secret, Token=token)
            client = CosS3Client(cos_config)
            for file in object_storage_file_list:
                file_info = file.split('/', 3)
                path_info = '/tmp/object_storage_download/' + job_id + '/' + file_info[3]
                try:
                    if not os.path.exists(os.path.dirname(path_info)):
                        os.makedirs(os.path.dirname(path_info))
                    tasks.append(pool.submit(self._cos_download, file_info, path_info, client, file))
                    local_file_list.append(path_info)
                except Exception as e:
                    logger.error(f'Error while downloading object storage file {file} from COS: {e}')
                    raise Exception(f'Error while downloading object storage file{file} form COS: {e}')
        wait(fs=tasks, return_when=FIRST_COMPLETED, timeout=None)
        return local_file_list

    def _oss_download(self, file, path_info, bucket, file_info):
        try:
            bucket.get_object_to_file(file_info[3], path_info)
        except Exception as e:
            logger.error(f'Error while downloading object storage file{file} from OSS: {e}')
            raise Exception(f'Error while downloading object storage file{file} from OSS: {e}')

    def _cos_download(self, file_info, path_info, client, file):
        try:
            client.get_object(Bucket=file_info[2], Key=file_info[3])['Body'].get_stream_to_file(path_info)
        except Exception as e:
            logger.error(f'Error while downloading object storage file {file} from COS: {e}')
            raise Exception(f'Error while downloading object storage file{file} form COS: {e}')

    def _parse_result_data(self):
        self.state = self.total_msg['status']['state']
        if self.state != 'FAILED':
            if 'data' not in self.total_msg['resultSet']:
                if 'location' in self.total_msg['resultSet']:
                    self.get_result_schema()
                    file_list = self.download_object_files_to_local()
                    self.data = QueryData(data_type=QueryDataType.File, file_list=file_list, data=None)
                else:
                    field = Field()
                    field.set_name('RESULT_MESSAGE')
                    field.set_type("STRING")
                    self.schema.append(field)
                    self.total_row_count = 1
                    result_data = [['OPERATION SUCCEED']]
                    self.data = QueryData(data=result_data, data_type=QueryDataType.Memory)
            else:
                if not (len(self.total_msg['resultSet']['data']['data'])):
                    self.total_row_count = 0
                    fields = self.total_msg['resultSet']['metadata']['fields']
                    for field in fields:
                        schema_field = Field()
                    self._parse_field(field, schema_field)
                    self.schema.append(schema_field)
                    self.data = QueryData(data=[], data_type=QueryDataType.Memory)
                    return
                result_data = self.total_msg['resultSet']['data']['data']
                self.get_result_schema()
                query_result = []
                for row in result_data:
                    partial_result = self.get_arrow_result(row)
                    query_result.extend(entity for entity in partial_result)
                self.data = QueryData(data=query_result, data_type=QueryDataType.Memory)

        else:
            raise Exception('SQL job execute failed.Error:' + self.total_msg['status']['message'].split('\n')[0])

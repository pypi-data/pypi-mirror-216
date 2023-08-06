from rastless import settings
from rastless.core.s3 import S3Bucket
from rastless.db.handler import Database


class Cfg:
    def __init__(self, table_name, bucket_name, dev):
        self.db = Database(table_name)
        self.s3 = S3Bucket(bucket_name)
        self.bucket_name = bucket_name
        self.dev = dev


def create_config(dev: bool = False) -> Cfg:
    table_name = settings.RASTLESS_TABLE_NAME_DEV if dev else settings.RASTLESS_TABLE_NAME
    bucket_name = settings.RASTLESS_BUCKET_NAME_DEV if dev else settings.RASTLESS_BUCKET_NAME

    return Cfg(table_name=table_name, bucket_name=bucket_name, dev=dev)

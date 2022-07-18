import os

import boto3

from aws_env_injector.base import BaseBackend

client = boto3.client("s3", endpoint_url=os.getenv("AWS_S3_ENDPOINT"))


class S3Backend(BaseBackend):
    json_expand_capable = False

    @classmethod
    def fetch_value(cls, config: dict):
        return client.get_object(**config)['Body'].read().decode()

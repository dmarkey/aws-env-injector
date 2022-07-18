import boto3
import os
from aws_env_injector.base import BaseBackend

client = boto3.client("ssm", endpoint_url=os.getenv("AWS_SSM_ENDPOINT"))


class SSMBackend(BaseBackend):

    @classmethod
    def fetch_value(cls, config: dict):
        return client.get_parameter(**config)['Parameter']['Value']

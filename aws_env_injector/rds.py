import os

import boto3

from aws_env_injector.base import BaseBackend

client = boto3.client("rds", endpoint_url=os.getenv("AWS_RDS_ENDPOINT"))


class RDSBackend(BaseBackend):
    json_expand_capable = False

    @classmethod
    def fetch_value(cls, config: dict):
        return client.generate_db_auth_token(**config)


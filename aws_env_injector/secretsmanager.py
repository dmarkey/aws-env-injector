import boto3
import os
from aws_env_injector.base import BaseBackend

client = boto3.client("secretsmanager", endpoint_url=os.getenv("AWS_SECRETSMANAGER_ENDPOINT"))


class SecretsManagerBackend(BaseBackend):

    @classmethod
    def fetch_value(cls, config: dict):
        return client.get_secret_value(**config)['SecretString']


import os
import sys
import json

import boto3

client = boto3.client("secretsmanager", endpoint_url=os.getenv("AWS_SECRETSMANAGER_ENDPOINT"))

PREFIX = "secretsmanager-inject"


class MisconfigurationException(Exception):
    pass


def inject_secrets_into_env():
    output = {}
    for name, value in os.environ.items():
        if value.startswith(PREFIX):
            try:
                trimmed_value = value[len(PREFIX) + 1:]
                pairs = trimmed_value.split(",")
                config = {z.split("=")[0]: z.split("=")[1] for z in pairs}
                version = config.get("version")
                args = {"SecretId": config['name']}
                if version:
                    if version in ("AWSCURRENT", "AWSPREVIOUS"):
                        args['VersionStage'] = version
                    else:
                        args['VersionId'] = version
                try:
                    secret_value = client.get_secret_value(**args)
                    if config.get("mode") == "expand":
                        output.update(json.loads(secret_value['SecretString']))
                    output[name] = secret_value['SecretString']
                except client.exceptions.ResourceNotFoundException:
                    if config.get('fallback'):
                        output[name] = config.get('fallback')
                    else:
                        raise MisconfigurationException(f"Secret {trimmed_value} is not found.")
            except (KeyError, IndexError):
                raise MisconfigurationException(f"Secret {value} is malformed.")
            except json.JSONDecodeError:
                raise MisconfigurationException(f"Secret {value} is not valid JSON and has mode=expand.")
    os.environ.update(output)
    return output


def main():
    inject_secrets_into_env()
    if len(sys.argv) == 1:
        print("Please specify a command to spawn after secrets are loaded.")
        sys.exit(1)
    os.execvp(sys.argv[1], sys.argv[1:])

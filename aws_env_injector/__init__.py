import os
import sys
import json

from aws_env_injector.secretsmanager import SecretsManagerBackend
from aws_env_injector.ssm import SSMBackend
from aws_env_injector.s3 import S3Backend
from aws_env_injector.rds import RDSBackend
from aws_env_injector.base import MisconfigurationException

BACKENDS = {
    "secretsmanager": SecretsManagerBackend,
    "ssm": SSMBackend,
    "s3": S3Backend,
    "rds": RDSBackend,
}


PREFIX = "aws-env-inject"


def inject_into_env(environment: dict):
    output = {}
    for name, value in os.environ.items():
        if value.startswith(PREFIX):
            try:
                trimmed_value = value[len(PREFIX) + 1:]
                pairs = trimmed_value.split(",")
                config = {z.split("=")[0]: z.split("=")[1] for z in pairs}
                backend = config.pop("type")
                backend_class = BACKENDS.get(backend, None)
                if not backend_class:
                    raise MisconfigurationException(f"Backend {backend} not supported")
                json_expand = config.pop("json_expand", "").lower() == "true"
                if json_expand and not backend_class.json_expand_capable:
                    raise MisconfigurationException(f"Backend {backend} not json_expand capable")
                secret_value = backend_class.fetch_value(config)
                output[name] = secret_value
                if json_expand:
                    output.update(json.loads(secret_value))

            except (KeyError, IndexError):
                raise MisconfigurationException(f"Configuration {value} is malformed.")
            except json.JSONDecodeError:
                raise MisconfigurationException(f"Configuration {value} is not valid JSON and has json_expand=true.")
    environment.update(output)
    return output


def main():
    try:
        cmd = sys.argv[sys.argv.index("--") + 1:]
    except (IndexError, ValueError):
        print("Please specify a command to spawn after values are loaded. `aws-env-injector -- bash` for example")
        sys.exit(1)
    inject_into_env(os.environ)
    os.execvp(cmd[0], cmd[0:])

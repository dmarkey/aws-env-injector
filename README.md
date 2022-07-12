# sm-env-injector
A small utility and library to replace environment variables with Secrets from AWS secrets manager

## Introduction

This utility scans the environment variables in the system and detects any value with the prefix "secretsmanager:". It will then fetch the secret from AWS secrets manager, replacing that environment variable with the one out of secrets manager. For example:

```
>> export SAMPLESECRET="secretsmanager-inject:name=foo,version=AWSCURRENT"
>> sm-env-injector env | grep SAMPLESECRET
SAMPLESECRET=string
```
You see here that the secret `string` has been has been fetched from Secrets Manager, the argument to sm-env-injector is the executable that you want to spawn after the secrets are fetched so they can be used.

It can also be used as a python library if being used in the context of a python program (django, flask app etc)

```
In [1]: import os

In [2]: import sm_env_injector

In [3]: sm_env_injector.inject_secrets_into_env()
Out[3]: {'SECRET3': 'string', 'SAMPLESECRET': 'string'}

In [4]: os.environ['SAMPLESECRET']
Out[4]: 'string'

```

# Installation

```
pip install sm_env_injector
```

# Configuration

It will scan all envirnment variables, for the `secretsmanager:` prefix. Aftet the prefix you can specify the following comma seperated values:

* name - required
* version - optional, either stage name, AWSCURRENT, AWSPREVIOUS or a full UUID version string.
* fallback - if the secret is *missing* then fallback to this version (may be useful in tests for example)

# Examples

`export SAMPLESECRET="secretsmanager-inject:name=foo,version=AWSCURRENT"`

`export SAMPLESECRET="secretsmanager-inject:name=foo,version=1F4CBFF8-878F-4046-8E89-D9344F85AF69"`

`export SAMPLESECRET="secretsmanager-inject:name=foo,version=1F4CBFF8-878F-4046-8E89-D9344F85AF69,fallback=myfallbackvalue"`

# Notes

Only `SecretString` type secrets are supported.

# aws-sm-env-injector
A small utility and library to replace environment variables with Secrets from AWS secrets manager

## Introduction

This utility scans the environment variables in the system and detects any value with the prefix "secretsmanager:". It will then fetch the secret from AWS secrets manager, replacing that environment variable with the one out of secrets manager. For example:

```
>> export SAMPLESECRET="aws-secretsmanager-inject:name=foo,version=AWSCURRENT"
>> aws-sm-env-injector env | grep SAMPLESECRET
SAMPLESECRET=string
```
You see here that the secret `string` has been has been fetched from Secrets Manager, the argument to sm-env-injector is the executable that you want to spawn after the secrets are fetched so they can be used.

It can also be used as a python library if being used in the context of a python program (django, flask app etc)

```
In [1]: import os

In [2]: import aws_sm_env_injector

In [3]: aws_sm_env_injector.inject_secrets_into_env()
Out[3]: {'SECRET3': 'string', 'SAMPLESECRET': 'string'}

In [4]: os.environ['SAMPLESECRET']
Out[4]: 'string'

```

# Installation

```
pip install aws_sm_env_injector
```

# Configuration

It will scan all envirnment variables, for the `secretsmanager:` prefix. Aftet the prefix you can specify the following comma seperated values:

* name - required
* version - optional, either stage name, AWSCURRENT, AWSPREVIOUS or a full UUID version string.
* fallback - if the secret is *missing* then fallback to this version (may be useful in tests for example)
* expanded - As well as fetching the secret, if the secret is Json (key value pairs), expand them and set Environment variables accordingly. Set to `true` if you want this behaviour.
# Examples

With a version that's a stage
`export SAMPLESECRET="secretsmanager-inject:name=foo,version=AWSCURRENT"`

With a version that's a UUID
`export SAMPLESECRET="secretsmanager-inject:name=foo,version=1F4CBFF8-878F-4046-8E89-D9344F85AF69"`

With a fallback value
`export SAMPLESECRET="secretsmanager-inject:name=foo,version=1F4CBFF8-878F-4046-8E89-D9344F85AF69,fallback=myfallbackvalue"`

With an expanded key, pair secret
```
>> aws secretsmanager create-secret --name=expanded-example --secret-string='{"EXPANDEDSECRET1":"secret1", "EXPANDEDSECRET2":"secret2"}'
>> export EXPANDEDSECRET="aws-secretsmanager-inject:name=expanded-example,expand=true"
>> aws-sm-env-injector env | grep EXPANDED
EXPANDEDSECRET={"EXPANDEDSECRET1":"secret1", "EXPANDEDSECRET2":"secret2"}
EXPANDEDSECRET1=secret1
EXPANDEDSECRET2=secret2
```
# Notes

Only `SecretString` type secrets are supported in both plain and keypair modes.

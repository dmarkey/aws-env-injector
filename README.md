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


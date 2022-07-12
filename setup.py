from setuptools import setup

setup(
    name='aws_sm_env_injector',
    packages=['aws_sm_env_injector'],
    url='https://github.com/dmarkey/aws-sm-env-injector',
    python_requires='>3.6.0',
    version='0.0.1',
    license='MIT',
    author='dmarkey',
    author_email='david@dmarkey.com',
    description='A small tool to inject secrets from AWS secrets manager into environment variables',
    entry_points={
        'console_scripts': ['aws-sm-env-injector=aws_sm_env_injector:main'],
    },
    install_requires=[
        'boto3'
    ],
)


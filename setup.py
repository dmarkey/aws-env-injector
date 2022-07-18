from setuptools import setup

setup(
    name='aws_env_injector',
    packages=['aws_env_injector'],
    url='https://github.com/dmarkey/aws-env-injector',
    python_requires='>3.6.0',
    version='0.0.1',
    license='MIT',
    author='dmarkey',
    author_email='david@dmarkey.com',
    description='A small tool to inject secrets from AWS services into environment variables',
    entry_points={
        'console_scripts': ['aws-env-injector=aws_env_injector:main'],
    },
    install_requires=[
        'boto3'
    ],
)


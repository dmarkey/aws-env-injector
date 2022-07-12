from setuptools import setup

setup(
    name='sm_env_injector',
    packages=['sm_env_injector'],
    url='https://github.com/dmarkey/sm_env_injector',
    python_requires='>3.6.0',
    version='0.0.1',
    license='MIT',
    author='dmarkey',
    author_email='david@dmarkey.com',
    description='A small tool to inject secrets from AWS secrets manager into environment variables',
    entry_points={
        'console_scripts': ['sm-env-injector=sm_env_injector:main'],
    },
    install_requires=[
        'boto3'
    ],
)


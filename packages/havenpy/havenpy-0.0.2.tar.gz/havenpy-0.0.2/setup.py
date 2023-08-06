from setuptools import setup, find_packages

setup(
    name='havenpy',
    version='0.0.2',
    author='Haven Technologies Inc.',
    author_email='hello@havenllm.com',
    description='Haven SDK',
    packages=find_packages(),
    install_requires=[
        'grpcio==1.54.2',
    ],
)

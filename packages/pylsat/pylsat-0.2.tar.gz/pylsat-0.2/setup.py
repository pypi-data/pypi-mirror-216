from setuptools import setup, find_packages

setup(
    name='pylsat',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'fastapi', 
        'starlette', 
        'pymacaroons', 
        'datetime', 
        'hashlib', 
        'uuid'
    ],
    url='https://github.com/plebos/pylsat',
    license='MIT',
    author='Tal Shmueli',
    author_email='tal@shmueli.org',
    description='A Python library for validating Lightning Service Authentication Tokens (LSAT) in a FastAPI application.'
)

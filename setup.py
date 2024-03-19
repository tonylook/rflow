from setuptools import setup, find_packages
import json

default_version = '1.0.0'

try:
    with open('version.info', 'r') as version_file:
        version_info = json.load(version_file)
        current_version = version_info['currentVersion']
except (FileNotFoundError, KeyError):
    current_version = default_version

setup(
    name='rflow',
    version=current_version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.7',
        'GitPython==3.1.42',
        'semantic-version==2.10.0',
        'gitdb==4.0.11',
        'smmap==5.0.1'
    ],
    entry_points={
        'console_scripts': [
            'rflow=rflow.cli:cli',
        ],
    },
)

from setuptools import setup, find_packages

setup(
    name='rflow',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.7',
        'GitPython==3.1.40',
        'semantic-version==2.10.0',
    ],
    entry_points={
        'console_scripts': [
            'rflow=rflow.cli:cli',
        ],
    },
)

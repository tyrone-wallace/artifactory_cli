from setuptools import setup, find_packages

setup(
    name='artifactory-cli',
    version='0.0.1',
    description='A CLI for managing JFrog Artifactory via its API',
    author='Tyrone Wallace',
    packages=find_packages(include=["artifactory_cli", "artifactory_cli.*"]),
    install_requires=[
        "requests",
        "InquirerPy"
    ],
    entry_points={
        'console_scripts': [
            'artifactory-cli=artifactory_cli.main:main',
        ],
    },
)

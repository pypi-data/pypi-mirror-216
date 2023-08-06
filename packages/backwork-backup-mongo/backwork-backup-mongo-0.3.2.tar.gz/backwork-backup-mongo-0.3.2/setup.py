"""Add support for MongoDB backups on backwork.
"""

from os import path

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md")) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="backwork-backup-mongo",
    version="0.3.2",
    description="Backwork plug-in for MongoDB backups.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/backwork-backup-mongo",
    author="Luiz Aoqui",
    author_email="laoqui@ca.ibm.com",
    license="Apache 2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Database",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=["backwork"],
    entry_points={
        "backwork.backups": ["mongo=mongo:MongoBackup"],
        "backwork.restores": ["mongo=mongo:MongoRestore"],
    },
)

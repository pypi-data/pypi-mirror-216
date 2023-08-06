"""File backup module for Backwork
"""

from os import path

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md")) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="backwork-backup-files",
    version="0.3.1",
    description="Backwork plug-in for file backups.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/backwork-backup-files",
    author="Leons Petrazickis",
    author_email="leonsp@ca.ibm.com",
    license="Apache 2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=["backwork"],
    entry_points={
        "backwork.backups": ["files=files:FilesBackup"],
        "backwork.restores": ["files=files:FilesRestore"],
    },
)

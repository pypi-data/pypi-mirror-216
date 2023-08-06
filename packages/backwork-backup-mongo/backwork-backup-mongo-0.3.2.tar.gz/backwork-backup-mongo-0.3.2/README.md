# backwork-backup-mongo [![Build Status](https://travis-ci.org/IBM/backwork-backup-mongo.svg?branch=master)](https://travis-ci.org/IBM/backwork-backup-mongo) [![PyPI version](https://badge.fury.io/py/backwork-backup-mongo.svg)](https://badge.fury.io/py/backwork-backup-mongo)
Adds support for MongoDB backups to [`backwork`](https://github.com/IBM/backwork).

## Requirements
This plug-in is build on top of [`mongodump`](https://docs.mongodb.com/manual/reference/program/mongodump/#bin.mongodump),
so you will need to have [`mongo-tools`](https://github.com/mongodb/mongo-tools)
installed.

If you already have the `mongod` server or `mongo` client installed then you
should have `mongodump`. If not, you can install them using the
[official packages](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#packages)
or build from [source](https://github.com/mongodb/mongo-tools).

## Installing
You can use `pip` to install this plug-in:
```sh
$ pip install backwork-backup-mongo
```

## Using
After installing the plug-in you will be able to use the `backup mongo` and `restore mongo` commands
on `backwork`.


#### `backwork backup mongo`
```sh
$ backwork backup mongo --help
usage: backwork backup mongo [-h]

Backup a MongoDB database. It uses `mongodump` so it's required to have it
installed and added to the system's PATH. You can use any of the arguments
supported by `mongodump`. Use `mongodump --help` for more information.

optional arguments:
  -h, --help  show this help message and exit
```

You can pass any option that you would normally use on `mongodump`, e.g.:

```sh
$ backwork backup mongo --user=user --password=pass --host=mongo
```

The only exception is `-h` which is reserved for the help/usage message, so the
host needs to be passed as `--host`.



#### `backwork restore mongo`

```sh
$ backwork restore mongo --help
usage: backwork restore mongo [-h]

Restore a MongoDB database. It uses `mongorestore` so it's required to have it
installed and added to the system's PATH. You can use any of the arguments
supported by `mongorestore`. Use `mongorestore --help` for more information.

optional arguments:
  -h, --help  show this help message and exit
```

You can pass any option that you would normally use on `mongorestore`, e.g.:

```sh
$ backwork restore mongo --user=user --password=pass --host=mongo dumps
```

The only exception is `-h` which is reserved for the help/usage message, so the
host needs to be passed as `--host`.

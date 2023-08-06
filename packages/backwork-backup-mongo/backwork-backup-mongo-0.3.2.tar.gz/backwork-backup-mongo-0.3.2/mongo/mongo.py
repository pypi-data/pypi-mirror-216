"""Add support for MongoDB backups on backwork.
"""

import argparse
import time
import logging
import os
import subprocess
import urllib
from urllib.parse import urlparse, quote

LOG = logging.getLogger(__name__)


class MongoBackup(object):
    """Backup a MongoDB database.

    It uses `mongodump` so it's required to have it installed and added to the
    system's PATH. You can use any of the arguments supported by `mongodump`.
    Use `mongodump --help` for more information.
    """
    command = "mongo"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `mongo` subparser for the `backup` command."""
        subparsers.add_parser(cls.command, description=cls.__doc__)

    def backup(self):
        """Backup a MongoDB database.

        If no output argument is specified (-o, --output, --archive) it will
        run `mongodump` with `--archive` and `--gzip` and store it into
        `./dumps` with a timestamped name.
        """
        LOG.info("starting mongo backup...")

        # parse special characters in URI passwords and usernames
        mongo_uri = [uri for uri in self.extra if "--uri=" in uri]
        if(len(mongo_uri) > 0):
            original_mongo_uri = mongo_uri[0].replace("--uri=", "")
            original_mongo_uri_parsed = urlparse(original_mongo_uri)
            mongo_uri_password = original_mongo_uri_parsed.password 
            mongo_uri_username = original_mongo_uri_parsed.username
            if(mongo_uri_password and mongo_uri_username):
                mongo_uri_password_decoded = urllib.parse.unquote(mongo_uri_password)
                mongo_uri_username_decoded = urllib.parse.unquote(mongo_uri_username)
                if(mongo_uri_password_decoded == mongo_uri_password and mongo_uri_username_decoded == mongo_uri_username):
                    mongo_uri_password_encoded = urllib.parse.quote(mongo_uri_password)
                    mongo_uri_username_encoded = urllib.parse.quote(mongo_uri_username)
                    original_mongo_uri = original_mongo_uri.replace(mongo_uri_password, mongo_uri_password_encoded)
                    original_mongo_uri = original_mongo_uri.replace(mongo_uri_username, mongo_uri_username_encoded)
            self.extra = [original_mongo_uri]

        # parse extra arguments to check output options
        output_config_parser = argparse.ArgumentParser()
        output_config_parser.add_argument("-o", "--output")
        output_config_parser.add_argument("--archive")
        output_args, _ = output_config_parser.parse_known_args(self.extra)

        if not any([output_args.output, output_args.archive]):
            # generate sensible defaults for output file: timestamped gziped archived file
            filename = "mongo_backup_{}.archive.gz".format(
                time.strftime("%Y%m%d-%H%M%S"))
            path = os.path.join(os.getcwd(), "dumps", filename)
            dirname = os.path.dirname(path)

            if not os.path.exists(dirname):
                os.mkdir(dirname)

            self.extra.append("--archive={}".format(path))
            if "--gzip" not in self.extra:
                self.extra.append("--gzip")

            LOG.info("saving file to %s", path)

        cmd = ["mongodump"] + self.extra

        try:
            self.result = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT)
            LOG.info('\n\n'+self.result.decode('utf-8'))
            LOG.info("backup complete")

        except subprocess.CalledProcessError as error:
            self.result = error.output
            LOG.error("failed to back up mongo database")
            LOG.error("return code was %s", error.returncode)
            LOG.error('\n\n'+self.result.decode('utf-8'))
            LOG.error("backup process failed")
            raise error


class MongoRestore(object):
    """Restore a MongoDB database.

    Restore a MongoDB database. It uses `mongorestore` so it's required to have it
    installed and added to the system's PATH. You can use any of the arguments
    supported by `mongorestore`. Use `mongorestore --help` for more information.
    """
    command = "mongo"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.result = ""

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `mongo` subparser for the `backup` command."""
        subparsers.add_parser(cls.command, description=cls.__doc__)

    def restore(self):
        """Restore a MongoDB database.

        """
        LOG.info("starting mongo restore...")

        cmd = ["mongorestore"] + self.extra

        try:
            self.result = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT)
            LOG.info('\n\n'+self.result.decode('utf-8'))
            LOG.info("restore complete")

        except subprocess.CalledProcessError as error:
            self.result = error.output
            LOG.error("failed to restore mongo database")
            LOG.error("return code was %s", error.returncode)
            LOG.error('\n\n'+self.result.decode('utf-8'))
            LOG.error("restore process failed")
            raise error

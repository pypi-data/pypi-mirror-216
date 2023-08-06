"""Add support for MySQL backups
"""

import logging
import subprocess
import sys

LOG = logging.getLogger(__name__)


class MySQLBackupException(Exception):  # pylint: disable=unused-variable
    """Raise for errors"""
    pass


class MySQLBackup(object):
    """Backup a MySQL database.

    It uses `mysqldump` so it's required to have it installed and added to the
    system's PATH. You can use any of the arguments supported by `mysqldump`.
    Use `mysqldump -h` for more information.
    """
    command = "mysql"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `mysql` subparser for the `backup` command."""
        mysql_parser = subparsers.add_parser(
            cls.command, description=cls.__doc__)

        mysql_parser.add_argument("--gzip", action="store_true", required=False,
                                  help="compress output file (requires gzip to be installed)")

        mysql_parser.add_argument("-o", "--output", required=False,
                                  help="output file path")

    def backup(self):
        """Backup a MySQL database."""
        output_file = sys.stdout
        gzip_out = None
        mysqldump_out = None

        if self.args.output:
            LOG.info("starting mysql backup...")
            output_file = open(self.args.output, 'w')
        if self.args.gzip:
            mysqldump_out = subprocess.PIPE
            gzip_out = output_file

        else:
            mysqldump_out = output_file

        try:
            mysqldump_cmd = ["mysqldump"] + self.extra
            mysqldump_process = subprocess.Popen(
                mysqldump_cmd, stdout=mysqldump_out)

            if self.args.gzip:
                gzip_process = subprocess.Popen(["gzip"], stdin=mysqldump_process.stdout,
                                                stdout=gzip_out)
                mysqldump_process.stdout.close()
                if gzip_process.wait() != 0:
                    raise MySQLBackupException("gzip failed for MySQL")

            if mysqldump_process.wait() != 0:
                raise MySQLBackupException("mysqldump failed for MySQL")

            if self.args.output:
                LOG.info("mysql backup complete")

        except Exception as error:
            LOG.error("Failed to backup MySQL database")
            raise error

        finally:
            if output_file and not output_file.closed:
                output_file.close()


class MySQLRestore(object):
    """Restores MySQL databases.

    It uses `mysql` so it's required to have it installed and added to the
    system's PATH.
    """
    command = "mysql"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `mysql` subparser for the `backup` command."""
        mysql_parser = subparsers.add_parser(
            cls.command, description=cls.__doc__)

        mysql_parser.add_argument("--gzip", action="store_true", required=False,
                                  help="decompress backup file before restoring (requires gzip to be installed)")

        mysql_parser.add_argument("-i", "--input", required=False,
                                  help="input file (backup) path")

    def restore(self):
        """Restore a MySQL database."""

        try:
            mysqlrestore_cmd = [
                *(
                    ["gunzip", "-c", str(self.args.input)]
                    if self.args.gzip
                    else ["cat", self.args.input]
                ),
                *["|", "mysql"],
                *self.extra
            ]
            print(' '.join(mysqlrestore_cmd))
            subprocess.Popen(
                ' '.join(mysqlrestore_cmd), shell=True).wait()
            LOG.info("Successfully restored MySQL database")

        except Exception as error:
            LOG.error("Failed to restore MySQL database")
            raise error

"""Add support for PostgreSQL backups
"""

import logging
import os
import subprocess
import sys

LOG = logging.getLogger(__name__)


class PostgreSQLBackupException(Exception):  # pylint: disable=unused-variable
    """Raise for errors"""

    pass


class PostgreSQLBackup(object):
    """Backup a PostgreSQL database.

    It uses `pg_dump` so it's required to have it installed and added to the
    system's PATH. You can use any of the arguments supported by `pg_dump`.
    Use `pg_dump --help` for more information.
    """

    command = "postgresql"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, subparsers):
        """Create the `postgresql` subparser for the `backup` command."""
        pg_parser = subparsers.add_parser(cls.command, description=cls.__doc__)

        pg_parser.add_argument(
            "--gzip",
            action="store_true",
            required=False,
            help="compress output file (requires gzip to be installed)",
        )

        pg_parser.add_argument(
            "-o", "--output", required=False, help="output file path"
        )

        pg_parser.add_argument(
            "-P", "--password", required=True, help="PostgreSQL connection password"
        )

    def backup(self):
        """Backup a PostgreSQL database."""
        output_file = sys.stdout
        gzip_out = None
        pg_dump_out = None

        if self.args.output:
            LOG.info("starting postgresql backup...")
            output_file = open(self.args.output, "w")

        if self.args.gzip:
            pg_dump_out = subprocess.PIPE
            gzip_out = output_file
        else:
            pg_dump_out = output_file

        try:
            os.environ["PGPASSWORD"] = self.args.password
            pg_dump_cmd = ["pg_dump"] + self.extra
            pg_dump_process = subprocess.Popen(pg_dump_cmd, stdout=pg_dump_out)

            if self.args.gzip:
                gzip_process = subprocess.Popen(
                    ["gzip"], stdin=pg_dump_process.stdout, stdout=gzip_out
                )
                pg_dump_process.stdout.close()
                if gzip_process.wait() != 0:
                    raise PostgreSQLBackupException("gzip failed for Postgres")

            if pg_dump_process.wait() != 0:
                raise PostgreSQLBackupException("pg_dump failed for Postgres")

            if self.args.output:
                LOG.info("PostgreSQL backup complete")

        except Exception as error:
            LOG.error("Failed to backup PostgreSQL database")
            raise error

        finally:
            if output_file and not output_file.closed:
                output_file.close()

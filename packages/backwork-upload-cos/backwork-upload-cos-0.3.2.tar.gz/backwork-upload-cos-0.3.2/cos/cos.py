"""Upload file to IBM Cloud Object Storage."""
import logging
import ibm_boto3
from ibm_botocore.client import Config, ClientError

import os
import ntpath
import json

LOG = logging.getLogger(__name__)


class CloudObjectStorageUpload(object):  # pylint: disable=unused-variable
    """Upload a file to Cloud Object Storage."""

    command = "cos"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.session = ibm_boto3.session.Session(
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
        )
        self.client = self.session.client("s3", endpoint_url=args.endpoint_url)
        self.s3 = self.session.resource("s3", endpoint_url=args.endpoint_url)
        self.cos = ibm_boto3.resource(
            "s3",
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
            endpoint_url=args.endpoint_url,
        )

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @classmethod
    def parse_args(cls, subparsers):
        """Add Cloud Object Storage arguments to command line parser."""
        cos_oo_parser = subparsers.add_parser("cos", description=cls.__doc__)

        cos_oo_parser.add_argument(
            "-e", "--endpoint-url", help="endpoint URL of the S3 storage"
        )
        cos_oo_parser.add_argument(
            "-s", "--instance-id", help="service instance id")
        cos_oo_parser.add_argument(
            "-u", "--access-key", help="acccess key id of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "-p", "--secret-key", help="secret access key of HMAC credentials")
        cos_oo_parser.add_argument(
            "local_path",
            nargs="?",
            default=None,
            help="path in the local file system of the file to be uploaded",
        )
        cos_oo_parser.add_argument("bucket", help="target s3 bucket")
        cos_oo_parser.add_argument(
            "remote_path",
            help="""path on Cloud Object Storage where the file
                                  will be stored""",
        )

    def upload(self):
        """Upload a file from `local_path` to `remote_path` on ObjectStorage."""
        LOG.info("uploading '%s' to Cloud Object Storage", self.args.local_path)
        LOG.info(
            "target path: 's3://%s/%s' at '%s'",
            self.args.bucket,
            self.args.remote_path,
            self.args.endpoint_url,
        )

        bucket = self.s3.Bucket(self.args.bucket)

        # make sure target bucket exists
        if bucket.name not in [
            b["Name"] for b in self.client.list_buckets()["Buckets"]
        ]:
            LOG.info("bucket '%s' not found. creating it...", self.args.bucket)
            bucket.create()

        if os.path.isfile(self.args.local_path):
            bucket.upload_file(
                os.path.abspath(self.args.local_path),
                "{}/{}".format(
                    self.args.remote_path, self.path_leaf(self.args.local_path)
                ),
            )
            LOG.info("upload complete")
        else:
            LOG.info("file does not exist")


class CloudObjectStorageShow(object):  # pylint: disable=unused-variable
    """List available backups in Cloud Object Storage."""

    command = "cos"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.session = ibm_boto3.session.Session(
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
        )
        self.client = self.session.client("s3", endpoint_url=args.endpoint_url)
        self.s3 = self.session.resource("s3", endpoint_url=args.endpoint_url)
        self.cos = ibm_boto3.resource(
            "s3",
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
            endpoint_url=args.endpoint_url,
        )

    @classmethod
    def parse_args(cls, subparsers):
        """Add Cloud Object Storage arguments to command line parser."""
        cos_oo_parser = subparsers.add_parser("cos", description=cls.__doc__)

        cos_oo_parser.add_argument(
            "-e", "--endpoint-url", help="endpoint URL of the S3 storage"
        )
        cos_oo_parser.add_argument(
            "-s", "--instance-id", help="service instance id")
        cos_oo_parser.add_argument(
            "-u", "--access-key", help="acccess key id of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "-p", "--secret-key", help="secret access key of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "-l", "--limit", help="max number of results to return")
        cos_oo_parser.add_argument(
            "--sort-last-modified", default=True, action="store_const", const=sum, help="if passed, sorts results from most to least recent"
        )

        cos_oo_parser.add_argument("bucket", help="target s3 bucket")

        cos_oo_parser.add_argument(
            "path",
            help="""Path/prefix to the look for backups in""",
        )

    def show(self):
        """Show backups that are available on a given remote path / prefix on Object Storage."""

        backup_objects = self.client.list_objects(
            Bucket=self.args.bucket,
            Prefix=self.args.path
        )["Contents"]

        if self.args.sort_last_modified:
            def get_backup_name_from_key(obj_key):
                # remove prefix/path from key
                backup_name = obj_key.split(self.args.path, 1)[-1]
                # # remove leading/trailing /
                backup_name = obj_key.strip('/')
                return backup_name

            def get_last_modified(obj):
                return int(
                    obj['LastModified'].strftime('%s'))

            backups = [
                {
                    'name': get_backup_name_from_key(backup['Key']),
                    'last_modified': str(backup['LastModified']),
                    'size': backup['Size']
                }
                for backup in sorted(backup_objects, key=get_last_modified, reverse=True)
            ]
            print(backups[0].keys())

        # remove any results that are empty / just the prefix
        backups = [backup for backup in backups if backup['name'] != ""]

        # can't use s3 MaxKeys param because we want to sort before we limit
        if self.args.limit:
            backups = backups[0:int(self.args.limit)]
        print(json.dumps({'backups': backups}))


class CloudObjectStorageDownload(object):  # pylint: disable=unused-variable
    """Download a file from Cloud Object Storage."""

    command = "cos"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.session = ibm_boto3.session.Session(
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
        )
        self.client = self.session.client("s3", endpoint_url=args.endpoint_url)
        self.s3 = self.session.resource("s3", endpoint_url=args.endpoint_url)
        self.cos = ibm_boto3.resource(
            "s3",
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
            endpoint_url=args.endpoint_url,
        )

    @classmethod
    def parse_args(cls, subparsers):
        """Add Cloud Object Storage arguments to command line parser."""
        cos_oo_parser = subparsers.add_parser("cos", description=cls.__doc__)

        cos_oo_parser.add_argument(
            "-e", "--endpoint-url", help="endpoint URL of the S3 storage"
        )
        cos_oo_parser.add_argument(
            "-s", "--instance-id", help="service instance id")
        cos_oo_parser.add_argument(
            "-u", "--access-key", help="acccess key id of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "-p", "--secret-key", help="secret access key of HMAC credentials"
        )

        cos_oo_parser.add_argument(
            "remote_path",
            help="""Cloud object storage path/prefix to the object
                                  being downloaded""",
        )
        cos_oo_parser.add_argument("bucket", help="target s3 bucket")
        cos_oo_parser.add_argument(
            "local_path",
            nargs="?",
            default=None,
            help="path to save the file to on the local filesystem",
        )

    def download(self):
        """Download a file from `remote_path` to `local_path` on ObjectStorage."""

        LOG.info("Downloading 's3://%s/%s' from '%s' from Cloud Object Storage to '%s'",
                 self.args.bucket,
                 self.args.remote_path,
                 self.args.endpoint_url,
                 os.path.abspath(self.args.local_path))

        bucket = self.s3.Bucket(self.args.bucket)
        bucket.download_file(
            self.args.remote_path,
            os.path.abspath(self.args.local_path)
        )

        LOG.info("Download complete.")

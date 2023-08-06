# backwork-upload-cos [![Build Status](https://travis-ci.org/IBM/backwork-upload-cos.svg?branch=master)](https://travis-ci.org/IBM/backwork-upload-cos) [![PyPI version](https://badge.fury.io/py/backwork-upload-cos.svg)](https://badge.fury.io/py/backwork-upload-cos)

Add support for IBM Cloud Object Storage uploads to [`backwork`](https://github.com/IBM/backwork).

## Installing

You can use `pip` to install this plug-in:

```sh
$ pip install backwork-upload-cos
```

## Using

After installing the plug-in you will be able to use the `upload cos`, `show cos`, and `download cos`
commands on `backwork`.

### `backwork upload cos`

```sh
$ backwork upload cos --help
usage: backwork upload cos [-h] [-e ENDPOINT_URL] [-s INSTANCE_ID]
                          [-u ACCESS_KEY] [-p SECRET_KEY]
                          [local_path] bucket remote_path

Upload a file to Cloud Object Storage.

positional arguments:
  local_path            path in the local file system of the file to be
                        uploaded
  bucket                target s3 bucket
  remote_path           path on Cloud Object Storage where the file will be
                        stored

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint URL of the S3 storage
  -s INSTANCE_ID, --instance-id INSTANCE_ID
                        service instance id
  -u ACCESS_KEY, --access-key ACCESS_KEY
                        acccess key id of HMAC credentials
  -p SECRET_KEY, --secret-key SECRET_KEY
                        secret access key of HMAC credentials
```

### `backwork show cos`

list backups
```sh
usage: backwork show cos [-h] [-e ENDPOINT_URL] [-s INSTANCE_ID]
                         [-u ACCESS_KEY] [-p SECRET_KEY] [-l LIMIT]
                         [--sort-last-modified]
                         bucket path

List available backups in Cloud Object Storage.

positional arguments:
  bucket                target s3 bucket
  path                  Path/prefix to the look for backups in

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint URL of the S3 storage
  -s INSTANCE_ID, --instance-id INSTANCE_ID
                        service instance id
  -u ACCESS_KEY, --access-key ACCESS_KEY
                        acccess key id of HMAC credentials
  -p SECRET_KEY, --secret-key SECRET_KEY
                        secret access key of HMAC credentials
  -l LIMIT, --limit LIMIT
                        max number of results to return
  --sort-last-modified  if passed, sorts results from most to least recent
```

A common use case would be to get the name of the most recent backup:

```sh
backwork show cos \
  --endpoint-url "${IBM_COS_ENDPOINT_URL}" \
  --instance-id "${IBM_COS_INSTANCE_ID}" \
  --access-key "${IBM_COS_ACCESS_KEY}" \
  --secret-key "${IBM_COS_SECRET_KEY}" \
  "my-bucket" \
  "my-path" \
  --limit 1 \
  --sort-last-modified \
  | jq .backups[0]
```

### `backwork download cos`

```sh
$ backwork download cos --help
usage: backwork download cos [-h] [-e ENDPOINT_URL] [-s INSTANCE_ID]
                             [-u ACCESS_KEY] [-p SECRET_KEY]
                             remote_path bucket [local_path]

Download a file from Cloud Object Storage.

positional arguments:
  remote_path           Cloud object storage path/prefix to the object being
                        downloaded
  bucket                target s3 bucket
  local_path            path to save the file to on the local filesystem

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint URL of the S3 storage
  -s INSTANCE_ID, --instance-id INSTANCE_ID
                        service instance id
  -u ACCESS_KEY, --access-key ACCESS_KEY
                        acccess key id of HMAC credentials
  -p SECRET_KEY, --secret-key SECRET_KEY
                        secret access key of HMAC credentials
```


## Author

- `Michael Lin <michael.lin1@ibm.com>`

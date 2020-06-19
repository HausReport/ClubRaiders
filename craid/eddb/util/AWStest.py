#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile

import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    # s3_client.
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        response = s3_client.upload_file(
            file_name, bucket, object_name,
            ExtraArgs={'ACL': 'public-read'}
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.INFO

key = os.getenv('AWS_ACCESS_KEY_ID')
reg = os.getenv('AWS_DEFAULT_REGION')
buck_key = os.getenv('AWS_SECRET_ACCESS_KEY')
buck_name = os.getenv('BUCKET_NAME')

print(key)
print(reg)
print(buck_key)
print(buck_name)

fname = "foo.html"
tmpDir = tempfile.gettempdir()
inFile = os.path.join(tmpDir, fname)
if os.path.exists(inFile):
    logging.info("copying: " + inFile + " to AWS")
    # f = io.BytesIO(fname)
    # with open(fname, "rb") as f:
    upload_file(inFile, buck_name, "foo.html")

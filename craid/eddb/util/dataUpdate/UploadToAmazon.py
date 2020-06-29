#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile

import boto3
from botocore.exceptions import ClientError

from craid.eddb.util.dataUpdate.AWStest import upload_file


def uploadToAWSFromTemp(shortName: str) -> bool:
    key = os.getenv('AWS_ACCESS_KEY_ID')
    reg = os.getenv('AWS_DEFAULT_REGION')
    buck_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    buck_name = os.getenv('BUCKET_NAME')

    print(key)
    print(reg)
    print(buck_key)
    print(buck_name)

    tmpDir = tempfile.gettempdir()
    inFile = os.path.join(tmpDir, shortName)
    if os.path.exists(inFile):
        logging.info(f"copying: {inFile} to AWS bucket {buck_name}/{shortName}")
        return upload_file(inFile, buck_name, shortName + "-test")

    return False

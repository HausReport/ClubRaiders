#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile

from craid.eddb.util.dataUpdate.AWStest import upload_file


def uploadToAWSFromTemp(shortName: str) -> bool:
    key = os.getenv('AWS_ACCESS_KEY_ID')
    reg = os.getenv('AWS_DEFAULT_REGION')
    buck_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    #buck_name = os.getenv('BUCKET_NAME')
    buck_name = "erlaed"

    #logging.info(f"------------->AWS KEY: [{key}]")
    #logging.info(f"------------->AWS REG: [{reg}]")
    #logging.info(f"------------->AWS SKEY: [{buck_key}]")
    #logging.info(f"------------->AWS BUCK: [{buck_name}]")

    tmpDir = tempfile.gettempdir()
    inFile = os.path.join(tmpDir, shortName)
    if os.path.exists(inFile):
        logging.info(f"copying: {inFile} to AWS bucket {buck_name}/{shortName}")
        return upload_file(inFile, buck_name, shortName)

    return False

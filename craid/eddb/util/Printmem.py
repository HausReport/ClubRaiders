#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging

import psutil


def printmem(msg: str):
    process = psutil.Process()
    logging.info("Memory tracker: " + msg + ":" + '{:,}'.format(process.memory_info()[0]))

#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

# logic for caching at:
# https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer
from craid.eddb.loader.strategy.WebLoader import WebDataLoader


class LoadDataFromGithub(WebDataLoader):

    def __init__(self, _forceWebDownload=False, _revision=None, _raw=False, useSmol=True):
        super().__init__(_forceWebDownload, useSmol)
        self.revision = _revision
        self.raw = _raw

    def getWebFilePrefix(self) -> str:
        if self.revision is None:
            return "https://raw.github.com/HausReport/ClubRaiders/master/data/"
        else:
            return "https://github.com/HausReport/ClubRaiders/blob/" + self.revision + "/data/"
            # d5ff5b1741467618df70a75c7078fb6b6fc32fe3/data/smol-systems_populated.jsonl.gz?raw=true

    def getWebFileSuffix(self) -> str:
        if self.raw is False:
            return ""
        return "?raw=true"

# if __name__ == '__main__':
# LoadDataFromEDDB.load_data()

#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

class ScoredMessage:

    def __init__(self, score: float, msg: str):
        self.score = score
        self.msg = msg

    def getScore(self) -> float:
        return self.score

    def getMessage(self) -> str:
        return self.msg

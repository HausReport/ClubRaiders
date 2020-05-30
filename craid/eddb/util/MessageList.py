#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

from util.ScoredMessage import ScoredMessage


class MessageList(object):

    def __init__(self):
        self.messages: List[ScoredMessage] = []

    def addMessage(self, msg: ScoredMessage):
        self.messages.append(msg)

    def add(self, sco: float, msg: str):
        foo = ScoredMessage(sco, msg)
        self.messages.append(foo)

    def toString(self):
        self.messages.sort(key=lambda x: x.score, reverse=True)
        ret: str = ""
        msg: ScoredMessage
        for msg in self.messages:
            ret += "*  " + msg.getMessage()
            ret += "\n"

        return ret

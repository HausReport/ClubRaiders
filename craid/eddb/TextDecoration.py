#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

def boolToTorBlank(myArgument: bool) -> str:
    if myArgument: return "&check;"
    return ""


def boolToTorF(myArgument: bool) -> str:
    if myArgument: return "T"
    return "F"


def boolToYesOrNo(myArgument: bool) -> str:
    if myArgument: return "Yes"
    return "No"

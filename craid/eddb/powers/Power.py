#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause

# "Aisling Duval"
# "Archon Delaine"
# "Arissa Lavigny-Duval"
# "Denton Patreus"
# "Edmund Mahon"
# "Felicia Winters"
# "Li Yong-Rui"
# "Pranav Antal"
# "Yuri Grom"
# "Zachary Hudson"
# "Zemina Torval"
# null
#
#
# "Contested"
# "Control"
# "Expansion"
# "Exploited"
# "Home System"
# null

class Power:
    NAME = 'name'

    def __init__(self, name=''):
        self._name: str = name

    def get_name(self) -> str:
        return self._name

    def set_name(self, x: str):
        self._name = x

    def smugglingMultiplier(self, sys) -> float:
        return 1.0

    def bountyMultiplier(self, sys) -> float:
        return 1.0

    def influenceMultiplier(self, sys) -> float:
        return 1.0

    def smugglingMessage(self, sys) -> str:
        return ""

    def bountyMessage(self, sys) -> str:
        return ""

    def influenceMessage(self, sys) -> str:
        return ""
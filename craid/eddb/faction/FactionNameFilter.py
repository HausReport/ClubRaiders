#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
#
from typing import Set

from craid.eddb.faction.Faction import Faction

# Have gone back and forth about having 'Bill Turner' in the list
badGuys: Set[str] = {'Abroin Universal PLC', 'Aegis Core', 'Aegis Research',
                     #"Benton's Gang", 'Bentonian Party',
                     'CQC Holdings',
                     'Gallant Investment Brokers', 'Hodack Prison Colony',
                     'Janus Incorporated', "Namarii Emperor's Dawn", 'Reyan BPS',
                     'Reynhardt IntelliSys', 'Sirius Atmospherics', 'Sirius Catering',
                     'Sirius Corporation', 'Sirius Drives', 'Sirius Hot2Cold',
                     'Sirius Hyperspace', 'Sirius Industrial',
                     'Sirius Luxury Transports', 'Sirius Mining Merope',
                     'Sirius Mining', 'Sirius Power', 'The Greenventure Group',
                     'The Peterson Group', 'The Rockforth Corporation',
                     'Turner Research Group', 'Wiggins Development Trust',
                     #'Worster Insurance',
                     'Wreaken Construction', 'Aegis Defense', 'Pleiades Resource Enterprise'}


class FactionNameFilter(object):

    @staticmethod
    def proClubFaction(CurFaction: Faction):
        # global FactionNameFilter.badGuys
        global badGuys
        curName = CurFaction.get_name()
        if curName in badGuys:
            return True
        return False

    @staticmethod
    def proClubFactionName(theName: str):
        global badGuys
        if theName in badGuys:
            return True
        return False

    @staticmethod
    def antiClubFactions(CurFaction):
        curName = CurFaction.get_name()
        if "Alliance Assembly" in curName: return True
        if "Mastapolos" in curName: return True
        if "Dark Wheel" in curName: return True
        if "Jet Gang" in curName: return True
        if "Raxxla" in curName: return True
        if "Yupini Limited" in curName: return True
        return False

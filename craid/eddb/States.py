#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import List

import craid.eddb.Constants as Constants


class Vulnerability:

    def __init__(self, govt: str, influence: float, state_dict):
        self.govt = govt
        self.influence = influence
        self.state_list: List[int] = []

        for state in state_dict:
            xid: int = int(state['id'])
            if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            if xid is Constants.STATE_WAR: self.state_list.append(xid)
            if xid is Constants.STATE_CIVIL_WAR: self.state_list.append(xid)
            if xid is Constants.STATE_ELECTION: self.state_list.append(xid)
            if xid is Constants.STATE_OUTBREAK: self.state_list.append(xid)
            if xid is Constants.STATE_INFRASTRUCTURE_FAILURE: self.state_list.append(xid)
            if xid is Constants.STATE_EXPANSION: self.state_list.append(xid)


            #
            # For mining/trade
            #
            if xid is Constants.STATE_BOOM: self.state_list.append(xid)
            if xid is Constants.STATE_CIVIL_LIBERTY: self.state_list.append(xid)
            if xid is Constants.STATE_PUBLIC_HOLIDAY: self.state_list.append(xid)
            if xid is Constants.STATE_PIRATE_ATTACK: self.state_list.append(xid)
            if xid is Constants.STATE_INVESTMENT: self.state_list.append(xid)

            # if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            # if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            # if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            #if xid is Constants.STATE_EXPANSION: self.state_list.append(xid)

    # a little experimental, but should be close
    def getMineralSalesString(self):
        if Constants.STATE_BOOM in self.state_list or Constants.STATE_INVESTMENT in self.state_list:
            ct: int = 0
            if Constants.STATE_CIVIL_LIBERTY in self.state_list: ct +=1
            if Constants.STATE_EXPANSION in self.state_list: ct +=1
            if Constants.STATE_PUBLIC_HOLIDAY in self.state_list: ct +=1
            if(ct<2): return ""
            if Constants.STATE_PIRATE_ATTACK in self.state_list: ct +=1
            return "MinSales" + ("+"*ct)

        return ""

    def getShortString(self):
        war: List[str] = []
        if 4.5 >= self.influence > 0.0:
            war.append("LowInf")
        if self.govt == "Anarchy":
            war.append("Anarchy")

        if Constants.STATE_RETREAT in self.state_list:
            war.append("Retreat")

        if Constants.STATE_WAR in self.state_list:
            war.append("War")
        if Constants.STATE_CIVIL_WAR in self.state_list:
            war.append("CivilWar")
        if Constants.STATE_ELECTION in self.state_list:
            war.append("Election")

        if Constants.STATE_OUTBREAK in self.state_list:
            war.append("Outbreak")
        if Constants.STATE_INFRASTRUCTURE_FAILURE in self.state_list:
            war.append("InfFail")
        if Constants.STATE_EXPANSION in self.state_list:
            war.append("Expans")

        if len(war) == 0:
            return ""
        return ",".join(war)

    # def getSort(self):
    # return [{'column_id': 'distance', 'direction': 'asc'}]

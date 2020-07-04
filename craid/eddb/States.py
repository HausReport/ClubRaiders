#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import List

import craid.eddb.base.GameConstants as gconst


# "16,Boom"
# "32,Bust"
# "37,Famine"
# "48,Civil Unrest"
# "64,Civil War"
# "65,Election"
# "66,Civil Liberty"
# "67,Expansion"
# "69,Lockdown"
# "72,Outbreak"
# "73,War"
# "80,None"
# "81,Pirate Attack"
# "101,Investment"
# "102,Blight"
# "103,Drought"
# "104,Infrastructure Failure"
# "105,Natural Disaster"
# "106,Public Holiday"
# "107,Terrorist Attack"

class States:

    def __init__(self, govt: str, influence: float, state_dict):
        self.govt = govt
        self.influence = influence
        self.state_list: List[int] = []

        for state in state_dict:
            xid: int = int(state['id'])
            if xid is gconst.STATE_RETREAT: self.state_list.append(xid)
            if xid is gconst.STATE_WAR: self.state_list.append(xid)
            if xid is gconst.STATE_CIVIL_WAR: self.state_list.append(xid)
            if xid is gconst.STATE_ELECTION: self.state_list.append(xid)
            if xid is gconst.STATE_OUTBREAK: self.state_list.append(xid)
            if xid is gconst.STATE_INFRASTRUCTURE_FAILURE: self.state_list.append(xid)
            if xid is gconst.STATE_EXPANSION: self.state_list.append(xid)

            #
            # For mining/trade
            #
            if xid is gconst.STATE_BOOM: self.state_list.append(xid)
            if xid is gconst.STATE_CIVIL_LIBERTY: self.state_list.append(xid)
            if xid is gconst.STATE_PUBLIC_HOLIDAY: self.state_list.append(xid)
            if xid is gconst.STATE_PIRATE_ATTACK: self.state_list.append(xid)
            if xid is gconst.STATE_INVESTMENT: self.state_list.append(xid)

            if xid is gconst.STATE_LOCKDOWN: self.state_list.append(xid)
            if xid is gconst.STATE_FAMINE: self.state_list.append(xid)
            if xid is gconst.STATE_CIVIL_UNREST: self.state_list.append(xid)

            # if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            # if xid is Constants.STATE_RETREAT: self.state_list.append(xid)
            # if xid is Constants.STATE_EXPANSION: self.state_list.append(xid)

    def hasState(self, which: int) -> bool:
        return which in self.state_list

    def getShortString(self,pending=False,recovering=False):
        war: List[str] = []
        prefix =""
        if pending:
            prefix="Pend"
        elif recovering:
            prefix="Rec"

        if len(prefix) == 0:
            if 4.5 >= self.influence > 0.0:
                war.append("LowInf")
            if self.govt == "Anarchy":
                war.append("Anarchy")

        if gconst.STATE_RETREAT in self.state_list:
            war.append(prefix+"Retreat")

        if gconst.STATE_WAR in self.state_list:
            war.append(prefix+"War")
        if gconst.STATE_CIVIL_WAR in self.state_list:
            war.append(prefix+"CivilWar")
        if gconst.STATE_ELECTION in self.state_list:
            war.append(prefix+"Election")

        if gconst.STATE_OUTBREAK in self.state_list:
            war.append(prefix+"Outbreak")
        if gconst.STATE_INFRASTRUCTURE_FAILURE in self.state_list:
            war.append(prefix+"InfFail")
        if gconst.STATE_EXPANSION in self.state_list:
            war.append(prefix+"Expans")

        if len(war) == 0:
            return ""
        return ",".join(war)

    # def getSort(self):
    # return [{'column_id': 'distance', 'direction': 'asc'}]

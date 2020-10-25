#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.system.InhabitedSystem import InhabitedSystem

#
# Need:
#    start date
#    ally name
#    ally initial influence
#    target name
#

#
# Form
#    a simulation
#

#
#  Return
#    campaign graph
#    campaign strategy text
#    estimated days
#

class Campaign():
    sys: InhabitedSystem
    ally: FactionInstance
    target: FactionInstance


    

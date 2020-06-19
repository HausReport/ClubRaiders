#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Faction constants
#
GOVERNMENT = 'government'
MINOR_FACTION_ID = 'minor_faction_id'
MINOR_FACTION_PRESENCES = 'minor_faction_presences'
NEIGHBOR_COUNT = 'neighbor_count'
HAS_ANARCHY = 'hasAnarchy'
ID = 'id'
NEIGHBORS = 'neighbors'
POWER_STATE = 'power_state'

#
# System constants
#
HAS_DOCKING = 'has_docking'
SYSTEM_ID = 'system_id'
PAD_SIZE = 'max_landing_pad_size'
DISTANCE_TO_STAR = 'distance_to_star'
STATION_TYPE = 'type'

STATE_BOOM = 16
STATE_BUST = 32
STATE_FAMINE = 37
STATE_CIVIL_UNREST = 48
STATE_CIVIL_WAR = 64
STATE_ELECTION = 65
STATE_CIVIL_LIBERTY = 66
STATE_EXPANSION = 67
STATE_LOCKDOWN = 69
STATE_OUTBREAK = 72
STATE_WAR = 73
STATE_NONE = 80
STATE_PIRATE_ATTACK = 81
STATE_RETREAT = 96
STATE_INVESTMENT = 101
STATE_BLIGHT = 102
STATE_DROUGHT = 103
STATE_INFRASTRUCTURE_FAILURE = 104
STATE_NATURAL_DISASTER = 105
STATE_PUBLIC_HOLIDAY = 106
STATE_TERRORIST_ATTACK = 107

#     if STATE_RETREAT in state_dict: ret.append(STATE_RETREAT) #96
#     STATE_WAR = 73
#     STATE_CIVIL_WAR = 64
#     STATE_ELECTION = 65
#
#     STATE_OUTBREAK = 72
#     STATE_INFRASTRUCTURE_FAILURE = 104
#     STATE_EXPANSION = 67
#
#     ','.join(ret)
#     #STATE_BOOM = 16
#     #STATE_BUST = 32
#     #STATE_FAMINE = 37
#     #STATE_CIVIL_UNREST = 48
#     #STATE_CIVIL_LIBERTY = 66
#     #STATE_LOCKDOWN = 69
#     #STATE_NONE = 80
#     #STATE_PIRATE_ATTACK = 81
#     #STATE_INVESTMENT = 101
#     #STATE_BLIGHT = 102
#     #STATE_DROUGHT = 103
#     #STATE_NATURAL_DISASTER = 105
#     #STATE_PUBLIC_HOLIDAY = 106
#     #STATE_TERRORIST_ATTACK = 107
#
#     for state in state_dict:
#         if (state['id'] == 64):
#             return 64
#         if (state['id'] == 65):
#             return 65
#         if (state['id'] == 73):
#             return 73
#         if (state['id'] == 96):
#             return 96
#         if (state['id'] == 104):
#             return 104
#
#     return 0

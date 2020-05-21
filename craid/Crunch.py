import json

import pandas as pd

from craid import Club
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem

all_factions_dict: Faction = {}
# all_stations_dict : Station = {}
all_systems_dict: InhabitedSystem = {}
club_factions_dict: Faction = {}
club_systems_arr: FactionInstance = [ ]

#
# Identified Pro-Club Faction Names
#


with open("data/factions.jsonl", 'r') as handle:
    for line in handle:
        lCurFaction = json.loads(line)
        lCurFactionId = int(lCurFaction[ 'id' ])
        curFaction = Faction(lCurFaction)
        all_factions_dict[ lCurFactionId ] = curFaction
        if Club.proClubFaction(curFaction):
            club_factions_dict[ lCurFactionId ] = curFaction

# with open(stations_file, 'r') as handle:
#      for line in handle:
#         station = json.loads(line)
#         system_id = station[ SYSTEM_ID ]
#         current_station = stations_dict.get(system_id)

with open("data/systems_populated.jsonl", 'r') as handle:
    for line in handle:
        sys = json.loads(line)
        tid = int(sys[ 'id' ])
        foo = InhabitedSystem(sys)
        all_systems_dict[ tid ] = foo


def desiredState(state_dict):
    for state in state_dict:
        if (state[ 'id' ] == 64): return 64
        if (state[ 'id' ] == 65): return 65
        if (state[ 'id' ] == 73): return 73
        if (state[ 'id' ] == 96): return 96
        if (state[ 'id' ] == 104): return 104

    return 0


for tsys in all_systems_dict.values():
    ttsys: InhabitedSystem = tsys
    mfp = ttsys.getMinorFactionPresences()
    for faction_ptr in mfp:
        if faction_ptr is None:
            continue
        faction_id = int(faction_ptr[ 'minor_faction_id' ])
        if faction_id is None:
            continue
        if faction_id in club_factions_dict:
            fac = club_factions_dict[ faction_id ]
            facname = fac.get_name2()
            if (facname.startswith("*")): continue  # filters player factions

            sysname = ttsys.get_name()
            facHome = fac.get_homesystem_id()
            sysid = ttsys.get_id()
            vulnerable = True
            if (sysid == facHome): vulnerable = False

            govt = ttsys.getGovernment()
            # allg = fac.get_allegiance()

            inf = faction_ptr[ 'influence' ]
            # sinf = '{:04.2f}'.format(inf)
            # print(sinf)

            # updated = ttsys.getUpdated();
            # date = datetime.datetime.utcfromtimestamp(updated)
            # ds = date.strftime("%m/%d/%Y %H:%M:%S")

            active_states = json.dumps(faction_ptr[ 'active_states' ])
            hasWar = desiredState(faction_ptr[ 'active_states' ])
            if (govt == "Anarchy"):
                hasWar = -16
            if (hasWar == 0 and inf <= 3.5 and inf > 0.0):
                hasWar = -15
            if (hasWar == 104 and inf > 10.0):
                hasWar = 0

            sysIns = FactionInstance(fac, ttsys, inf, hasWar)
            club_systems_arr.append(sysIns)
            # print(facname + "," + sysname)
            # print("=====================================================================================")
            # print(facname + "," + sysname + "," + x + "," + y + "," + z + "," + allg + "," + sinf + "," + war+ "," + ds )  # + "," + allg)

xs = [ ]
ys = [ ]
zs = [ ]
factionName = [ ]
systemName = [ ]
allgs = [ ]

for xcs in club_systems_arr:
    cs: FactionInstance = xcs
    # vulnerable = cs.isVulnerable()
    # if (vulnerable == False): continue
    factionName.append(cs.get_name())
    systemName.append(cs.getSystemName())
    xs.append(cs.getX())
    ys.append(cs.getY())
    zs.append(cs.getZ())
    allgs.append(cs.get_allegiance())

data = {
    'systemName': systemName,
    'factionName': factionName,
    'x': xs,
    'y': ys,
    'z': zs,
    'allegiance': allgs
}

#
# Main dataframe of all club factions
#
df = pd.DataFrame(data=data)

#
# Dataframe of all club factions except Emp Grace
#
filter = df[ ~df[ 'factionName' ].str.contains("Emperor's Grace") ]

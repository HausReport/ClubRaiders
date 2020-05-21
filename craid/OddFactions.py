import json
import os
import re

import named.Faction
import named.Systems

GOVERNMENT = 'government'
MINOR_FACTION_ID = 'minor_faction_id'
MINOR_FACTION_PRESENCES = 'minor_faction_presences'
NEIGHBOR_COUNT = 'neighbor_count'
HAS_ANARCHY = 'hasAnarchy'
ID = 'id'
NEIGHBORS = 'neighbors'
POWER_STATE = 'power_state'

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(data_dir, 'venv\\data\\')
factions_file = os.path.join(data_dir, 'factions.jsonl')
populated_systems_file = os.path.join(data_dir, 'systems_populated.jsonl')

factions_dict = {}
words_dict = {}
filter_words_dict = {}
rare_words_dict = {}
rarity = 5


# pat = re.compile('[0-9\-+.a]+')


# name2 = "HIP 44791 First"
# name2 = name2.replace("HIP ", "")
# name2 = name2.replace('[0-9]+', "")
#
# print(name2)
# if True:
# exit(0)


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


systems_dict = {}
with open(populated_systems_file, 'r') as handle:
    for line in handle:
        sys = json.loads(line)
        tid = sys[ ID ]
        tn = sys[ 'name' ]
        systems_dict[ tid ] = tn
#
# Load the factions
#
with open(factions_file, 'r') as handle:
    for line in handle:
        lCurFaction = json.loads(line)
        curFaction = named.Faction.Faction(lCurFaction)
        lCurFactionId = lCurFaction[ 'id' ]
        factions_dict[ lCurFactionId ] = curFaction

print("================================================================================")


def getFactionById(id):
    return factions_dict.get(id)

for sysname in systems_dict.values():
    words = sysname.split()

    for word in words:
        if word in filter_words_dict:
            filter_words_dict[ word ] += 1
        else:
            filter_words_dict[ word ] = 1

# shit = "Aasgay Independents"
# sn = systems_dict.get(int("19858"), "")
# print(shit.replace(sn, "").strip())

# if True:
# exit(0)

for faction in factions_dict.values():
    name2: str = faction.get_name2()

    if name2.startswith("*"): continue

    sid: int = faction.get_homesystem_id()
    sn = systems_dict.get(sid, "")

    # name2 = name2.replace(sn, "")
    # name2 = name2.replace("HIP ", "")
    # name2 = name2.replace("HR ", "")
    # name2 = name2.replace("LHS ", "")
    # name2 = name2.replace("LP ", "")
    # name2 = name2.replace("BD+", "")
    # name2 = name2.replace("BD-", "")
    # name2 = name2.replace("CD-", "")
    name2 = name2.strip()

    words = name2.split()

    for word in words:
        #if RepresentsInt(word) == True: continue
        #if re.search('[0-9\-+.a]+', word): continue

        if word in words_dict:
            words_dict[ word ] += 1
        else:
            words_dict[ word ] = 1

for ct in words_dict.keys():
    count = words_dict[ ct ]
    if (count <= rarity):
        if (count >= 1):
            if( ct not in filter_words_dict):
                rare_words_dict[ ct ] = int(words_dict[ ct ])

# sortkeys = list(rare_words_dict.keys())
# sortkeys.sort()
# for word in sortkeys:
# print(word)
# if True:
# exit(0)

for faction in factions_dict.values():
    name = faction.get_name2()
    if (name.startswith("*")): continue
    for ct in rare_words_dict.keys():
        words = name.split()
        for word in words:
            if (word == ct):
                print(ct + "\t" + str(rare_words_dict[ ct ]) + "\t" + name + "\t" + str(faction.get_homesystem_id()))
                break
print("================================================================================")

import json
import os
from typing import Dict

from craid.eddb.Faction import Faction

# GOVERNMENT = 'government'
# MINOR_FACTION_ID = 'minor_faction_id'
# MINOR_FACTION_PRESENCES = 'minor_faction_presences'
# NEIGHBOR_COUNT = 'neighbor_count'
# HAS_ANARCHY = 'hasAnarchy'
ID = 'id'
# NEIGHBORS = 'neighbors'
# POWER_STATE = 'power_state'

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(data_dir, 'venv\\data\\')
factions_file = os.path.join(data_dir, 'factions.jsonl')
populated_systems_file = os.path.join(data_dir, 'systems_populated.jsonl')

factions_dict: Dict[int, Faction] = {}
words_dict: Dict[int, Faction] = {}
filter_words_dict: Dict[str, int] = {}
rare_words_dict: Dict[str, int] = {}
rarity = 5

systems_dict = {}
with open(populated_systems_file, 'r') as handle:
    for line in handle:
        sys = json.loads(line)
        tid = sys[ID]
        tn = sys['name']
        systems_dict[tid] = tn
#
# Load the factions
#
with open(factions_file, 'r') as handle:
    for line in handle:
        lCurFaction = json.loads(line)
        curFaction = Faction(lCurFaction)
        lCurFactionId = lCurFaction['id']
        factions_dict[lCurFactionId] = curFaction


def getFactionById(_id):
    return factions_dict.get(_id)


for systemName in systems_dict.values():
    words = systemName.split()

    for word in words:
        if word in filter_words_dict:
            filter_words_dict[word] += 1
        else:
            filter_words_dict[word] = 1

for faction in factions_dict.values():
    name2: str = faction.get_name2()

    if name2.startswith("*"):
        continue

    sid: int = faction.get_homesystem_id()
    sn = systems_dict.get(sid, "")
    name2 = name2.strip()

    words = name2.split()

    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1

for ct in words_dict.keys():
    count: int = words_dict[ct]
    if count <= rarity and (count >= 1) and (ct not in filter_words_dict):
        rare_words_dict[ct] = int(words_dict[ct])

for faction in factions_dict.values():
    name = faction.get_name2()
    if name.startswith("*"):
        continue
    for ct in rare_words_dict.keys():
        words = name.split()
        for word in words:
            if word == ct:
                print(ct + "\t" + str(rare_words_dict[ct]) + "\t" + name + "\t" + str(faction.get_homesystem_id()))
                break

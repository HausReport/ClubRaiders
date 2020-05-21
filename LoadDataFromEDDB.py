import requests

if(True is True):
  #
  # Gets the most recent data dumps from eddb.io
  #
  url = 'https://eddb.io/archive/v6/systems_populated.jsonl'
  r = requests.get(url, allow_redirects=True)
  open('data/systems_populated.jsonl', 'wb').write(r.content)

  #url = 'https://eddb.io/archive/v6/stations.jsonl'
  #r = requests.get(url, allow_redirects=True)
  #open('data/stations.jsonl', 'wb').write(r.content)

  url = 'https://eddb.io/archive/v6/factions.jsonl'
  r = requests.get(url, allow_redirects=True)
  open('data/factions.jsonl', 'wb').write(r.content)
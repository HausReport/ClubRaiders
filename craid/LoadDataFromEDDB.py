import os

import requests

#logic for caching at:
#https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer

def load_data():
    if not os.path.exists('data'):
        os.makedirs('data')
    if (True is True):
        #
        # Gets the most recent data dumps from eddb.io
        #
        url = 'https://eddb.io/archive/v6/systems_populated.jsonl'
        r = requests.get(url, allow_redirects=True)
        open('data/systems_populated.jsonl', 'wb').write(r.content)

        # url = 'https://eddb.io/archive/v6/stations.jsonl'
        # r = requests.get(url, allow_redirects=True)
        # open('data/stations.jsonl', 'wb').write(r.content)

        url = 'https://eddb.io/archive/v6/factions.jsonl'
        r = requests.get(url, allow_redirects=True)
        open('data/factions.jsonl', 'wb').write(r.content)

if __name__ == '__main__':
    load_data()

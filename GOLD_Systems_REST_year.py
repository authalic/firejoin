
import requests
import json
import GOLD_Systems_token

from dateutil.parser import parse # for parsing datetime strings in the format "2019-08-21T21:01:00.000Z"
from datetime import datetime # for strptime() output format
from datetime import timedelta # to increment the dates in the API calls


# FBS API Documentation
# https://ut.firebilling.org/fire/s/api

# Acceptance testing URL
# resturl = "https://testut.firebilling.org/fire/s/api/incidents"

# URL of GOLD Systems REST service
resturl = "https://ut.firebilling.org/fire/s/api/incidents"


# URL parameters
# Options and examples
    # 'irwinId': '57c08414-6cac-43b9-bc33-611af128f22d'  # Pahvant WMA
    # 'irwinId': 'd59ee23f-17b6-4153-bf6f-629161315654'  # West Tridell (acreages available)
    # 'irwinId': '1bfd3a06-0959-4fdf-a7d9-72b7b1bb78a3'  # Green Ravine
    # 'year': 2019
    # 'incidentNumber: 'UTSWS-000029'
    # 'modifiedFrom': '2020-08-01T06:00:00.000Z',
    # 'modifiedTo':   '2020-08-19T05:59:59.000Z'


# HTTP Headers: required for authorization
headers = {
    'Authorization': GOLD_Systems_token.get_token() # tokens expire after 15min
}


def printjson(r):
    '''print and prettify the dict using the json.dumps() method'''
    print(json.dumps(r, sort_keys=True, indent=4))


def get_incidents(fireyear):

    payload = {'year': fireyear}

    # get the Requests Response object
    r = requests.get(resturl, headers=headers, params=payload)


    # return the incidents in JSON format
    return json.dumps(r.json())


# test code

incidents = get_incidents('1999')


print(incidents)

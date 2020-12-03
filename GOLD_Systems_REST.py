
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


def from_gsdate(datestring):
    '''
    accepts a timestamp string in the format used by the Gold Systems API.
    returns a Python Datetime object of that value.
    '''

    # example: '2020-08-01T06:00:00.000Z'

    return parse(datestring)


def to_gsdate(dt):
    '''
    converts a datetime object to the string format used by Gold Systems
    '''
    return dt.isoformat().split('+')[0] + '.000Z'


def get_incidents(datetime_start, datetime_end):
    '''returns a JSON file of all incidents modified between start and end times
       dates and times are in UTC
    '''

    # parse date strings into Datetime objects
    try:
        date1 = from_gsdate(datetime_start)   # initial start date
        date2 = date1 + timedelta(days=1)     # start date +1 day
    except:
        print("input date formats not parseable")

    # Gold Systems API has a call limit of 1000 records
    # loop through the date range and makes an API call for each day

    # list to store incidents from each date iteration
    incidents = []

    while date1 < from_gsdate(datetime_end):

        payload = {
            'modifiedFrom': to_gsdate(date1),
            'modifiedTo':   to_gsdate(date2)
            }

        # get the Requests Response object
        r = requests.get(resturl, headers=headers, params=payload)

        if r:
            # print(r.json()["incidents"], '\n\n')
            # append the returned incidents to the dict

            for incident in r.json()["incidents"]:
                incidents.append(incident)

        # increment the date range by 1 day
        date1 = date1 + timedelta(days=1)
        date2 = date2 + timedelta(days=1)


    # return the incidents in prettified JSON format
    return json.dumps({"incidents": incidents, "messages": [], "success": True}, sort_keys=False, indent=4)


# test code

incidents = get_incidents('2020-01-1T07:00:00.000Z', '2020-01-15T06:59:59.000Z')


print(incidents)

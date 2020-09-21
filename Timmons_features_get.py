import json
import requests
# from urllib.parse import urljoin

# get fire polygon features from the Timmons polygon REST api


# Timmons Map Server:        https://maps3.timmons.com/arcgis/rest/services/utwrap/FireMAP/MapServer/
# Incident Points:           https://maps3.timmons.com/arcgis/rest/services/utwrap/FireMAP/MapServer/0
# Fire Perimeters (outline): https://maps3.timmons.com/arcgis/rest/services/utwrap/FireMAP/MapServer/1
# Fire Perimeters (fill)   : https://maps3.timmons.com/arcgis/rest/services/utwrap/FireMAP/MapServer/2

# URL of feature service
featserv_url = r'https://maps3.timmons.com/arcgis/rest/services/utwrap/FireMAP/MapServer/1'
output_filename = 'results.json'


# SQL WHERE clause for API request
whereclause = '1=1'

# URL query string key/value pairs
payload = {
    "where": whereclause,
    "text": "",
    "objectIds": "",
    "time": "",
    "geometry": "",
    "geometryType": "esriGeometryEnvelope",
    "inSR": "",
    "spatialRel": "esriSpatialRelIntersects",
    "relationParam": "",
    "outFields": "*",
    "returnGeometry": "true",
    "returnTrueCurves": "false",
    "maxAllowableOffset": "",
    "geometryPrecision": "6",  # number of decimal places in x/y coordinates
    "outSR": "4326",
    "returnIdsOnly": "false",
    "returnCountOnly": "false",
    "orderByFields": "",
    "groupByFieldsForStatistics": "",
    "outStatistics": "",
    "returnZ": "false",
    "returnM": "false",
    "gdbVersion": "",
    "returnDistinctValues": "false",
    "resultOffset": "",               # starting point of record request
    # max number of records per API request (usually 1000)
    "resultRecordCount": "",
    "queryByDistance": "",
    "returnExtentsOnly": "false",
    "datumTransformation": "",
    "parameterValues": "",
    "rangeValues": "",
    "f": "pjson",
    "token": ""  # see: agol_token.py script for info on how to set this value
}


def getRecordCount(featserv_url):
    query_url = featserv_url.strip('/') + r'/query'

    payload = {
        'where': '1=1',
        'returnCountOnly': 'false',
        'f': 'pjson'
    }
    r = requests.get(query_url, params=payload)
    records = json.loads(r.text)

    return int(records["count"])


def getMaxRecordCount(featserv_url):
    services_url = featserv_url.strip('/') + r'?f=pjson'

    r = requests.get(services_url)
    records = json.loads(r.text)

    return int(records["maxRecordCount"])


def getRecords(featserv_url, payload):
    # request the total number of records (recordCount)
    # in increments of max requests permitted per API call (batchsize)

    query_url = featserv_url.strip('/') + r'/query'

    # total record count in feature service
    recordcount = getRecordCount(featserv_url)
    # number of records requested per API call (usually 1000 max)
    batchsize = getMaxRecordCount(featserv_url)
    payload["resultRecordCount"] = batchsize

    print(recordcount, "total records")

    for offset in range(0, recordcount, batchsize):

        if offset + batchsize <= recordcount:
            print(str(offset) + " - " + str(offset + batchsize))
        else:
            print(str(offset) + " - " + str(recordcount))

        # set the starting point for the next batch of records requested
        payload["resultOffset"] = offset

        # send the GET request to the REST endpoint
        r = requests.get(query_url, params=payload)  # SHOULD BE QUERY URL

        if offset == 0:
            # first API request: save complete JSON response as dict
            records = json.loads(r.text)
        else:
            # each subsequent request, append only the records to dict
            j = json.loads(r.text)
            records["features"] += j["features"]

    return records


def writeRecords(records, prettify):
    # write the dictionary of results to a JSON text file
    with open(output_filename, 'w') as file:

        if(prettify):
            file.write(json.dumps(records, sort_keys=False, indent=4))
        else:
            file.write(json.dumps(records))


records = getRecords(featserv_url, payload)
writeRecords(records, True)

print("done")

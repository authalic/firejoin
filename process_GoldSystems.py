'''
Transform the output of the Gold Systems API to an Esri GeoJSON FeatureCollection format.
Currenlty only supports point features (lat/lon)

todo: incorporate the polygon features
'''

import json


jsonfile = 'output_test.json'
outputfile = 'gs_geojson.json'

# # pretty print the JSON dict
# print(json.dumps(d, sort_keys=True, indent=4))


def feature(incident):

    # reformat an incident from the REST API dict to the Esri GeoJSON format
    # Note: Order of keys in the dict is important in the final output

    # test if lat/lon values are not null
    if(incident["initialLongitude"] and incident["initialLatitude"]):

        geometry = {}
        geometry["type"] = "Point"
        geometry["coordinates"] = [float(incident["initialLongitude"]), float(incident["initialLatitude"])]

        f = {}
        f["type"] = "Feature"
        f["geometry"] = geometry
        f["properties"] = incident

        return f


def featurecoll(jsonfile):

    # open the output json file from Gold Systems REST API

    with open(jsonfile) as f:
        d = json.loads(f.read())

    fc = {
        "type": "FeatureCollection",
        "features": []
    }

    # loop through all the incident dicts
    for i in d['incidents']:
        fc["features"].append(feature(i))

    return fc


# build a feature collection

fc = featurecoll(jsonfile)

output = open(outputfile, 'w')
output.write(json.dumps(fc))
output.close()

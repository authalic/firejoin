'''
Transform the output of the Gold Systems API to an Esri GeoJSON FeatureCollection format.
Currenlty only supports point features (lat/lon)

todo: incorporate the polygon features
'''

import json


jsonfile = 'api_output.json'
outputfile = 'gs_esri_geojson.json'

# # pretty print the JSON dict
# print(json.dumps(d, sort_keys=True, indent=4))


def feature(incident):

    # reformat an incident from the REST API dict to the Esri GeoJSON format
    # Note: Order of keys in the dict is important in the final output

    # test if lat/lon values are not null
    if(incident["initialLongitude"] and incident["initialLongitude"]):

        # test if lat/lon values are valid coords in north & west hemispheres
        if(
            float(incident["initialLongitude"]) <= 0 and
            float(incident["initialLongitude"]) >= -180 and
            float(incident["initialLatitude"]) >= 0 and
            float(incident["initialLatitude"]) <= 90
        ):
            geometry = {}
            geometry["type"] = "Point"
            geometry["coordinates"] = [float(incident["initialLongitude"]), float(incident["initialLatitude"])]

            f = {}
            f["type"] = "Feature"
            f["geometry"] = geometry
            f["properties"] = incident

            return f
        else:
            # return a point on the Equator if the feature lacks lacks valid lat/lon coords
            geometry = {}
            geometry["type"] = "Point"
            geometry["coordinates"] = [-111.0, 0.0]

            f = {}
            f["type"] = "Feature"
            f["geometry"] = geometry
            f["properties"] = incident

            return f
    else:
        # return a point on the Equator if the feature lacks lacks valid lat/lon coords
        # todo: remove this redundant code and rework the if statement
        geometry = {}
        geometry["type"] = "Point"
        geometry["coordinates"] = [-111.0, 0.0]

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
        incident = feature(i)

        # if a feature lacks lat/lon coordinates, feature() will return None

        if incident:
            fc["features"].append(incident)

    return fc


# build a feature collection

fc = featurecoll(jsonfile)

output = open(outputfile, 'w')
output.write(json.dumps(fc, sort_keys=False, indent=4))
output.close()

print("done")

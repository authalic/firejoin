import geopandas

'''
Outline:

    Timmons: extract all of the polygon features from the Timmons feature service
    Store the features in a dict
        key: IrwinID, values: dict of attribute key/value pairs
    Loop through the dict
    for each IrwinID: call the Gold Systems API
    Append the GS key/values to the dict

    output the dict as GeoJSON

'''

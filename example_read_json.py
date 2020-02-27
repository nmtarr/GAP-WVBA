# -*- coding: utf-8 -*-
"""
Created by N. Tarr Feb 27 2020.

Example of how to download GAP species data from ScienceBase, and also
how to deal with dictionaries and lists.

"""
import json
import sciencebasepy as sb

# Paths and variables
toDir = "T:/Temp/"
gap_id = "bbggnx"

# Connect
sb = sb.SbSession()

# Search for gap model item in ScienceBase
gap_id = gap_id[0] + gap_id[1:5].upper() + gap_id[5]
item_search = '{0}_CONUS_HabModel_2001v1.json'.format(gap_id)
items = sb.find_items_by_any_text(item_search)

# Get a public item.  No need to log in.
mod =  items['items'][0]['id']
item_json = sb.get_item(mod)
get_files = sb.get_item_files(item_json, toDir)

# Read in the json of the model
with open(toDir + gap_id + "_CONUS_HabModel_2001v1.json", "r") as inJSON:
    model_json = json.load(inJSON)

# Drill down to the species models
mods = model_json["models"]
NE_summer_primary = [x[1] for x in mods['bBGGNx-s3']['PrimEcoSys']]
SE_summer_primary = [x[1] for x in mods['bBGGNx-s6']['PrimEcoSys']]

# Which ecological systems are selected for SE but not NE?  Use python sets...
SE_only = set(SE_summer_primary) - set(NE_summer_primary)
print(SE_only)
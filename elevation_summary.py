# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:37:40 2020

@author: nmtarr

Description: Code to retrieve elevation parameters from GAP data, both the 
models and the maps.  Results are saved in a csv file.  

The general workflow is to loop through species list (GAP WV birds) and 
retrieve the max and min elevation parameters from the model dictionaries/json.
Then, use the habitat map to determine the elevations of the highest (max) and
lowest (min) grid cells that were identified as habitat.

These processes generate several variables with integer format that can be 
written to a results dataframe and csv.

NOTES:
Since WVBBA only looked at breeding season, we are only concerned with summer
(and year-round) data from GAP.

This code is full of holes and will need to be added to considerably in order
to run it.
"""
from datetime import datetime
import pandas as pd
import json
import sciencebasepy as sb
import os
import glob
import random
from retrying import retry

# Set paths to data
projDir = "P:/Proj6/GAP-WVBA/"
dataDir = projDir + "Data/"
habitatDir = projDir + "Data/habmaps/"
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
resultsCSV = projDir + "Results/elevation_summary.csv"
toDir = "C:/Temp/"
#toDir = "T:/Temp/"

# Read in elevation.csv as a dataframe and save a copy in the archive, 
#run only once as spp list will be reread and duplicated each time
inDF = pd.read_csv(resultsCSV, dtype={'GAP_code': 'string', 
                                      'common_name': 'string'})
timestamp = str(datetime.now(tz=None).strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
newDF = inDF.copy(deep=True)
sppList = pd.read_csv(listDir, dtype={'strUC': 'string',
                                      'strCommonName': 'string'}) 
sppList.rename(columns = {'strUC':'GAP_code'}, inplace = True)
sppList.rename(columns = {'strCommonName':'common_name'}, inplace = True)
sppList.drop(['state_name', 'strScientificName_x','intHa', 
              'strScientificName_y', 'N_birds', 'N_points', 'Det_Rate'], 
             axis='columns', index=None, columns=None, 
            level=None, inplace=True, errors='raise')
fullDF = newDF.append(sppList) 
fullDF.set_index('GAP_code', drop = True, append = False, inplace = True)
fullDF.to_csv(archiveCSV)
fullDF.to_csv(resultsCSV) #updates elev summary table with spp list as index 

# Connect
sb = sb.SbSession()

# Create a function for retrieving the elevation parameter from sciencebase
def elev_from_model(gap_id, parameter, region):
    """
    Downloads GAP habitat model dictionary (json) and retrieves the elevation
    setting.
    
    Parameters:
    gap_id -- GAP species code
    parameter -- either "max" or "min"
    region -- number of region
    
    Example:
    elev = elev_from_model('bAMROx', 'max', '6')
    """
    ######## FILL OUT BY FOLLOWING example_read_json.py

# Get a python list of species codes to loop through.
timestamp = str(datetime.now(tz=None).strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
elTable = pd.read_csv(resultsCSV, index_col = 'GAP_code', dtype={'GAP_code': 'string', 
                                     'common_name': 'string'})                        
i= elTable.index[0:]
for i in elTable.index[0:]:
    gap_id = i[0] + i[1:5].upper() + i[5]
    while gap_id + "*" not in toDir:       
        # Search for gap model item in ScienceBase
        print(str("Retreiving data for ") + gap_id)
        item_search = '{0}_CONUS_HabModel_2001v1.json'.format(gap_id)
        items = sb.find_items_by_any_text(item_search)
# Get a public item.  No need to log in.
        mod =  items['items'][0]['id']
        item_json = sb.get_item(mod)
        sb.get_item_files(item_json, toDir)  
        break
# Read in the json of the model
    try:   
        print("Opening JSON file for gap_id")  
        with open(toDir + gap_id + "_CONUS_HabModel_2001v1.json", 
              "r") as inJSON:
            model_json = json.load(inJSON)

# Drill down to the species models
        mods = model_json["models"]  
        try:
            if gap_id + '-s3' in mods.keys():
                models3 = mods[gap_id + '-s3']
                NE_maxElev = models3['intElevMax']
                elTable.loc[i,'GAP_max_NE'] = NE_maxElev
                NE_minElev = models3['intElevMin']
                elTable.loc[i,'GAP_min_NE'] = NE_minElev
            if gap_id + '-y3' in mods.keys():
                modely3 = mods[gap_id + '-y3']
                NE_maxElev = modely3['intElevMax']
                elTable.loc[i,'GAP_max_NE'] = NE_maxElev
                NE_minElev = modely3['intElevMin']
                elTable.loc[i,'GAP_min_NE'] = NE_minElev   
            if gap_id + '-y3' and gap_id + '-s3' not in mods.keys():
                   elTable.loc[i,'GAP_max_NE'] = str("None specified") 
                   elTable.loc[i,'GAP_min_NE'] = str("None specified")
            if NE_maxElev is None:
                    elTable.loc[i,'GAP_max_NE'] = "None" 
            if NE_minElev is None:
                    elTable.loc[i,'GAP_min_NE'] = "None"                      
            print(str("Elevation data filled for") + gap_id)
        except Exception as e: 
            print(str("Failure writing ne_intElev data for") + gap_id) 
            print(e) 

        try:   
            if gap_id + '-s6' in mods.keys():
                models6 = mods[gap_id + '-s6']
                SE_maxElev = models6['intElevMax']
                elTable.loc[i,'GAP_max_SE'] = SE_maxElev
                SE_minElev = models6['intElevMin']
                elTable.loc[i,'GAP_min_SE'] = SE_minElev
            if gap_id + '-y6' in mods.keys():
                modely6 = mods[gap_id + '-y6']
                SE_maxElev = modely6['intElevMax']
                elTable.loc[i,'GAP_max_SE'] = SE_maxElev
                SE_minElev = modely6['intElevMin']
                elTable.loc[i,'GAP_min_SE'] = SE_minElev   
            if gap_id + '-y6' and gap_id + '-s6' not in mods.keys():
                   elTable.loc[i,'GAP_max_SE'] = str("None specified") 
                   elTable.loc[i,'GAP_min_SE'] = str("None specified")
            if SE_maxElev is None:
                    elTable.loc[i,'GAP_max_SE'] = "None" 
            if SE_minElev is None:
                    elTable.loc[i,'GAP_min_SE'] = "None"   
        except Exception as e: 
            print(str("Failure retreiving se_intElev data for") + gap_id)
            print (e)                
        files = glob.glob(toDir + '*')
        for f in files:
            os.remove(f)
    except Exception as e: 
        print(str("Failure retreiving data for ") + gap_id)
        print(e)        
elTable.to_csv(archiveCSV)
"""    
>>>>>>> c875d4be8258f5965184f227e1af929f0286eb27
    # Return elevation
    return elevation

"""






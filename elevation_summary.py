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

# Set paths to data
projDir = "P:/Proj6/GAP-WVBA/"
habitatDir = projDir + "Data/habmaps/"
resultsCSV = projDir + "Results/elevation_summary.csv"

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
    # Return elevation
    return elevation

# Create a function for retrieving the elevation parameter from sciencebase
def elev_from_map(gap_id, parameter):
    """
    Assessess GAP habitat map against elevation raster to determine the max
    or min elevation of suitable habitat grid cells (summer).
    
    Parameters:
    gap_id -- GAP species code
    parameter -- either "max" or "min"
    
    Example:
    elev = elev_from_map('bAMROx', 'max')
    """
    ######## Not sure yet the best way to do this. arcpy? 
    # Return elevation
    return elevation

# Read in elevation.csv as a dataframe and save a copy in the archive
inDF = pd.read_csv(resultsCSV)
timestamp = str()#use datetime.now() to get a timestamp string for the file name.
archiveCSV = projDir + "Results/elevation_" + timestamp + ".csv"
inDF.to_csv(archiveCSV)
newDF = inDF.copy()

# Get a python list of species codes to loop through.
species_list = 

# For each species, determine the model parameters, and record in the results
# dataframe
for sp in species_list:
    print(sp)
    # Here's a start for how you'd use the function to get data from the hab model
    max_s6 = elev_from_model(sp, 'max', '6')
    newDF.loc[sp, 'GAP_max_SE'] = max_s6
    # Get the max elevation from the habitat map
    max_map = elev_from_map(sp, 'max')
    newDF.loc[sp, 'GAP_max_map'] = max_map
    
newDF.to_csv(resultsCSV)
    



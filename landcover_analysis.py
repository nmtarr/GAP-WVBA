# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:08:21 2020

@author: nmtarr

Issues -- invalid habitat codes recorded 
"""
import pandas as pd
import repo_functions as fun

# Load GAP cover associations
GAP = pd.read_csv(fun.resultsDir + "GAP_spp_lc_cells.csv", header=0)

# Load WV cover associations
WV = pd.read_csv(fun.resultsDir + "WV_spp_lc_detections.csv", header=0) 

# Load WV tally of records per cover type
WV_tally = pd.read_csv(fun.dataDir + "LandCover/WV_habitat_entries.csv",
                       header=0)

# Load land cover crosswalk
cross = pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv", 
                    header=0) 


# Which GAP cover types were sampled? HOW TO DO THIS??????????????????????????

# Define a species -----------------------------------------------------------
species = "Acadian Flycatcher"

# Return associations --------------------------------------------------------
GAP_types = fun.GAP_mapped_in(species)
print("\nGAP")
print(GAP_types)
WVBBA_types = fun.WVBBA_detected_in(species)
print("\nWVBBA")
print(WVBBA_types)

# Which GAP associations were supported? -------------------------------------
'''
For the species, get the WVBBA cover types it was detected in.
For each cover type, gather a list of GAP types linked to it.
Determine the count of GAP types linked to the WVBBA type for use in weighting. 
'''
validated = set([])
for code in WVBBA_types:
    code = code.upper() #  NOT WORKING !!!!!!! for letter ones.
    print(code)

    # WVtoGAP(code):
    GAPs = (cross[lambda x: x['wv_code_fine'] == code]
             ['GAP_code']
             .unique())
    GAPs = [str(int(x)) for x in GAPs]
    print(GAPs)
    print(len(GAPs))
    match = {x[len(GAPs)] for x in GAPs}
    # return GAPs
    validated = match | validated
print(validated)













'''
# gap to wv query ------------------------------------------------------------
code = GAP_types[0]
# GAPtoWV(code):
WVs = (pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv", 
                    header=0)
         [lambda x: x['GAP_code'] == code]
         ['wv_code_fine']
         .unique())
# return WVs
print(WVs)
'''
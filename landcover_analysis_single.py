# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:08:21 2020

@author: nmtarr

Single-species demonstration of assessment of WVBBA support for GAP ecological
system associations.

Objectives of the assessment:
    Can we validate GAP cover type associations with this type of data?
    What are the barriers to this type of comparison?
    Is obtaining useful habitat data in this way (for an atlas) feasible?
   
Per species questions:
    Which existing associations are supported?
    What additional associations are supported?
    How many GAP associations remain unvalidate?
    What proportion of detections were unusable?
    What proportion of detections supported an additional associations?
    What proportion of detections validated an existing association?
    What WVBBA types were entered that couldn't be linked at all?

Across species:    
    What proportion of the records are usable (averaged across species) in 
       light of uncertainties in links.
    Averages of measure from above.

Issues -- invalid habitat codes recorded 

# Load GAP cover associations
#GAP = pd.read_csv(fun.resultsDir + "GAP_spp_lc_cells.csv", header=0)

# Load WV cover associations
#WV = pd.read_csv(fun.resultsDir + "WV_spp_lc_detections.csv", header=0) 

# Load WV tally of records per cover type
#WV_tally = pd.read_csv(fun.dataDir + "LandCover/WV_habitat_entries.csv", header=0)
"""

import pandas as pd
import repo_functions as fun
pd.set_option('display.max_columns', 15)

# Define a species ----------------------------------------------------------
species = 'Tufted Titmouse'

# Load land cover crosswalk - slow loading for some reason
cross = pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv", 
                    header=0,
                    dtype={'GAP_code': str}) 

# Perform crosswalk of detections from WV -> USGAP
master, GAP_linked, unmatched, gap_types, wv_types = fun.cross_to_GAP(species,
                                                                          cross)

# Show validated associations ------------------------------------------------
print("\nValidated associations")
df_valid = master[master['evaluation'] == 'valid']
print(df_valid[['GAP_code', 'GAP_name', 'detections']])

# Show supported additions ---------------------------------------------------
print("\nNew GAP ecological system associations that are supported by WVBBA:")
df_add = master[master['evaluation'] == 'add_association']
print(df_add[['GAP_code', 'GAP_name', 'detections']])

# Show invalid WV codes entered ----------------------------------------------
print("\nInvalid habitat codes entered by WVBBA observers:")
print(unmatched)

# Report and plot results for usable detections ------------------------------
usable_df = pd.DataFrame(index=["Unusable", "Supported validation",
                                "Supported addition", "Total detections"], 
                         columns=["detections"])
usable_df.loc['Supported validation', 'detections'] = int(df_valid[['detections']].sum())
usable_df.loc['Supported addition', 'detections'] = int(df_add[['detections']].sum())
usable_df.loc['Total detections', 'detections'] = wv_types['detections'].sum()
usable_df.loc['Unusable', 'detections'] = int(wv_types['detections'].sum() - 
                                           df_valid[['detections']].sum() - 
                                           df_add[['detections']].sum())
usable_df = usable_df.fillna(0)
print(usable_df)
plt1 = usable_df.drop(['Total detections']).plot(y='detections', kind='pie',
                                                 legend=False, 
                                                 title = species + " Detections",
                                                 colors=['gray', 'g', 'y'])
plt1.set_ylabel("")
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

# Define a species ----------------------------------------------------------
species = "Acadian Flycatcher"
WVBBA_types = fun.WVBBA_detected_in(species)

# Return associations -------------------------------------------------------
GAP_types = fun.GAP_mapped_in(species)
GAP_types = [str(x) for x in GAP_types]
GAP_types = pd.DataFrame(index=GAP_types, columns=['GAP'])
GAP_types['GAP'] = 1
print(GAP_types)

WVBBA_types = fun.WVBBA_detected_in(species)
WVBBA_types = [fun.wv_lc_code_cleaner(code) for code in WVBBA_types]
WVBBA_types = pd.DataFrame(index=WVBBA_types, columns=['WV'])
WVBBA_types['WV'] = 1
print(WVBBA_types)

# Which GAP associations are linked to WVBBA associations? ------------------
'''
For the species, get the WVBBA cover types it was detected in.
For each cover type, gather a list of GAP types linked to it.
Determine the count of GAP types linked to the WVBBA type for use in weighting. 
'''
unmatched=[]
GAP_linked = pd.DataFrame()
GAP_linked.index.name="GAP_code"
for code in WVBBA_types.index:
    GAPs = (cross[lambda x: x['wv_code_fine'] == code]
             ['GAP_code']
             .unique())
    GAPs = [str(int(x)) for x in GAPs]
    match_n = len(GAPs)
    print(GAPs, match_n)
    if match_n != 0:
        for gap in GAPs:
            confi = (cross[(cross['GAP_code'] == int(gap)) &
                          (cross['wv_code_fine'] == code)]
                     ["confidence"]
                     .iloc[0])
            print(confi)
            GAP_linked.loc[gap, 'support'] = confi/match_n
    else:
        unmatched.append(code)
print(GAP_linked)
print(unmatched)

# Filter out links with little support -------  THIS IS SUBJECTIVE
GAP_linked = GAP_linked[GAP_linked["support"] > 0]

# Compile a table of GAP types and WVBBA support for the sp ------------------
aaa = (GAP_types.merge(GAP_linked, left_index=True, right_index=True, 
                       how='outer')
       .fillna(0))
aaa.index.name = 'GAP_code'


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
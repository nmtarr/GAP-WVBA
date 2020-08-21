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
"""
# Define a species ----------------------------------------------------------
species = "Louisiana Waterthrush"

import pandas as pd
import repo_functions as fun

# Load GAP cover associations
#GAP = pd.read_csv(fun.resultsDir + "GAP_spp_lc_cells.csv", header=0)

# Load WV cover associations
#WV = pd.read_csv(fun.resultsDir + "WV_spp_lc_detections.csv", header=0) 

# Load WV tally of records per cover type
#WV_tally = pd.read_csv(fun.dataDir + "LandCover/WV_habitat_entries.csv", header=0)

# Load land cover crosswalk
cross = pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv", 
                    header=0,
                    dtype={'GAP_code': str}) 

# Create a dictionary to store unmatchable WV cover types, from data sheets.
unmatched={}

# Which GAP cover types were sampled? HOW TO DO THAT??????????????????????????

# Return cover associations -------------------------------------------------------
GAP_types = fun.GAP_mapped_in(species)
GAP_types = [str(x) for x in GAP_types]
GAP_types = pd.DataFrame(index=GAP_types, columns=['GAP_associated'])
GAP_types['GAP_associated'] = 1
print("\nSystem associations in the GAP model")
print(GAP_types)

WVBBA_types = fun.WVBBA_detected_in(species)
WVBBA_types.index = [x.lower() for x in WVBBA_types.index]
#WVBBA_types = [fun.wv_lc_code_cleaner(code) for code in WVBBA_types]
#WVBBA_types = pd.DataFrame(index=WVBBA_types, columns=['WV'])
#WVBBA_types['WV'] = 1
print("\nWVBBA detections by WVBBA habitat type")
print(WVBBA_types)

# Which GAP types are linked to WVBBA associations? --------------------------
'''
Create a table with crosswalk info for the species
Rows for GAP types species was mapped in or detected in.
Column for confidence of cross walk (WV to GAP)
Column for number of GAP systems WV type was linked to
Column denoting whether GAP mapped species in type
Column for number of detections related to the type
'''
GAP_linked = pd.DataFrame()
GAP_linked.index.name="GAP_code"
sp_unmatched = {}
for code in WVBBA_types.index:
    detections = WVBBA_types.loc[code, 'detections']
    GAPs = (cross[lambda x: x['wv_code_fine'] == code]
             ['GAP_code']
             .unique())
    GAPs = [str(int(x)) for x in GAPs]
    match_n = len(GAPs)
    if match_n != 0:
        for gap in GAPs:
            confi = (cross[(cross['GAP_code'] == gap) &
                          (cross['wv_code_fine'] == code)]
                     ["confidence"]
                     .iloc[0])
            GAP_linked.loc[gap, 'cross_confidence'] = confi
            GAP_linked.loc[gap, 'cross_matches'] = match_n
            GAP_linked.loc[gap, 'detections'] = detections
    else:
        sp_unmatched[code] = detections
unmatched[species] = sp_unmatched

result_sp = (GAP_types.merge(GAP_linked, left_index=True, right_index=True, 
                       how='outer')
          .fillna(0))
result_sp.index.name = 'GAP_code'

# Calculate a measure of support for the link
result_sp["link_strength"] = result_sp["cross_confidence"]/result_sp["cross_matches"]
result_sp.fillna(0, inplace=True)


# Get names back in table ----------------------------------------------------
names = cross[['GAP_code', 'GAP_name']].drop_duplicates()
result_sp = result_sp.merge(names, right_on='GAP_code', left_on='GAP_code', how='inner')

# Categorize support ---------------------------------------------------------
support_categories = ['low', 'med', 'high']
bins = [0, 0.49, 0.80, 1]
support = pd.cut(result_sp['link_strength'], bins, labels=support_categories)
result_sp['support'] = support

# Evaluations ----------------------------------------------------------------
add = result_sp[(result_sp['support'] == 'high') &
                (result_sp['detections'] > 1) &
                (result_sp['GAP_associated'] == 0.0)]
result_sp.loc[result_sp.index.isin(add.index) == True, 'evaluation'] = 'add_association'

valid = result_sp[(result_sp['support'] == 'high') &
                (result_sp['detections'] > 1) &
                (result_sp['GAP_associated'] == 1.0)]
result_sp.loc[result_sp.index.isin(valid.index) == True, 'evaluation'] = 'valid'

GAP_n = len(GAP_types)
valid_n = len(result_sp[result_sp['evaluation'] == 'valid'])
print("{1} of {0} GAP ecological system associations were validated."
      "".format(GAP_n, valid_n))

# Show results ---------------------------------------------------------------
print("\nValidated associations")
df = result_sp[result_sp['evaluation'] == 'valid']
print(df[['GAP_code', 'GAP_name', 'detections']])

print("\nNew GAP ecological system associations that are supported by WVBBA:")
df = result_sp[result_sp['evaluation'] == 'add_association']
print(df[['GAP_code', 'GAP_name', 'detections']])

print("\nInvalid habitat codes entered by WVBBA observers:")
print(pd.DataFrame(unmatched))

# Report back results for usable detections!!!!!!!!!!!  START HERE MONDAY !!!!!
usable_df = pd.DataFrame(index=["Unusable", "Supported validation",
                                "Supported an addition", "Total detections"], 
                         columns=["detections"])

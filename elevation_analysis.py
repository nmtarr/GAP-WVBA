# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:13:10 2020

@author: nmtarr

Create summaries and figures of WVBBA elevation and GAP elevation match.
"""
import pandas as pd
import repo_functions as fun
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

# Elevation summary csv
eDF0 = pd.read_csv(fun.resultsDir + "elevation_summary.csv",
                   header=0, 
                   names=["GAP_code", "WVBBA_code", "common_name",
                          "map_max", "map_min", "SE_max", "SE_min", 
                          "NE_max", "NE_min", "WVBBA_max", "WVBBA_min",
                          "max_diff(%)", "min_diff(%)", "scientific_name",
                          "max_diff", "min_diff", "WVBBA_individuals(n)", 
                          "individuals_over(n)", "individuals_under(n)"])
#eDF0.replace(to_replace='NULL', value=np.nan, inplace=True) 
# Set a margin of error for elevation
elev_error = 75

##############################  MAXIMUM  #####################################
##############################################################################
##########  MAP
###################
# Which species were detected above max elevation from habitat maps?
df0 = eDF0[eDF0["individuals_over(n)"] > 0]
overMax = df0.filter(items=['GAP_code', 'common_name', 'individuals_over(n)', 
                            'WVBBA_max', 'map_max', 'max_diff', 'SE_max', 
                            'NE_max', 'WVBBA_individuals(n)'], 
                     axis=1)
''' 
Omit records with difference greater than the set "elev_error" bcs. count 
circles have range of elevations and gps precision, which creates reason to 
question a conflict bcs. elev is 'close' to gap max.
'''
overMax = overMax[overMax['max_diff'] > elev_error]

'''
If only a small percentage of the detected individuals conflict with the map,
then it's probably not appropriate to change the model, so filter out
species w/ <1% of individuals conflicting with the model'
'''
overMax['individuals_over(%)'] = 100*(overMax['individuals_over(n)']/overMax['WVBBA_individuals(n)'])
overMax.sort_values(by="individuals_over(n)", ascending=False, inplace=True)
overMax = overMax[overMax['individuals_over(%)'] > 1]

##########  MODEL
###################
# For which species was a model responsible and needs to be adjusted?
'''
If one of the model max's is NULL, then map output max wasn't necessarily
constrained by it, so exlude.  
'''
overMax2 = overMax.copy().dropna()
print("\n\nMax elevation needs to be adjusted in the models for these species")
print(overMax2)

# For which species was something other than a model responsible for the error?
overMax3 = overMax[overMax['GAP_code'].isin(overMax2['GAP_code']) == False]
print("\n\nSomething other than a max elevation parameter could be erroneously restricting map output to low elevations.")
print(overMax3)



##############################  MINIMUM  #####################################
##############################################################################
##########  MAP
###################
# Which species were detected below min elevation from habitat maps?
df1 = eDF0[eDF0["individuals_under(n)"] > 0]
overMin = df1.filter(items=['GAP_code', 'common_name', 'individuals_under(n)', 
                            'WVBBA_min', 'map_min', 'min_diff', 'SE_min', 
                            'NE_min', 'WVBBA_individuals(n)'], 
                     axis=1)
''' 
Omit records with difference greater than the set "elev_error" bcs. count 
circles have range of elevations and gps precision, which creates reason to 
question a conflict bcs. elev is 'close' to gap min.
'''
overMin = overMin[overMin['min_diff'] > elev_error]

'''
If only a small percentage of the detected individuals conflict with the map,
then it's probably not appropriate to change the model, so filter out
species w/ <1% of individuals conflicting with the model
'''
overMin['individuals_under(%)'] = 100*(overMin['individuals_under(n)']/overMin['WVBBA_individuals(n)'])
overMin.sort_values(by="individuals_under(n)", ascending=False, inplace=True)
overMin = overMin[overMin['individuals_under(%)'] > 1]

##########  MODEL
###################
# For which species was a model responsible and needs to be adjusted?
'''
If one of the model min's is NULL, then map output min wasn't necessarily
constrained by it, so exlude.  
'''
overMin2 = overMin.copy().dropna()
print("\n\nMin elevation needs to be adjusted in the models for these species")
print(overMin2)

# For which species was something other than a model responsible for the error?
overMin3 = overMin[overMin['GAP_code'].isin(overMin2['GAP_code']) == False]
print("\n\nSomething other than a min elevation parameter could be erroneously restricting map output to high elevations.")
print(overMin3)


#################  OBSOLETE ELEVATION PARAMETERS  ############################
##############################################################################
# For which species is max map elevation less than the max elevation parameter
misMax = eDF0.copy().filter(items=['GAP_code', 'common_name', 'map_max', 'SE_max', 
                            'NE_max'], axis=1)
misMax = misMax.dropna()
misMax2 = misMax[(misMax['map_max'] + 1 < misMax['SE_max']) & (misMax['map_max'] + 1 < misMax['NE_max'])]
print("\n\nThese species have obsolete maximum elevations for WV")
print(misMax2)

misMin = eDF0.copy().filter(items=['GAP_code', 'common_name', 'map_min', 'SE_min', 
                            'NE_min'], axis=1)
misMin = misMin.dropna()
misMin2 = misMin[(misMin['map_min'] - 1 > misMin['SE_min']) & (misMin['map_min'] - 1 > misMin['NE_min'])]
print("\n\nThese species have obsolete minimum elevations for WV")
print(misMin2)


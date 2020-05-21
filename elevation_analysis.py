# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:13:10 2020

@author: nmtarr

Create summaries and figures of WVBBA elevation and GAP elevation match.
"""
import pandas as pd
import repo_functions as fun
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

# Elevation summary csv
eDF0 = pd.read_csv(fun.resultsDir + "elevation_summary.csv",
                   header=0, 
                   names=["WVBBA_code", "GAP_code", "common_name",
                          "map_max", "map_min", "SE_max", "SE_min", 
                          "NE_max", "NE_min", "WVBBA_max", "WVBBA_min",
                          "max_diff(%)", "min_diff(%)", "scientific_name",
                          "max_diff", "min_diff", "WVBBA_individuals(n)", 
                          "individuals_over(n)", "individuals_under(n)"])

# Which species were detected above max elevation from habitat maps?
df0 = eDF0[eDF0["individuals_over(n)"] > 0]
overMax = df0.filter(items=['GAP_code', 'common_name', 'individuals_over(n)', 
                            'WVBBA_max', 'map_max', 'max_diff', 'SE_max', 
                            'NE_max', 'WVBBA_individuals(n)'], 
                     axis=1)
overMax.sort_values(by="individuals_over(n)", ascending=False, inplace=True)
print(overMax)

# Which had more than 1% of individuals above?

# For which and how many species did model max not equal map max?

# Which species were detected below min elevaiton from habitat maps?




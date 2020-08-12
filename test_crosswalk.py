# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:56:04 2020

@author: nmtarr
"""

import pandas as pd
import repo_functions as fun

# Load GAP cover associations
test = pd.read_csv(fun.dataDir + "LandCover/test_crosswalk.csv", header=0,
                   dtype={'X':str, 'Y':str, 'confidence':float, 
                          'X_area':int, 'Y_area':int})

# Add column: how many types linked to each type
X_count_Y = (test.groupby("Y").count().filter("X", axis=1)
             .rename(columns={'X':'X_matches'}))
Y_count_X = (test.groupby("X").count().filter("Y", axis=1)
            .rename(columns={'Y':'Y_matches'}))

# Merge datasets
test2 = pd.merge(test, X_count_Y, how='outer', left_on='Y', right_index=True)
test3 = pd.merge(test2, Y_count_X, how='outer', left_on='X', right_index=True)

# Compute evidence metric
test3['']
test3['XY_evidence'] = test3['confidence']/test3['Y_matches']
print(test3)
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:08:21 2020

@author: nmtarr
"""

import pandas as pd
import repo_functions as fun
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

# Load GAP cover associations
GAPlc0 = pd.read_csv(fun.resultsDir + "habitat_summary.csv", 
                     header=0)

# Load WV cover associations
WVlc0 = pd.read_csv(fun.resultsDir + "bbaHab_summary.csv", 
                     header=0) 

# Load land cover crosswalk
WVlc0 = pd.read_csv(fun.resultsDir + "ary.csv", 
                     header=0) 





# What habitat types were found in the counts, but not in lc?
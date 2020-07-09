# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:39:19 2020

@author: nmtarr
"""
import pandas as pd
import repo_functions as fun 
import numpy as np
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)

# Read in the spp crosswalk
crosswalk = pd.read_csv(fun.dataDir + "SpeciesLists/WV_GAP_Atlas.csv",
                            header=0,
                            names=["GAP_sci_name", "GAP_code",
                                   "common_name", "GAP_habitat(ha)",
                                   "WVBBA_sci_name", "WVBBA_individuals",
                                   "WVBBA_points", "WVBBA_rate"])


# Ebird pulled via rebird frequency 2011 to 2015 in WV
eBird =(pd.read_csv(fun.dataDir + "SpeciesLists/ebird_WV_2011_2015.csv")
        [lambda x: x['frequency'] > 0]
        [lambda x: x['comName'].str.contains(' sp.') == False]
        [lambda x: x['monthQt'].str.contains('May|June')]
        [lambda x: x['comName'].str.contains('hybrid') == False]
        [lambda x: x['comName'].str.contains('/') == False]
        .drop(['monthQt'], axis=1)
        .groupby('comName').mean()
        .drop(['sampleSize'], axis=1)
        .rename(columns={'frequency': 'eBird_mean_freq'})
        .reset_index()
        .sort_values(by=['eBird_mean_freq'], ascending=False))

# Merge the eBird, WV, and GAP lists
df = pd.merge(crosswalk, eBird, left_on='common_name', right_on='comName',
              how='outer')


# Which species were on the eBird and GAP list but not detected by WVBBA?
print(df[(df['WVBBA_individuals'].isnull() == True) & 
         (df['GAP_code'].isnull() == False) &
         (df['comName'].isnull() == False)
        ])

# Which species were submitted on the eBird list but not GAP or WVBBA?
print(df[(df['WVBBA_individuals'].isnull() == True) & 
         (df['GAP_code'].isnull() == True) &
         (df['comName'].isnull() == False)
        ])

# Which were on the GAP list but not eBird or WVBBA
print(df[(df['WVBBA_individuals'].isnull() == True) & 
         (df['GAP_code'].isnull() == False) &
         (df['comName'].isnull() == True)
        ])




'''
Results are A data frame containing the collected information. 

     "monthQt": month and week (eBird data divides each month by four
     weeks)

     "comName": species common name

     "frequency": proportion of times the species was seen in a
     specified week

     "sampleSize" number of complete eBird checklists submitted for
     specified given week @return If in wide format, then first column
     is the species list and all other columns are of individual weeks
     (four in each month). First row contains the number of complete
     checklists for each week.
'''

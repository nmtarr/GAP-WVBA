# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:05:33 2020

@author: nmtarr

Dev script for region-specific crosswalking.
"""
import pandas as pd
import repo_functions as fun

pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)


# SET SPECIES & REGION -------------------------------------------------------
sp_name = "Common Yellowthroat"
sp = fun.WVBBA_spp_code(sp_name)
region = "region1" # I think this may have to be done by region (looping)


# LOAD TABLES ----------------------------------------------------------------
# Land cover crosswalk
WV_cross = (pd.read_csv(fun.dataDir + "/LandCover/land_cover_crosswalk.csv")
            .drop(["wv_code_coarse", "wv_name_coarse", "confidence_notes",
                   "alexa_comments"], axis=1))

# GAP land cover type distribution across regions
GAPlc_region = (pd.read_csv(fun.dataDir + "GAPlc_by_region.csv"))

# Survey sites and detections; filter out non-target species records
detections = (pd.read_csv(fun.dataDir + "WV_spp_lc_site_detections.csv")
              [lambda x: x['species'] == sp]
              .filter(["US_L4CODE", "US_L3CODE", "NE_or_SE", "habitat",
                       "point_sum"], axis=1))

# ???? FILTER MORE HERE?  VERIFY NON DUPLICATES ETC.


# PROCESS CROSSWALK ----------------------------------------------------------
# Create empty set to collect results
linked_types = set([])






# RESULT ---------------------------------------------------------------------
print(linked_types)
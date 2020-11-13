# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:05:33 2020

@author: nmtarr

Dev script for region-specific crosswalking.  Relies on groupby-apply method.
Group by chunks detection table by region and a crosswalk function is then
applied to each chunk to do a region-specific crossalk.  
"""
import pandas as pd
import repo_functions as fun

pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 40)
pd.set_option('display.max_rows', 60)
pd.set_option('display.max_columns', 10)


# SET SPECIES & REGION -------------------------------------------------------
sp_name = "Common Yellowthroat"
sp = fun.WVBBA_sp_code(sp_name)

# LOAD TABLES ----------------------------------------------------------------
# Land cover crosswalk
WV_xwalk = (pd.read_csv(fun.dataDir + "/LandCover/land_cover_crosswalk.csv")
            .drop(["wv_code_coarse", "wv_name_coarse", "confidence_notes",
                   "alexa_comments", "wv_recorded"], axis=1))

# GAP land cover type distribution across regions
GAPlc_rgn = pd.read_csv(fun.dataDir + "GAPlc_by_region.csv")


# Merge crosswalk with GAP lc region table
xwalk_rgns = pd.merge(WV_xwalk, GAPlc_rgn, on="GAP_code", how="left")

# Survey sites and detections; filter out non-target species records
birds = (pd.read_csv(fun.dataDir + "WV_spp_lc_site_detections.csv")
              [lambda x: x['species'] == sp]
              .filter(["US_L4CODE", "US_L3CODE", "NE_or_SE", "habitat",
                       "point_sum"], axis=1)
              .rename({"NE_or_SE": "GAP_regions", "US_L3CODE":"Ecoregion3",
                       "US_L4CODE": "Ecoregion4"}, axis=1))

# ???? FILTER MORE HERE?  VERIFY NON DUPLICATES ETC.


# PREPARE TABLES -------------------------------------------------------------
'''
This step pulls out records with unmatcheable habitat types (at the state 
level).  More unmatcheble records may occur in the regional crosswalk.  
'''
# Detections could have wv codes that are unmatcheable, pull out
unmatcheable = (pd.merge(birds, WV_xwalk, how="left", left_on="habitat",
                         right_on="wv_code_fine")
                [lambda x: x["GAP_code"].isna() == True]
                .filter(["habitat", "point_sum", "wv_code_fine"]))

# Exclude unmatcheable records from detections
birds = birds[birds['habitat'].isin(unmatcheable['habitat']) == False]

# CREATE CROSSWALKING FUNCTION -----------------------------------------------
'''
A crosswalk function is defined so that it can be applied to each groupby 
group/chunk with .apply() when detections are grouped by region.  Detections 
records are then grouped by habitat within regions and summed/tallied.
'''

# The function is look for some variables - assign to dummies for now
regions=""
cutoff = 0.5

def xwalk_in_regions(df1):
    """
    Performs crosswalk of detections by habitat within regions.  Built for
    use in groupby.apply().
    
    Parameters
    ----------
    df1 : data frame
        A data frame of detection tallies by wv cover cover type (fine).
    regions : string
        Column name of the regions to use in crosswalk
    cutoff : float, optional
        Cutoff in percent of pixels used to assign a cover type to a 
        region. The default is 5.0.

    Returns
    -------
    df5 : data frame
        Result of the crosswalk by region.
    df6 : data frame
        
    """
    print(regions); print(cutoff)
    try:
        # Retrieve the region of the group.  Groupby object has regions as keys.
        rgn = df1[regions].unique()[0]
        #df1 = birds_sum[birds_sum[regions] == rgn]
        
        # Build a crosswalk for the region; exclude cover types from outside 
        # the region with a threshold for minimum percent of cover type in region.
        rgn_xwalk = (xwalk_rgns[xwalk_rgns[rgn] >= cutoff]
                     .filter(["GAP_code", "wv_code_fine",
                              "confidence"], axis=1))
        rgn_xwalk
        
        # Merge detections with lc crosswalk and drop non-matches
        df2 = pd.merge(rgn_xwalk, df1, how='right', right_on="habitat", 
                       left_on='wv_code_fine')
        
        print("------- UNMATCHABLE IN REGION ---------")
        print(df2[df2["GAP_code"].isna() == True])
        
        df3 = (df2[df2["GAP_code"].isna() == False]
               .drop(["habitat", regions], axis=1))
        
        # Determine number of links per system
        df4 = (df3[["GAP_code", "wv_code_fine"]]
               .groupby(["wv_code_fine"])
               .count()
               .reset_index()
               .rename({"GAP_code": "links"}, axis=1))
        
        # Add links column to df3
        df5 = (pd.merge(df3, df4, how="left", on="wv_code_fine")
               .rename({"point_sum": "detections"}, axis=1))
        
        # Calculate link strength
        df5["link_strength"] = df5["confidence"]/df5["links"]
        
        # Add column to document region type
        df5["regions"] = regions
            
        return df5
    except Exception as e:
        print(e)


# MODELING REGIONS CROSSWALKS ------------------------------------------------
regions="GAP_regions"
cutoff = 5.0
# ----------------------------------------------------------------------------
# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()
birds_sum

# Create grouped df based on region.
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_df1 = detections_gb.apply(xwalk_in_regions)

# Link strength could be different by region, take the max
out_df2 = (out_df1[["regions", "GAP_code", "detections", "link_strength"]]
           .groupby("GAP_code")
           .max())

# Categorize link strength as support
support_categories = ['low', 'med', 'high']
bins = [0, 0.49, 0.80, 1]
out_df2['support'] = pd.cut(out_df2['link_strength'], bins, 
                            labels=support_categories)
mod_region_output = out_df2

# LEVEL 3 ECOREGION CROSSWALKS -----------------------------------------------
regions="Ecoregion3"
cutoff = 5.0
# ----------------------------------------------------------------------------
# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()
birds_sum

# Create grouped df based on region.
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_df1 = detections_gb.apply(xwalk_in_regions)

# Link strength could be different by region, take the max
out_df2 = (out_df1[["regions", "GAP_code", "detections", "link_strength"]]
           .groupby("GAP_code")
           .max())

# Categorize link strength as support
support_categories = ['low', 'med', 'high']
bins = [0, 0.49, 0.80, 1]
out_df2['support'] = pd.cut(out_df2['link_strength'], bins, 
                            labels=support_categories)
eco3_output = out_df2

# LEVEL 4 ECOREGION CROSSWALKS -----------------------------------------------
regions="Ecoregion4"
cutoff = 5.0
# ----------------------------------------------------------------------------
# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()
birds_sum

# Create grouped df based on region.
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_df1 = detections_gb.apply(xwalk_in_regions)

# Link strength could be different by region, take the max
out_df2 = (out_df1[["regions", "GAP_code", "detections", "link_strength"]]
           .groupby("GAP_code")
           .max())

# Categorize link strength as support
support_categories = ['low', 'med', 'high']
bins = [0, 0.49, 0.80, 1]
out_df2['support'] = pd.cut(out_df2['link_strength'], bins, 
                            labels=support_categories)
eco4_output = out_df2


# RESULT ---------------------------------------------------------------------
out_df = pd.concat([mod_region_output, eco3_output, eco4_output])
print(out_df)
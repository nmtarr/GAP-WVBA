# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:05:33 2020

@author: nmtarr

Dev script for region-specific crosswalking.  Relies on groupby-apply method.
Group by chunks detection table by region and a crosswalk function is then
applied to each chunk to do a region-specific crossalk.  

Desired results:
    1. What codes unmatcheable at WV level; how many associated records
    2. What codes unmatcheable at regional level; what region-type combo and how many records?
    3. What gap types were linked to? what level of support? How many associated records?
    4. What gap types should be added?  Associated record count.
    5  What gap types were validated?  Associated record count.
    6. How many records met threshold for support, but outcompeted by higher support?    
    
"""
import pandas as pd
import repo_functions as fun

pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 40)
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 15)


# SET ARGUMENTS --------------------------------------------------------------
sp_name = "Common Yellowthroat"
sp = fun.WVBBA_sp_code(sp_name)
cutoff = 1.0 # Maximum percent of a cover types total acreage that can be in a 
#              region and it still be considered absent in the region. 
min_detections = 0
min_link = 0.49         

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

nbirds = birds.point_sum.sum()

# ???? FILTER MORE HERE?  VERIFY NON DUPLICATES ETC.


# PREPARE TABLES -------------------------------------------------------------
'''
This step pulls out records with unmatcheable habitat types (at the state 
level).  More unmatcheble records may occur in the regional crosswalk.  
'''
# Detections could have wv codes that are unmatcheable; pull them out
unmatcheable_0 = (pd.merge(birds, WV_xwalk, how="left", left_on="habitat",
                         right_on="wv_code_fine")
                  [lambda x: x["GAP_code"].isna() == True]
                  .filter(["habitat", "point_sum", "wv_code_fine"])
                  .groupby("habitat", as_index=False)
                  .sum()
                  .rename({"point_sum": "detections", 
                           "habitat": "recorded_habitat"}, axis=1))

# Exclude unmatcheable records from detections
birds = birds[birds['habitat'].isin(unmatcheable_0['recorded_habitat']) == False]

# CREATE RESULTS HOLDERS -----------------------------------------------------
'''
Below, groupby.apply() is used.  When output from the apply function is a 
single data frame, the results can be automatically concatenated.  Here,
the apply function generates multiple types of output that have to be collected
in some sort of rounabout way.  These tables get filled out as the function
is applied.
'''
unmatcheable_1 = unmatcheable_0.copy()
unmatcheable_1["region_type"] = "state"
unmatcheable_1["subregion"] = "WV"



# CREATE CROSSWALKING FUNCTION -----------------------------------------------
'''
A crosswalk function is defined so that it can be applied to each groupby 
group/chunk with .apply() when detections are grouped by region.  Detections 
records are then grouped by habitat within regions and summed/tallied.
'''

# The function will look for some variables - assign to dummies for now
regions=""

def xwalk_in_regions(df1, result):
    """
    Performs crosswalk of detections by habitat within regions.  Built for
    use in groupby.apply().
    
    Parameters
    ----------
    df1 : data frame
        A data frame of detection tallies by wv cover cover type (fine).

    Returns
    -------
    df5 : data frame
        Result of the crosswalk by region.   
        
    Needed:
        Total number of detections in each region.
        How many were unmatcheable.
        
    """
    try:
        # Retrieve the region of the group.  Groupby object has regions as keys.
        rgn = df1[regions].unique()[0]
        #df1 = birds_sum[birds_sum[regions] == rgn]
        
        # Build a crosswalk for the region; exclude cover types from outside 
        # the region with a threshold for minimum percent of cover type in
        # region.
        rgn_xwalk = (xwalk_rgns[xwalk_rgns[rgn] >= cutoff]
                     .filter(["GAP_code", "wv_code_fine",
                              "confidence"], axis=1))
        
        # WV -> GAP assessment -----------------------------------------------
        '''
        This section handles 1) one-to-one 2) one-to-none 3) one-to-many.
        '''
        # Merge detections with lc crosswalk and drop non-matches
        df2 = pd.merge(rgn_xwalk, df1, how='right', right_on="habitat", 
                       left_on='wv_code_fine')
        
        unmatcheable_10 = (df2[df2["GAP_code"].isna() == True]
                           .rename({"habitat": "recorded_habitat",
                                    "point_sum": "detections", 
                                    "GAP_regions": "subregion",
                                    "Ecoregion3": "subregion",
                                    "Ecoregion4": "subregion"}, axis=1)
                           .drop(["GAP_code", "wv_code_fine", 
                                  "confidence"], axis=1)
                           .reset_index(drop=True)
                           .rename({0: "subregion"}, axis=1)
                           )
        unmatcheable_10["region_type"] = regions
        
        # Move forward with matcheable records
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
        
        # GAP -> WV Assessment -----------------------------------------------
        '''
        Handling 1 GAP to many WV (many-to-one) requires assessing in the 
        other direction. This handles assessment of how many wv types linked 
        to a single GAP type have sufficient detections.
        Goal: what 
        '''
        # Merge detections with lc crosswalk ("left" this time)
        #print("detections merged with xwalk")
        df20 = (pd.merge(rgn_xwalk, df1, how='left', right_on="habitat", 
                        left_on='wv_code_fine'))
        
        # Get a df with # wv types linked to each GAP type in region
        # Also filter out GAP codes with 1 corresponding wv type; those are 
        # handled above.
        df21 = (df20
                .filter(["GAP_code", "habitat"], axis=1)
                .groupby("GAP_code", as_index=False)
                .count()
                .rename({"habitat": "wv_type_count"}, axis=1)
                [lambda x: x['wv_type_count'] > 1]
                )
        #print(df21)
        # Get a df with # wv types with enough detections linked to each GAP
        df22 = (df20
                [lambda x: x["point_sum"] > min_detections]
                .filter(["GAP_code", "habitat"], axis=1)
                .groupby("GAP_code", as_index=False)
                .count()
                .rename({"habitat": "wv_sufficient_count"}, axis=1)
                )
        
        # Merge df's with count of potential links and count of sufficient
        # links
        df23 = pd.merge(df22, df21, how="right", on="GAP_code")
        df23["proportion_sufficient"] = df23.wv_sufficient_count/df23.wv_type_count
        
        # Get confidence and detections into the df
        df24 = (pd.merge(df23, rgn_xwalk, how="left", on="GAP_code")
                )
        
        # Get detections (point_sum) into df
        df25 = (pd.merge(df24, df3, how="left", on=["wv_code_fine",
                                                    "GAP_code", "confidence"])
                [lambda x: x["point_sum"].isna() == False]
                .rename({"point_sum": "detections"}, axis=1)
                )
        df25["link_strength"] = df25["confidence"] * df25["proportion_sufficient"]
        
        # Combine the two result df (at this point) for further processing
        #    remove records with insufficient link_strength
        df30 = (pd.concat([df25[["GAP_code", "wv_code_fine", "link_strength",
                                 "detections"]],
                         df5[["GAP_code", "wv_code_fine", "link_strength",
                              "detections"]]])
                [lambda x: x["link_strength"] > min_link]
                .drop(["link_strength"], axis=1)
                )
        
        # Get a list of supported GAP_codes
        supported_GAP_codes = (pd.DataFrame(df30["GAP_code"])
                               .drop_duplicates()
                               .reset_index(drop=True))
        supported_GAP_codes["region_type"] = regions
        supported_GAP_codes["subregion"] = rgn
                
        # Get table of wv codes, detection # that were supported
        tally = (df30[["wv_code_fine", "detections"]]
                 .drop_duplicates()
                 .reset_index(drop=True)
                 )
        tally["region_type"] = regions
        tally["subregion"] = rgn
        
        
        if result == "nonmatches":
            return unmatcheable_10
        if result == "GAP_types":
            return supported_GAP_codes
        if result == "record_count":
            return tally
    
    except Exception as e:
        print(e)


# MODELING REGIONS CROSSWALKS ------------------------------------------------
regions="GAP_regions"

# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()

# Create grouped df based on region (create chunks based on region)
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_1 = (detections_gb.apply(xwalk_in_regions, result="GAP_types")
             .reset_index(drop=True)
             )
out_2 = (detections_gb.apply(xwalk_in_regions, result="record_count")
             .reset_index(drop=True)
             )
out_3 = (detections_gb.apply(xwalk_in_regions, result="nonmatches")
             .reset_index(drop=True)
             )


# LEVEL 3 ECOREGION CROSSWALKS -----------------------------------------------
regions="Ecoregion3"

# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()

# Create grouped df based on region (create chunks based on region)
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_4 = (detections_gb.apply(xwalk_in_regions, result="GAP_types")
             .reset_index(drop=True)
             )
out_5 = (detections_gb.apply(xwalk_in_regions, result="record_count")
             .reset_index(drop=True)
             )
out_6 = (detections_gb.apply(xwalk_in_regions, result="nonmatches")
             .reset_index(drop=True)
             )


# LEVEL 4 ECOREGION CROSSWALKS -----------------------------------------------
regions="Ecoregion4"

# Tally number of detections by region and habitat type
birds_sum = birds.groupby([regions, "habitat"]).sum().reset_index()

# Create grouped df based on region (create chunks based on region)
detections_gb = birds_sum.groupby([regions], as_index=False)

# Apply crosswalk function to groups
out_7 = (detections_gb.apply(xwalk_in_regions, result="GAP_types")
             .reset_index(drop=True)
             )
out_8 = (detections_gb.apply(xwalk_in_regions, result="record_count")
             .reset_index(drop=True)
             )
out_9 = (detections_gb.apply(xwalk_in_regions, result="nonmatches")
             .reset_index(drop=True)
             )


# QUESTIONS ------------------------------------------------------------------
# Choose the row with highest support -- how to adjust counts????????!!!!!!!!!!!!!
#df11 = df10.groupby(["GAP_code"], as_index=False).max()

# # Categorize link strength as support
# bins = [0, 0.49, 0.80, 1]
# df11['support'] = pd.cut(df11['link_strength'], bins, 
#                             labels=['low', 'med', 'high'])

# Filter out low or low and medium support
####    RESUME WORK HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Find validations

# Find additions

# How many records were useful? - sum of validations and additions?

# RESULTS --------------------------------------------------------------------

# Which unmatcheable codes were present
print("\tUnmatcheable")
print(pd.concat([unmatcheable_1, out_3, out_6, out_9]))

# GAP types supported
print("\tSupported GAP types")
print(pd.concat([out_1, out_4, out_7]))

# Tallies of usable records
print("\tTallies of usable records")
print(pd.concat([out_2, out_5, out_8]))




# How many total detections
print(nbirds)

# How many supported addition, supported validation, unusable

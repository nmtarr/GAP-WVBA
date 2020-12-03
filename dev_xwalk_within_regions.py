# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:05:33 2020

@author: nmtarr

Dev script for region-specific crosswalking.  Relies on groupby-apply method.
Group by chunks detection table by region and a crosswalk function is then
applied to each chunk to do a region-specific crossalk.  
    
"""
import repo_functions as fun

# DEFINE FUNCTION ------------------------------------------------------------
def regional_xwalk(sp_name, cutoff_lc, min_detections, min_link, support_bins,
                   print_tables=True):
    """
    Parameters
    ----------
    sp_name : string
        Like "Acadian Flycatcher".
    cutoff_lc : float
        Maximum percent of a cover types total acreage that can be in a 
        region and it still be considered absent in the region.
    min_detections : integer
        Cutoff in minimum number of detections for a cover type in order for
        the records to be included in the assessment.
    min_link : float
        Cutoff in link strength below which the link is insufficient for 
        validation or addition of GAP types in the GAP model.  For one-to-many
        links, link strength is confidence/number of links (many).  For 
        many-to-one, link strength is the proportion of "many"s with sufficient
        numbers of detections (> min_detections) multiplied by confidence.
    support_bins : list
        Breakpoints for reclassifying link strength as "low", "medium", or 
        "high".
    print_tables : boolean, optional
        Should the results be printed. The default is True.

    Returns
    -------
    evaluations : data frame
        Rows for GAP cover types from GAP habitat model and results of 
        evaluations based on WVBBA data: validated, unvalidated, or potential
        additions.
    totals : data frame
        Detection totals for USABLE region-cover type combinations.
    nonmatches : data frame
        WV habitat types that couldn't be matched within some subregions.
    nbirds : integer
        The total number of detections for the species.
    """
    try:
        import pandas as pd
        pd.set_option('display.width', 2000)
        pd.set_option('display.max_colwidth', 40)
        pd.set_option('display.max_rows', 300)
        pd.set_option('display.max_columns', 15)
        
        
        # SPECIES NAME -----------------------------------------------------------
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
        
        nbirds = birds.point_sum.sum()
        
        # ???? FILTER MORE HERE?  VERIFY NON DUPLICATES ETC.??????????????????????????
        
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
        
        # Add columns for regional info
        unmatcheable_0["region_type"] = "State"
        unmatcheable_0["subregion"] = "WV"
        
        # Exclude unmatcheable records from detections
        birds = birds[birds['habitat'].isin(unmatcheable_0['recorded_habitat']) == False]
        
        
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
            df1 : dataframe chunk
                From groupby of table with detections.
            result : string
                Choose from one of three options: "nonmatches", "GAP_types", "record_count".
        
            Returns
            -------
            data frame
                Depending on the result argument, it generates one of 3 table types.
        
            """
            try:
                # Retrieve the region of the group.  Groupby object has regions as keys.
                rgn = df1[regions].unique()[0]
                
                # Build a crosswalk for the region; exclude cover types from outside 
                # the region with a threshold for minimum percent of cover type in
                # region.
                rgn_xwalk = (xwalk_rgns[xwalk_rgns[rgn] >= cutoff_lc]
                             .filter(["GAP_code", "wv_code_fine",
                                      "confidence"], axis=1))
                
                # 1) ONE-TO-ONE 2) ONE-TO-NONE 3) ONE-TO-MANY ------------------------
                # Merge detections with lc crosswalk and drop/find non-matches
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
                unmatcheable_result = unmatcheable_10
                
                # Move forward with matcheable records
                df3 = (df2[df2["GAP_code"].isna() == False]
                       .drop(["habitat", regions], axis=1)
                       )
                
                # Determine number of links per system
                df4 = (df3[["GAP_code", "wv_code_fine"]]
                       .groupby(["wv_code_fine"])
                       .count()
                       .reset_index()
                       .rename({"GAP_code": "links"}, axis=1)
                       )
                
                # Add links column to df3
                df5 = (pd.merge(df3, df4, how="left", on="wv_code_fine")
                       .rename({"point_sum": "detections"}, axis=1)
                       )
                
                # Calculate link strength
                df5["link_strength"] = df5["confidence"]/df5["links"]
                
                # Add column to document region type
                df5["regions"] = regions
                 
            
                # MANY-TO-ONE --------------------------------------------------------
                '''
                Handling 1 GAP to many WV (many-to-one) requires assessing in the 
                other direction. This handles assessment of how many wv types linked 
                to a single GAP type.
                '''
                # Merge detections with lc crosswalk (how="left" this time)
                df20 = pd.merge(rgn_xwalk, df1, how='left', right_on="habitat", 
                                 left_on='wv_code_fine')
                
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
               
                # Get a df with # wv types with enough detections linked to each GAP
                df22 = (df20
                        [lambda x: x["point_sum"] > min_detections]
                        .filter(["GAP_code", "habitat"], axis=1)
                        .groupby("GAP_code", as_index=False)
                        .count()
                        .rename({"habitat": "wv_sufficient_count"}, axis=1)
                        )
                
                # Merge df's with counts of potential and sufficient links
                df23 = pd.merge(df22, df21, how="right", on="GAP_code")
                df23["proportion_sufficient"] = df23.wv_sufficient_count/df23.wv_type_count
                
                # Get confidence and detections into the df
                df24 = pd.merge(df23, rgn_xwalk, how="left", on="GAP_code")
                
                # Get detections (point_sum) into the df
                df25 = (pd.merge(df24, df3, how="left", on=["wv_code_fine",
                                                            "GAP_code", "confidence"])
                        [lambda x: x["point_sum"].isna() == False]
                        .rename({"point_sum": "detections"}, axis=1)
                        )
                df25["link_strength"] = df25["confidence"] * df25["proportion_sufficient"]
                
                # Combine the two result df (at this point) for further processing
                #    remove records with insufficient link_strength
                aaa = df25[["GAP_code", "wv_code_fine", "link_strength", "detections"]]
                bbb = df5[["GAP_code", "wv_code_fine", "link_strength", "detections"]]
                df30 = (pd.concat([aaa, bbb])
                        [lambda x: x["link_strength"] > min_link]
                        )
                
                # Get a list of supported GAP_codes
                supported_GAP_codes = (df30[["GAP_code", "link_strength"]]
                                       .drop_duplicates()
                                       .reset_index(drop=True))
                supported_GAP_codes["region_type"] = regions
                supported_GAP_codes["subregion"] = rgn
                        
                # Get table of wv codes, detection number that were supported
                tally = (df30[["wv_code_fine", "detections"]]
                         .drop_duplicates()
                         .reset_index(drop=True)
                         )
                tally["region_type"] = regions
                tally["subregion"] = rgn
                
                if result == "nonmatches":
                    return unmatcheable_result
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
        
        
        # XWALK CALLS ----------------------------------------------------------------
        # Which unmatcheable codes were present
        nonmatches = (pd.concat([unmatcheable_0, out_3, out_6, out_9])
                      [["region_type", "subregion", "recorded_habitat", "detections"]]
                      )
        
        # GAP types supported
        supported_GAP_types = (pd.concat([out_1, out_4, out_7])
                               [["region_type", "subregion", "GAP_code", 
                                 "link_strength"]]
                               )
        
        # Categorize support; use bins from above/argument
        support_categ = ['low', 'med', 'high']
        support = pd.cut(supported_GAP_types['link_strength'], support_bins, 
                         labels=support_categ)
        supported_GAP_types['support'] = support
        
        # Tallies of usable records
        totals = (pd.concat([out_2, out_5, out_8])
                  [["region_type", "subregion", "wv_code_fine", "detections"]]
                  )
        
        
        # COMPARISON TO GAP MODEL ----------------------------------------------------
        # Return cover associations 
        GAP_types = fun.GAP_mapped_in(sp_name)
        GAP_types = pd.DataFrame(index=GAP_types, columns=['GAP_associated'])
        GAP_types.index.name = "GAP_code"
        GAP_types.reset_index(drop=False, inplace=True)
        GAP_types['GAP_associated'] = 1
        GAP_types2 = (GAP_types
                      .merge(WV_xwalk, left_on='GAP_code', right_on='GAP_code', 
                             how='inner')
                      .set_index(['GAP_code'])
                      [['GAP_name']]
                      .drop_duplicates()
                      )
        
        
        # EVALUATIONS ----------------------------------------------------------------
        # Merge with supported types to prep for finding validations and additions
        GAP_comp0 = pd.merge(GAP_types, supported_GAP_types, how="outer", 
                             left_on="GAP_code", right_on="GAP_code")
        GAP_comp0["GAP_associated"].fillna(0, inplace=True)
        GAP_comp0["evaluation"] = ""
        
        # Additions
        add = GAP_comp0[(GAP_comp0['link_strength'].isnull() == False) &
                        (GAP_comp0['GAP_associated'] == 0.0)]
        GAP_comp0.loc[GAP_comp0.index.isin(add.index) == True, 
                      'evaluation'] = 'add_association'
        
        # Validations
        valid = GAP_comp0[(GAP_comp0['link_strength'].isnull() == False) &
                          (GAP_comp0['GAP_associated'] == 1.0)]
        GAP_comp0.loc[GAP_comp0.index.isin(valid.index) == True, 
                      'evaluation'] = 'validated'
        
        # Unvalidated
        nonvalidated = GAP_comp0[(GAP_comp0['link_strength'].isnull() == True) &
                                 (GAP_comp0['GAP_associated'] == 1.0)]
        GAP_comp0.loc[GAP_comp0.index.isin(nonvalidated.index) == True, 
                      'evaluation'] = 'unvalidated'

        # Report result
        evaluations = (GAP_comp0
                       .merge(GAP_types2, left_on='GAP_code', right_on='GAP_code', 
                              how='left')
                       .filter(["GAP_code", "evaluation", "support"], 
                               axis=1)
                       .drop_duplicates()
                       )
        
        # Bring in names
        names = WV_xwalk[["GAP_code", "GAP_name"]]
        evaluations = (pd.merge(evaluations, names, how="left", on="GAP_code")
                       .drop_duplicates()
                       [["GAP_code", "GAP_name", "evaluation", "support"]]
                       )
        
        # RETURN RESULTS -------------------------------------------------------------
        if print_tables == True:
            print("\n\nEvaluations")
            print(evaluations)
            print("\n\nTotals")
            print(totals)
            print("\n\nNonmatches")
            print(nonmatches)
        
        return evaluations, totals, nonmatches, nbirds
    
    except Exception as e:
        print(e)
        
# RUN IT ---------------------------------------------------------------------
a, b, c, d = regional_xwalk(sp_name="American Robin", cutoff_lc=1.0, 
                   min_detections=1, min_link=0.49, 
                   support_bins=[0, 0.49, 0.80, 1],
                   print_tables=True)
projDir = "P:/Proj6/USGAP-WVBBA/"
dataDir = projDir + "Data/"
rangDir = projDir + "Temp/"
resultsDir = projDir + "Results/"
clipDir = dataDir + 'habmaps'
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'

import pandas as pd
import numpy as np
'''
WV_pc_site = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="all data")
WV_pc_site_spp = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="HABDATA_for_newCHART")
WV_hab_labels = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="Habitat type")
WV_cap_spp = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="CAPTIONS")
'''

def wv_lc_code_cleaner(code):
        code = code.lower().replace('"', '')
        return code

def WVBBA_sp_code(name):
    '''
    Return the WV atlas species code for the common name provided.
    '''
    code = (pd.read_csv(dataDir + "/SpeciesLists/WV_GAP_Atlas3.csv", header=0)
            [lambda x: x['common_name'] == name]
            ['WV_code']
            .iloc[0])
    return code

def GAP_spp_code(name):
    '''
    Return the GAP species code for the common name provided.
    '''
    code = (pd.read_csv(dataDir + "/SpeciesLists/WV_GAP_Atlas3.csv", header=0)
            [lambda x: x['common_name'] == name]
            ['strUC']
            .iloc[0])
    code = code[0] + code[1:5].upper() + code[5]
    return code

def WVBBA_sp_code(name):
    '''
    Return the WV atlas species code for the common name provided.
    '''
    code = (pd.read_csv(dataDir + "/SpeciesLists/WV_GAP_Atlas3.csv", header=0)
            [lambda x: x['common_name'] == name]
            ['WV_code']
            .iloc[0])
    return code

def WVBBA_detected_in(species):
    '''
    Returns list of cover types WVBBA found species in.
    '''
    WV = pd.read_csv(resultsDir + "WV_spp_lc_detections.csv", header=0)
    WV.rename({'3A' : '3', '4A' : '4', '8A' : '8', '7C' : '7', '13A' : '13', 
           '16D' : '16', '18D' : '18','1"': '1', '1LA' : '1',
           '1"U': '1', '1LB': '1', '1B' : '1', '1M' : '1', '10A' : '10'}, axis=1, inplace=True)
    WV = WV.groupby(WV.columns, axis=1).sum()
    WV.replace(0,np.nan, inplace=True)

    spp = GAP_spp_code(species)
    WV_types = (WV
            [lambda x: x['species'] == spp[1:5]]
            .T)

    WV_types = (WV_types.rename(columns={WV_types.columns[0]: 'detections'})
           .iloc[:-1]
            [lambda x: x['detections'] > 0])
    return WV_types

def GAP_mapped_in(species):
    '''
    Returns list of GAP land cover class codes species was mapped in.
    Format species like "Acadian Flycatcher"
    '''
    spp = GAP_spp_code(species)
    GAP = pd.read_csv(resultsDir + "GAP_spp_lc_cells.csv", header=0)
    GAP_types = (GAP
                 [lambda x: x['GAP_sp_code'] == spp]
                 ['GAP_lc_code']
                 .pipe(list))
    return GAP_types

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
        sp = WVBBA_sp_code(sp_name)
        
        
        # LOAD TABLES ----------------------------------------------------------------
        # Land cover crosswalk
        WV_xwalk = (pd.read_csv(dataDir + "/LandCover/land_cover_crosswalk.csv")
                    .drop(["wv_code_coarse", "wv_name_coarse", "confidence_notes",
                           "alexa_comments", "wv_recorded"], axis=1))
        
        # GAP land cover type distribution across regions
        GAPlc_rgn = pd.read_csv(dataDir + "GAPlc_by_region.csv")
        
        # Merge crosswalk with GAP lc region table
        xwalk_rgns = pd.merge(WV_xwalk, GAPlc_rgn, on="GAP_code", how="left")
        
        # Survey sites and detections; filter out non-target species records
        birds = (pd.read_csv(dataDir + "WV_spp_lc_site_detections.csv")
                 .replace({"habitat": {'3A' : '3', '4A' : '4', '8A' : '8', 
                                       '7C' : '7', '13A' : '13', '16D' : '16',
                                       '18D' : '18','1"': '1', '1LA' : '1',
                                       '1"U': '1', '1LB': '1', '1B' : '1', 
                                       '1M' : '1', '10A' : '10'}})
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
                 
            
                # # MANY-TO-ONE --------------------------------------------------------
                # '''
                # REMOVE??????????????????????????????????????????????????????????????
                # Handling 1 GAP to many WV (many-to-one) requires assessing in the 
                # other direction. This handles assessment of how many wv types linked 
                # to a single GAP type.
                # '''
                # # Merge detections with lc crosswalk (how="left" this time)
                # df20 = pd.merge(rgn_xwalk, df1, how='left', right_on="habitat", 
                #                  left_on='wv_code_fine')
                
                # # Get a df with # wv types linked to each GAP type in region
                # # Also filter out GAP codes with 1 corresponding wv type; those are 
                # # handled above.
                # df21 = (df20
                #         .filter(["GAP_code", "habitat"], axis=1)
                #         .groupby("GAP_code", as_index=False)
                #         .count()
                #         .rename({"habitat": "wv_type_count"}, axis=1)
                #         [lambda x: x['wv_type_count'] > 1]
                #         )
               
                # # Get a df with # wv types with enough detections linked to each GAP
                # df22 = (df20
                #         [lambda x: x["point_sum"] > min_detections]
                #         .filter(["GAP_code", "habitat"], axis=1)
                #         .groupby("GAP_code", as_index=False)
                #         .count()
                #         .rename({"habitat": "wv_sufficient_count"}, axis=1)
                #         )
                
                # # Merge df's with counts of potential and sufficient links
                # df23 = pd.merge(df22, df21, how="right", on="GAP_code")
                # df23["proportion_sufficient"] = df23.wv_sufficient_count/df23.wv_type_count
                
                # # Get confidence and detections into the df
                # df24 = pd.merge(df23, rgn_xwalk, how="left", on="GAP_code")
                
                # # Get detections (point_sum) into the df
                # df25 = (pd.merge(df24, df3, how="left", on=["wv_code_fine",
                #                                             "GAP_code", "confidence"])
                #         [lambda x: x["point_sum"].isna() == False]
                #         .rename({"point_sum": "detections"}, axis=1)
                #         )
                # df25["link_strength"] = df25["confidence"] * df25["proportion_sufficient"]
                # #  REMOVE above???????????????????????????????????????????????????????????
                # # Combine the two result df (at this point) for further processing
                # #    remove records with insufficient link_strength
                # aaa = df25[["GAP_code", "wv_code_fine", "link_strength", "detections"]]
                # bbb = df5[["GAP_code", "wv_code_fine", "link_strength", "detections"]]
                # df30 = (pd.concat([aaa, bbb])
                #         [lambda x: x["link_strength"] > min_link]
                #         )
                
                # Remove records with insufficient link strength
                df30 = df5[df5["link_strength"] > min_link]
                
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
        GAP_types = GAP_mapped_in(sp_name)
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
        
        
def cross_to_GAP(species, crosswalk, print_tables=True):
    '''
    Gathers and matches WVBBA cover type associations to GAP types, assesses
    support for GAP associations in WVBBA data.
    '''
    # Return cover associations -------------------------------------------------------
    GAP_types = GAP_mapped_in(species)
    GAP_types = [str(x) for x in GAP_types]
    GAP_types = pd.DataFrame(index=GAP_types, columns=['GAP_associated'])
    GAP_types['GAP_associated'] = 1
    if print_tables == True:
        print("\nSystem associations in the GAP model")
        print(GAP_types
              .merge(crosswalk, left_index=True, right_on='GAP_code', 
                     how='inner')
              [['GAP_code', 'GAP_name', 'GAP_associated']]
              .set_index(['GAP_code'])
              [['GAP_name']]
              .drop_duplicates()
              )

    WVBBA_types = WVBBA_detected_in(species)
    WVBBA_types.index = [x.lower() for x in WVBBA_types.index]
    if print_tables == True:
        print("\nWVBBA detections by WVBBA habitat type")
        print(WVBBA_types
              .merge(crosswalk, left_index=True, right_on='wv_code_fine', 
                     how='inner')
              [['wv_code_fine', 'wv_name_fine', 'detections']]
              .set_index(['wv_code_fine'])
              .drop_duplicates())
        
        
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
        GAPs = (crosswalk[lambda x: x['wv_code_fine'] == code]
                ['GAP_code']
                .unique())
        GAPs = [str(int(x)) for x in GAPs]
        match_n = len(GAPs)
        if match_n != 0:
            for gap in GAPs:
                confi = (crosswalk[(crosswalk['GAP_code'] == gap) &
                        (crosswalk['wv_code_fine'] == code)]
                         ["confidence"]
                         .iloc[0])
                name = (crosswalk[crosswalk['wv_code_fine'] == code]['wv_name_fine']
                       .unique()[0])
                GAP_linked.loc[gap, 'cross_confidence'] = confi
                GAP_linked.loc[gap, 'cross_matches'] = match_n
                GAP_linked.loc[gap, 'detections'] = detections
                GAP_linked.loc[gap, 'wv_code_fine'] = code
                GAP_linked.loc[gap, 'wv_name_fine'] = name
        else:
            sp_unmatched[code] = detections

    result_sp = (GAP_types.merge(GAP_linked, left_index=True, 
                                 right_index=True, how='outer')
                 .fillna(0))
    result_sp.index.name = 'GAP_code'
    
    
    # Calculate a measure of support for the link -----------------------------
    result_sp["link_strength"] = result_sp["cross_confidence"]/result_sp["cross_matches"]
    result_sp.fillna(0, inplace=True)


    # Get names back in table ----------------------------------------------------
    names = crosswalk[['GAP_code', 'GAP_name']].drop_duplicates()
    result_sp = result_sp.merge(names, right_on='GAP_code', 
                                left_on='GAP_code', how='inner')


    # Categorize support ---------------------------------------------------------
    support_categories = ['low', 'med', 'high']
    bins = [0, 0.49, 0.80, 1]
    support = pd.cut(result_sp['link_strength'], bins, 
                     labels=support_categories)
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
    if print_tables == True:
        print("{1} of {0} GAP ecological system associations were validated."
              "".format(GAP_n, valid_n))

    # Deal with wv codes not matchable to GAP types
    GAPnan = (result_sp[result_sp['GAP_code'] == '0']
              .set_index(['wv_code_fine']))

    # Pull out unmatched systems
    result_sp = result_sp[result_sp['GAP_code'] != '0']
    for nan in GAPnan.index:
        sp_unmatched[nan] = GAPnan.loc[nan, 'detections']

    return result_sp, GAP_linked, sp_unmatched, GAP_types, WVBBA_types


def download_GAP_range_CONUS2001v1(gap_id, toDir):
    """
    Downloads GAP Range CONUS 2001 v1 file and returns path to the unzipped
    file.  NOTE: doesn't include extension in returned path so that you can
    specify if you want csv or shp or xml when you use the path.
    """
    import sciencebasepy
    import zipfile

    # Connect
    sb = sciencebasepy.SbSession()

    # Search for gap range item in ScienceBase
    gap_id = gap_id[0] + gap_id[1:5].upper() + gap_id[5]
    item_search = '{0}_CONUS_2001v1 Range Map'.format(gap_id)
    items = sb.find_items_by_any_text(item_search)

    # Get a public item.  No need to log in.
    rng =  items['items'][0]['id']
    item_json = sb.get_item(rng)
    get_files = sb.get_item_files(item_json, toDir)

    # Unzip
    rng_zip = toDir + item_json['files'][0]['name']
    zip_ref = zipfile.ZipFile(rng_zip, 'r')
    zip_ref.extractall(toDir)
    zip_ref.close()

    # Return path to range file without extension
    return rng_zip.replace('.zip', '')


def download_GAP_model_CONUS2001v1(gap_id, toDir):
    """
    Gets GAP habitat models as JSONs.  Pulls out summer NE and SE.  
    Returns a list of dictionaries.
    """
    import sciencebasepy
    import json
    
    # Connect
    sb = sciencebasepy.SbSession()
    
    # Search for gap range item in ScienceBase
    gap_id = gap_id[0] + gap_id[1:5].upper() + gap_id[5]
    item_search = '{0}_CONUS_HabModel_2001v1.json'.format(gap_id)
    items = sb.find_items_by_any_text(item_search)
    
    # Get a public item.  No need to log in.
    mod =  items['items'][0]['id']
    item_json = sb.get_item(mod)
    get_files = sb.get_item_files(item_json, toDir)
    
    # Read in json file
    models = json.load(open(toDir + gap_id + "_CONUS_HabModel_2001v1.json"))
    models = [models["models"][gap_id + "-s6"], models["models"][gap_id + "-s3"]]
    
    if models[0]['ysnHandModel'] == True or models[1]['ysnHandModel'] == True:
        print('handmodel')
    else:
        return models
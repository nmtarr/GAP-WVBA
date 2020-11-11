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
              .merge(crosswalk, left_index=True, right_on='GAP_code', how='inner')
              [['GAP_code', 'GAP_name', 'GAP_associated']]
              .set_index(['GAP_code'])
              [['GAP_name']]
              .drop_duplicates())

    WVBBA_types = WVBBA_detected_in(species)
    WVBBA_types.index = [x.lower() for x in WVBBA_types.index]
    if print_tables == True:
        print("\nWVBBA detections by WVBBA habitat type")
        print(WVBBA_types
              .merge(crosswalk, left_index=True, right_on='wv_code_fine', how='inner')
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

    result_sp = (GAP_types.merge(GAP_linked, left_index=True, right_index=True,
                       how='outer')
          .fillna(0))
    result_sp.index.name = 'GAP_code'
    
    
    # Calculate a measure of support for the link -----------------------------
    result_sp["link_strength"] = result_sp["cross_confidence"]/result_sp["cross_matches"]
    result_sp.fillna(0, inplace=True)


    # Get names back in table ----------------------------------------------------
    names = crosswalk[['GAP_code', 'GAP_name']].drop_duplicates()
    result_sp = result_sp.merge(names, right_on='GAP_code', left_on='GAP_code',
                                how='inner')


    # Categorize support ---------------------------------------------------------
    support_categories = ['low', 'med', 'high']
    bins = [0, 0.49, 0.80, 1]
    support = pd.cut(result_sp['link_strength'], bins, labels=support_categories)
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
projDir = "P:/Proj6/USGAP-WVBBA/"
dataDir = projDir + "Data/"
rangDir = projDir + "Temp/"
resultsDir = projDir + "Results/"
clipDir = dataDir + 'habmaps'
listDir = dataDir + 'Specieslists/WV_AtlasCodes.csv'
wvBoundary = projDir + 'WV_GAPcover/2001/WVworkspace/wv_bound.shp'

import pandas as pd
WV_pc_site = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="all data")
WV_pc_site_spp = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="HABDATA_for_newCHART")
WV_hab_labels = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="Habitat type")

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


def lc_crosswalker(systems, fro, to):
    """
    Crosswalks a list of land cover classes from one classification to another.

    Arguments
    systems -- python list of system names
    from -- classification system of systems list
    to -- classification to crosswalk list to
    """
    #
    return out_systems

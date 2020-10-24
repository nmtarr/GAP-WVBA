# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 18:18:16 2020

@author: Jessica
"""

import pandas as pd
import numpy as np
import repo_functions as fun
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)

wvGAP = pd.read_csv(fun.dataDir + "LandCover/lcgapwv_2001_Clean.csv",
                    header=0, dtype={'LEVEL3': str},
                    usecols=["LEVEL3", "ECOLSYS_LU"])
wvGAP.rename(columns = {'LEVEL3':'GAP_code', "ECOLSYS_LU" : 'GAP_name'}, inplace = True)

# In[]
##Create table with percentage of each landcover type  in each L3 ecoregion 
wvLC = pd.read_csv(fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_L3.csv", 
                   dtype={'VALUE': str})
wvLC.rename(columns = {'VALUE':'GAP_code'}, inplace = True)
wvLC.drop(["OID"], axis=1, inplace=True)
wvLC['WV_Total'] = wvLC.sum(axis=1)
selLC = wvLC.filter(regex='^A_').div(wvLC['WV_Total'], 
                                     axis =0).apply(lambda x: 
                                                    x*100).round(2).set_index(wvLC['GAP_code'])
selLC.columns = selLC.columns.str.replace('[A_]', '')                                                    
mergeTab = pd.merge(left = wvGAP, right= selLC, how='outer', 
                    on=['GAP_code'],left_index=True)
mergeTab.to_csv(fun.dataDir + "RegionMatching/eco_crossL3.csv")

# In[]
##Create table with percentage of each landcover type  in each L4 ecoregion 
wvLC4 = pd.read_csv(fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_L4.csv", 
                   dtype={'VALUE': str})
wvLC4.rename(columns = {'VALUE':'GAP_code'}, inplace = True)
wvLC4.drop(["OID"], axis=1, inplace=True)
wvLC4['WV_Total'] = wvLC4.sum(axis=1)
selLC4 = wvLC4.filter(regex='^A_').div(wvLC4['WV_Total'], 
                                     axis =0).apply(lambda x:
                                                    x*100).round(2).set_index(wvLC4['GAP_code'])
selLC4.columns = selLC4.columns.str.replace('[A_]', '')   
mergeTab = pd.merge(left = wvGAP, right= selLC4, how='outer', 
                    on=['GAP_code'],left_index=True)
mergeTab.to_csv(fun.dataDir + "RegionMatching/eco_crossL4.csv")

# In[]
##Create table with percentage of each landcover type  in each GAP region
wvLCne = pd.read_csv(fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_ne.csv", 
                   dtype={'VALUE': str})
wvLCne.rename(columns = {'VALUE':'GAP_code', 'WEST_VIRGI': 'WV_NE'}, inplace = True)
wvLCne.drop(["OID"], axis=1, inplace=True)

mergeWV = pd.merge(left = wvGAP, right= wvLCne, how='outer', 
                    on=['GAP_code'],left_index=True)

wvLCse = pd.read_csv(fun.dataDir + "LandCover/WVworkspace/ecoclip/wvlc_se.csv", 
                   dtype={'VALUE': str})
wvLCse.rename(columns = {'VALUE':'GAP_code', 'WEST_VIRGI': 'WV_SE'}, inplace = True)
wvLCse.drop(["OID"], axis=1, inplace=True)
mergeWV = pd.merge(left = mergeWV, right= wvLCse, how='outer', 
                    on=['GAP_code'],left_index=True)
mergeWV['WVtotal'] = mergeWV.sum(axis=1)
selLCwv = mergeWV.filter(regex='^WV_').div(mergeWV['WVtotal'], 
                                     axis =0).apply(lambda x:
                                                    x*100).round(2).set_index(mergeWV['GAP_code'])
mergeTab2 = pd.merge(left = mergeWV[['GAP_code', 'GAP_name']], right= selLCwv, how='outer', 
                    on=['GAP_code'],left_index=True)
mergeTab2.fillna(value= 0, inplace = True)
mergeTab2.rename(columns = {'WV_SE' : 'SE', 'WV_NE' : 'NE'}, inplace = True)
mergeTab2.to_csv(fun.dataDir + "RegionMatching/lcGAP_bound.csv")

# In[]
##Clean up ArcGIS results of point data
pointsDF = pd.read_excel(fun.dataDir + "LandCover/WVworkspace/ecoclip/point_data.xls", 
                   dtype={'GRIDCODE': str})
pointsDF = pointsDF.drop(['FID','Join_Count','TARGET_FID'], axis=1)
pointsDF.rename(columns = {'block_poin' : 'block-point number', 
                          'GRIDCODE' : 'NE_or_SE'}, inplace = True)
pointsDF['NE_or_SE'].replace({'0': 'NE', '1': 'SE'}, inplace = True)
pointsDF.to_csv(fun.dataDir + "RegionMatching/WV_pc_site_spp.csv")


##Sum original point data and merge GIS output to pointdata (solves issue of dropped data)
###Currently raising the following error: KeyError: 'block-point number' (likely needs space removed)
WV_pc_site_spp = pd.read_excel(fun.dataDir + "WVBBA_DATA.xlsx", sheet_name="HABDATA_for_newCHART")
resultsCSV = fun.dataDir + "RegionMatching/WV_spp_lc_site_detections.csv"
resultsCSV2 = fun.dataDir + "RegionMatching/WVspp_lc_site_detect_stack.csv"


fillCols = {'0-<50m:0-3 min' : '0', '0-<50m:>3-5 min': '0', 
            '0-<50m:>5-10min': '0', 
             '50-100m:0-3min': '0', '50-100m:>3-5min': '0', 
             '50-100m:>5-10min': '0', 
             '≥100m or flyover:0-3min': '0', '≥100m or flyover:>3-5min': '0', 
             '≥100m or flyover:>5-10min': '0'}
pointList = WV_pc_site_spp[{'0-<50m:0-3 min','0-<50m:>3-5 min', '0-<50m:>5-10min',
         '50-100m:0-3min','50-100m:>3-5min','50-100m:>5-10min',	
         '≥100m or flyover:0-3min', '≥100m or flyover:>3-5min',	
         '≥100m or flyover:>5-10min'}]
pointList.fillna(fillCols, inplace=True)
pointList = pointList.astype(int)
WV_pc_site_spp['point_sum'] = pointList.sum(axis=1)
pointsFULL = pd.merge(left = WV_pc_site_spp, right= pointsDF['NE_or_SE'], how='outer', 
                    on=['block-point number','species', 
                            'habitat'],left_index=True)
groupdf = pointsFULL.groupby(['block-point number','species', 
                            'habitat', 'NE_or_SE']).agg({'point_sum': ['sum']})
unstackdf = groupdf.unstack(level=-1)
unstackdf.to_csv(resultsCSV)
groupdf.to_csv(resultsCSV2)
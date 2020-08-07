# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:36:12 2020

@author: Jessie Jordan
"""

import os
import re
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

dataDir = "P:/Proj6/USGAP-WVBBA/Data/"
#projDir = "C:/Users/jhpage/Data/Specieslists/"
projDir = "P:/Proj6/USGAP-WVBBA/Data/Specieslists/"

gap = projDir + "WV_GAP_Atlas.csv"
result = projDir + "WV_GAP_Atlas.csv"

## read gap and atlas files in as dataframes
df1 = pd.read_csv(gap, dtype={'strCommonName': 'string'})
print(df1.head())
df2 = pd.read_excel(io=dataDir + "WVBBA_DATA.xlsx", sheet_name="CAPTIONS", 
                    dtype={'species name': 'string'})
df2 = df2.rename(columns={"species name": "strCommonName"})
df2= re.sub(r'(?<=-)\w+', lambda m: m.group().lower(), df2['strCommonName'])
df2 = df2.filter(['strCommonName', 'sci name', 'total count', 'total blocks',
                  '% blocks', 'WV code'])
df2['strCommonName'] = [x.rstrip() for x in df2['strCommonName']]

print('\n')
print(df2.head())

##Join atlas spp to gap spp to include non-matches and export to csv
result = pd.merge(df1, df2, how='outer', on='strCommonName')
result.to_csv(projDir + 'WV_GAP_Atlasall.csv', index = False, header=True)
print('\n')
print(result.head(10))
print(len(result))

##Used after cleaning of document to include column describing if the species 
##data was used in the final WVBBA document
sppTable = pd.read_csv(projDir + 'WV_GAP_Atlasall.csv', 
                       dtype={'strScientificName_y': 'string'})
sppTable.fillna(value="NULL", inplace=True)
i= sppTable.index[0:] 
for i in sppTable.index[0:]:
    sppTable.loc[i,'modeled_WVBBA'] = ["0" 
                                       if sppTable.loc[i,'strScientificName_y'] 
                                       == "NULL" else "1"]
sppTable.to_csv(projDir + 'WV_GAP_Atlasall.csv', index = False, header=True)
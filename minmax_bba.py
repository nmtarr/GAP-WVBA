# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:36:09 2020

@author: Jessica
"""
import os
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

projDir = "P:/Proj6/GAP-WVBA/"
listDir = projDir + "Data/Specieslists/WV_AtlasCodes.csv"
resultsCSV = projDir + "Results/elevation_summary.csv"
codesBBA = projDir + "Data/Specieslists/BBA_sppcodes.csv"
from datetime import datetime

"""
## read sppList and Elev Summary dataframes
sppList = pd.read_csv(listDir, dtype={'strUC': 'string',
                                      'strCommonName': 'string'}) 
sppList.rename(columns = {'strUC':'GAP_code'}, inplace = True)
sppList.rename(columns = {'strScientificName_y':'strScientificName'}, 
               inplace = True)
sppList.drop(['state_name','strCommonName', 'intHa', 'strScientificName_x', 'N_birds', 
              'N_points', 'Det_Rate'], axis='columns', index=None, 
             columns=None, level=None, inplace=True, errors='raise')
print(sppList.head())
newDF = pd.read_csv(resultsCSV, dtype={'strUC': 'string'})
elDF = newDF.copy(deep=True)
#elDF['strUC'] = [x.rstrip() for x in elDF['strUC']]

#print('\n')
print(elDF.head())

##Join atlas spp to gap spp and export to csv
result = elDF.merge(sppList, how='outer', on='GAP_code')
print('\n')
print(result.head(10))
print(len(result))
result.to_csv(resultsCSV)

##Join atlas spp to gap spp to include non-matches and export to csv
result.drop(['WV_species_id'], axis='columns', index=None, 
             columns=None, level=None, inplace=True, errors='raise')
bbaList = pd.read_csv(codesBBA, dtype={'FIELD2': 'string'})
bbaList.rename(columns = {'FIELD2':'WV_species_id'}, inplace = True)
bbaList.rename(columns = {'FIELD4':'strScientificName'}, inplace = True)
bbaList.drop(['ID','FIELD1','FIELD3','FIELD5','ID.1'], axis='columns', index=None, 
             columns=None, level=None, inplace=True, errors='raise')
result2 = pd.merge(result, bbaList, how='left', on='strScientificName')
print('\n')
print(result2.head(10))
print(len(result2))
result2.to_csv(resultsCSV)
"""
#Where column name = loc, find max and min value in roundelev 
#if value in spp column is greater than 0
#code is non-functional in this section and needs work to complete
timestamp = str(datetime.now(tz=None).strftime("%d%B%Y_%I%M%p"))
archiveCSV = projDir + "/Results/Archive/elevation_" + timestamp + ".csv"
elTable = pd.read_csv(resultsCSV, index_col = 'WV_species_id', 
                      dtype={'WV_species_id': 'string'}) 
for i in elTable.index[108:109]:
    print(i)
    bbaData= projDir + "Data/WVBBA_ALLDATA.csv"
    bbaDF= pd.read_csv(bbaData)
    bbaDF.set_index(i, drop = False, append = False, inplace = True)
    bbaDF.drop(bbaDF.index[bbaDF[i] == 0], inplace = True)
    sppMAX = bbaDF['roundelev'].max()
    elTable.loc[i, 'WVBBA_max'] = sppMAX
    print(sppMAX)
    sppMIN = bbaDF['roundelev'].min()
    elTable.loc[i, 'WVBBA_min'] = sppMIN
    print(sppMIN)
elTable.to_csv(archiveCSV)
elTable.to_csv(resultsCSV)
print("Done")

elTable = pd.read_csv(resultsCSV, index_col = 'WV_species_id', 
                      dtype={'WV_species_id': 'string'}) 
for i in elTable.index[0:]:
    maxdiff = (((elTable.loc[i, 'WVBBA_max']) - (elTable.loc[i, 'GAP_max_map']))/(elTable.loc[i, 'GAP_max_map']))*100
    mindiff = (((elTable.loc[i, 'GAP_min_map']) - (elTable.loc[i, 'WVBBA_min']))/(elTable.loc[i, 'GAP_min_map']))*100
    #if maxdiff >0:
    elTable.loc[i, 'above_GAP_max(%)'] = maxdiff
    #if maxdiff <=0:
    elTable.loc[i, 'below_GAP_min(%)'] = mindiff 
elTable.to_csv(archiveCSV)
elTable.to_csv(resultsCSV)


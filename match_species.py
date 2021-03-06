import os
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)
import repo_functions as fun

#projDir = "P:/Proj6/GAP-WVBA/Data/"
projDir = fun.projDir
projDir = "C:/Users/jhpage/Data/Specieslists/"
atlas = projDir + "WVAtlasSPP.csv"
gap = projDir + "Gap_birds_WV.csv"
result = projDir + "Gap_birds_WV.csv"
result2 = projDir + "Gap_birds_WV.csv"

## read gap and atlas files in as dataframes
df1 = pd.read_csv(gap, dtype={'strCommonName': 'string'})
print(df1.head())
df2 = pd.read_csv(atlas, dtype={'strCommonName': 'string'})
df2['strCommonName'] = [x.rstrip() for x in df2['strCommonName']]

print('\n')
print(df2.head())

##Join atlas spp to gap spp and export to csv
result = df1.merge(df2, how='outer', on='strCommonName')
print('\n')
print(result.head(10))
print(len(result))
result.to_csv(projDir + 'WV_GAP_Atlas.csv', index = False, header=True)

##Join atlas spp to gap spp to include non-matches and export to csv
result2 = pd.merge(df1, df2, how='right', on='strCommonName')
result2.to_csv(projDir + 'WV_AtlasCodes.csv', index = False, header=True)
print('\n')
print(result2.head(10))
print(len(result2))
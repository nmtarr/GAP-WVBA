import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 10)

atlas = 'T:\\Temp\\Specieslists\\WVAtlasSPP.csv'
gap = 'T:\\Temp\\Specieslists\\Gap_birds_WV.csv'
result = 'T:\\Temp\\Specieslists\\Gap_birds_WV.csv'

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
result.to_csv('T:\\Temp\\Specieslists\\WV_GAP_AtlasNT.csv', index = False, header=True)

import os
import pandas as pd

atlas = 'C:\\Users\\jhpage\\Specieslists\\WVAtlasSPP.csv'
gap = 'C:\\Users\\jhpage\\Specieslists\\Gap_birds_WV.csv'
result = 'C:\\Users\\jhpage\\Specieslists\\Gap_birds_WV.csv'

##read gap and atlas files in as dataframes
df1 = pd.read_csv(gap)
df2 = pd.read_csv(atlas)

##Join atlas spp to gap spp and export to csv
result = pd.merge(df1, df2, how='outer', on='strScientificName')
result.to_csv('C:\\Users\\jhpage\\Specieslists\\WV_GAP_Atlas.csv', index = False, header=True)
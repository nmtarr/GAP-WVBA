import repo_functions as fun
import pandas as pd
species = "Cerulean Warbler"

#def WVBBA_detected_in(species):
'''
Returns list of cover types WVBBA found species in.
'''
WV = pd.read_csv(fun.resultsDir + "WV_spp_lc_detections.csv", header=0)
WV.rename({'1"': '1',
           '1"U': '1'}, axis=1, inplace=True)
WV.fillna(0)
WV['new'] = WV['1'] + WV['10']

spp = fun.GAP_spp_code(species)
WV_types = (WV
            [lambda x: x['species'] == spp[1:5]]
            .T)


WV_types = (WV_types.rename(columns={WV_types.columns[0]: 'detections'})
            .iloc[1:]
            [lambda x: x['detections'] > 0])
#return WV_types

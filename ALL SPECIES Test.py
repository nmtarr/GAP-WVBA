#!/usr/bin/env python
# coding: utf-8

# #  US Gap Analysis Project - WV Breeding Bird Atlas Data Comparison 
# Nathan Tarr and Jessie Jordan
# 
# ## Cover type associations in West Virginia
# We investigated the agreement between WV Breeding Bird Atlas (2011-2015) and USGS Gap Analysis Project data on 


# In[12]:


import pandas as pd
import numpy as np
import repo_functions as fun
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)

# In[13]:
# Call species lists and generate empty dataframes-----------------------------
specieslist = (pd.read_csv(fun.dataDir + "/SpeciesLists/WV_GAP_Atlas.csv", 
                           index_col ='strCommonName', header=0))
mastdf = pd.DataFrame(index=[ "Unusable", "Supported validation", 
                                        "Supported addition", 
                                        "Total detections"], 
                             columns=["Species", "detections"])
masteval = pd.DataFrame(index=[ "Unvalidated", "Validated", 
                              "Additions"], columns=["Species", 
                                            {"GAP_types" : int()}])
allunmatch = pd.DataFrame()

# Load land cover crosswalk - slow loading for some reason
cross = pd.read_csv(fun.dataDir + "LandCover/land_cover_crosswalk.csv", 
                    header=0, dtype={'GAP_code': str}) 
# In[14]:
for species in specieslist.index[0:]:
    try:
        # Perform crosswalk of detections from WV -> USGAP
        master, GAP_linked, unmatched, gap_types, wv_types = fun.cross_to_GAP(species, cross)

        #Insert Species name into first column
        
        print(str("Species summary complete for ") + species)
        master_valid = master[master['evaluation'] == 'valid']
        master_add = master[master['evaluation'] == 'add_association']
        usable_df = pd.DataFrame(index=[ "Unusable", "Supported validation", 
                                        "Supported addition", 
                                        "Total detections"], 
                             columns=["detections"])
        usable_df.loc['Supported validation', 
                      'detections'] = int(master_valid[['detections']].sum())
        usable_df.loc['Supported addition', 
                      'detections'] = int(master_add[['detections']].sum())
        usable_df.loc['Total detections', 
                      'detections'] = wv_types['detections'].sum()
        usable_df.loc['Unusable', 
                      'detections'] = int(wv_types['detections'].sum() - 
                                          master_valid[['detections']].sum() - 
                                          master_add[['detections']].sum())
        usable_df.insert(0, "Species", species, True)
        usable_df = usable_df.fillna(0)
        mastdf = pd.concat([usable_df, mastdf])
        
        # Aggregate results for proportion of GAP systems validated------------
        eval_df = pd.DataFrame(index=[ "Unvalidated", "Validated", 
                                      "Additions"], columns=[int("GAP_types")])
        eval_df.loc['Unvalidated', "GAP_types"] = len(gap_types) - len(master_valid)
        eval_df.loc['Validated', "GAP_types"] = len(master_valid)
        eval_df.loc['Additions', "GAP_types"] = len(master_add)
        eval_df.insert(0, "Species", species, True)
        eval_df = eval_df.fillna(0)
        masteval = pd.concat([eval_df, masteval])
        print(eval_df)
        print(species + " add successful")
        #Generate a full list of unmatched habitat types across all species
        #(DOES NOT WORK, STILL GENERATING EMPTY DATFRAME)
        print(unmatched)
        allunmatch = pd.concat([unmatched, allunmatch])
    except Exception as e: 
            print(str(" concatonate failed for ") + species) 
            print(e) 
print(mastdf)
print(masteval)

#The following: drop na does make a slight difference on final results though 
#the main purpose was to clean excess NaN records for bird not in WVBBA        
mastdf = mastdf.dropna()
masteval = masteval.dropna()

#Create pivot table summarizing the validtidity of WVBBA habitat detections
pivdf = mastdf.pivot_table(index = mastdf.index,
                           aggfunc = {'detections' : [np.mean, sum, lambda x: len(x.unique())]},
                           fill_value = 0).sort_index()
print(pivdf) 

#Create pivot table summarizing the proportion of GAP systems validated 
#(SUMMARY OF GAP_types NOT WORK DUE TO NOT INTEGER DATATYPE)
piveval = masteval.pivot_table(index = masteval.index,
                           aggfunc = {'GAP_types' : [np.mean, sum, lambda x: len(x.unique())]},
                           fill_value = 0).sort_index()

#Plot pie chart of total detections
plt1 = pivdf.drop(['Total detections']).plot(y=('detections',        'sum'), 
                                             kind='pie',
                                             legend=False, 
                                             title = "Total Species Detections",
                                             colors=['gray', 'g', 'y'])
plt1.set_ylabel("")   

print(eval_df)
plt2 = piveval.plot(y='GAP_types', kind='barh', legend=False, 
                    title = "All species GAP associations")    
# In[17]:
    
#Something is wrong with the following now, returns an empty df, see above loop 
#instead of all unmatched---follow up and troubleshoot   
# Show invalid WV codes entered ----------------------------------------------
print("Invalid habitat codes entered by WVBBA observers:")
print(allunmatch)
    


    

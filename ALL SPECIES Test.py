#!/usr/bin/env python
# coding: utf-8

# #  US Gap Analysis Project - WV Breeding Bird Atlas Data Comparison 
# Nathan Tarr and Jessie Jordan
# 
# ## Cover type associations in West Virginia
# We investigated the agreement between WV Breeding Bird Atlas (2011-2015) and USGS Gap Analysis Project data on 


# In[12]:


import pandas as pd
import repo_functions as fun
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)

# In[13]:
# Define a species ----------------------------------------------------------
specieslist = (pd.read_csv(fun.dataDir + "/SpeciesLists/WV_GAP_Atlas.csv", 
                           index_col ='strCommonName', header=0))
mastdf = pd.DataFrame(index=[ "Unusable", "Supported validation", 
                                        "Supported addition", 
                                        "Total detections"], 
                             columns=["Species", "detections"])

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
        usable_df = usable_df.fillna(0)
        usable_df.insert(0, "Species", species, True)
        mastdf = pd.concat([usable_df, mastdf])
        print(species + " add successful")
    except Exception as e: 
            print(str(" concatonate failed for ") + species) 
            print(e) 

#The following: drop na does make a slight difference on final results though 
#the main purpose was to clean excess NaN records for bird not in WVBBA        
mastdf = mastdf.dropna()
pivdf = mastdf.pivot_table(index = mastdf.index,
                           aggfunc = {'detections' : [np.mean, sum, lambda x: len(x.unique())]},
                           fill_value = 0).sort_index()
print(pivdf) 
#Too many labels in plot, also plot average as bar   
plt1 = pivdf.drop(['Total detections']).plot(y='detections', kind='pie',
                                                     legend=False, 
                                                     title = "Total Species Detections",
                                                     colors=['gray', 'g', 'y'])
plt1.set_ylabel("")   

    
# In[17]:
    
#Something is wrong with the following now, returns an empty df 
#instead of all unmatched---follow up and troubleshoot   
# Show invalid WV codes entered ----------------------------------------------
print("Invalid habitat codes entered by WVBBA observers:")
print(unmatched)
    
    
    
    # In[19]:
    
  """  
    # Report and plot results for proportion of GAP systems validated ------------------------------
    eval_df = pd.DataFrame(index=["Unvalidated", "Validated", "Additions"], columns=["GAP_types"])
    eval_df.loc['Unvalidated', "GAP_types"] = len(gap_types) - len(df_valid)
    eval_df.loc['Validated', "GAP_types"] = len(df_valid)
    eval_df.loc['Additions', "GAP_types"] = len(df_add)
    eval_df = eval_df.fillna(0)
    print(eval_df)
    plt2 = eval_df.plot(y='GAP_types', kind='barh', legend=False, title = species + " GAP associations")
    

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 08:56:48 2020

@author: nmtarr


"""
import pandas as pd
import repo_functions as fun 
import numpy as np
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', 400)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_columns', 15)


# Read in the map list -- map type by species --------------------------------
maps_list = pd.read_excel(io=fun.dataDir + "WVBBA2 maps by species.xlsx", 
                          sheet_name="Species list")

# Fix some common names
maps_list['Species Account'].replace("Black-and-white Warbler", 
                                     "Black-and-White Warbler",
                                     inplace=True)
maps_list['Species Account'].replace("Blue-Gray Gnatcatcher", 
                                     "Blue-gray Gnatcatcher",
                                     inplace=True)
maps_list['Species Account'].replace("Chuck-wills-widow", 
                                     "Chuck-will's-widow",
                                     inplace=True)
maps_list['Species Account'].replace("Cooper’s Hawk", 
                                     "Cooper's Hawk",
                                     inplace=True)
maps_list['Species Account'].replace("Eastern Screech-Owl", 
                                     "Eastern Screech-owl",
                                     inplace=True)
maps_list['Species Account'].replace("Eastern Whip-poor-will", 
                                     "Whip-poor-will",
                                     inplace=True)
maps_list['Species Account'].replace("Eastern Wood-Pewee", 
                                     "Eastern Wood-pewee",
                                     inplace=True)
maps_list['Species Account'].replace("Eurasian Collared-Dove", 
                                     "Eurasian Collared-dove",
                                     inplace=True)
maps_list['Species Account'].replace("Northern Saw-Whet Owl", 
                                     "Northern Saw-whet Owl",
                                     inplace=True)
maps_list['Species Account'].replace("Wilson’s Snipe", 
                                     "Wilson's Snipe",
                                     inplace=True)
maps_list = maps_list[maps_list['Species Account'] != 'Total:']
maps_list = maps_list[maps_list['Species Account'].isnull() == False]

# Rename columns, set index to common name, replace "x" with 1
maps_list = (maps_list.rename({'Br. Evidence': 'breeding_evid_map',
                   'Est. occurrence': 'occupancy_map',
                   'Est. density': 'density_map',
                   'Est. change': 'change_map'}, axis=1)
             .set_index(['Species Account'])
             .replace("x", 1))

# Add species that were detected, but no evidence of breeding
'''
This list was acquired from Rich Bailey in an email Sept 30 2020.
'''
no_evid = ("American Coot", "Black-crowned Night-heron", "Common Gallinule",
           "Double-crested Cormorant", "Golden Eagle", "Mississippi Kite",
           "White-throated Sparrow")
no_evid = (pd.DataFrame({'Species Account': no_evid, 
                         'detected': [1,1,1,1,1,1,1]})
           .set_index(['Species Account']))

# New column for detected only (no breeding evidence)
maps_list['detected'] = 1

# Add new rows for detected only species
maps_list2 = maps_list.append(no_evid)


# Read in the spp crosswalk --------------------------------------------------
crosswalk = pd.read_csv(fun.dataDir + "SpeciesLists/WV_GAP_Atlas2.csv", header=0)

# Drop old 'modeled' column
crosswalk.drop(['modeled_WVBBA'], axis=1, inplace=True)

# Add new columns to the crosswalk for map type
crosswalk['breeding_evid_map'] = False
crosswalk['occupancy_map'] = False
crosswalk['density_map'] = False
crosswalk['change_map'] = False
crosswalk['detected'] = False


# Update the crosswalk -------------------------------------------------------
cr2 = (crosswalk.set_index(['strCommonName'])
       .rename({'sci name': 'sci_name_WV', 
                'strScientificName_x': 'sci_name_GAP'}, axis=1))
cr2.update(maps_list2)

# Non-matched indices were left out, add them in
missing = [x for x in no_evid.index if x not in cr2.index]
missingDF = no_evid[no_evid.index.isin(missing)]
cr2 = cr2.append(missingDF)

# Fill na with 0
for x in cr2.columns[-5:]:
    cr2[x].fillna(0, inplace=True)
    

# Add GAP modeled column -----------------------------------------------------
cr2['GAP_modeled'] = np.where(cr2['intHa'] > 0, 1, 0)  

    
# Write new crosswalk --------------------------------------------------------
cr2 = cr2[['sci_name_GAP', 'sci_name_WV', 'strUC', 'WV_code', 'GAP_modeled',
          'detected', 'occupancy_map', 'density_map', 'change_map',
          'breeding_evid_map', 'intHa', 'N_birds', 'N_points', 'Det_Rate',
          '%_of_blocks', 'notes']]
cr2.index.name = "common_name"
cr2.to_csv(fun.dataDir + "SpeciesLists/WV_GAP_Atlas3.csv")


"""
##############################################################################
# Extras ---------------------------------------------------------------------
# Build breeding evidence list
br_evid = list(maps_list[maps_list['Br. Evidence'].isnull() == False]['Species Account'])

# Build occupancy map list
occupancy = list(maps_list[maps_list['Est. occurrence'].isnull() == False]['Species Account'])

# Build density map list
density = list(maps_list[maps_list['Est. density'].isnull() == False]['Species Account'])

# Build change map list
change = list(maps_list[maps_list['Est. change'].isnull() == False]['Species Account'])
"""
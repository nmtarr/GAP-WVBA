# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:05:33 2020

@author: nmtarr

Example of one way to perform crosswalk with site-specific survey data.

"""
import pandas as pd

# make example data frames - similar to what we already have
survey_df = pd.DataFrame([["a", "sp1", "forest"],
                         ["b", "sp2", "water"]],
                         columns=["site", "species", "WVtype"])

site_df = pd.DataFrame([["a", 1, 0], ["b", 0, 1]], 
                       columns=["site", "region1", "region2"])

cross_df = pd.DataFrame(columns=["WVtype", "GAPtype"], 
                        data=[["forest", "forest1"], ["forest", "forest2"],
                              ["forest", "forest3"], ["water", "water1"],
                              ["water", "water2"], ["water", "water3"]])

GAPlc_df = pd.DataFrame(columns=["GAPtype", "region1", "region2"], 
                        data=[["forest1", 1, 1], ["forest2", 1, 0],
                              ["forest3", 0, 1], ["water1", 1, 0],
                              ["water2", 1, 1], ["water3", 0, 1]])

print(survey_df); print(site_df); print(cross_df); print(GAPlc_df)


# add columns that represent crosswalk at wv level
df1 = pd.merge(GAPlc_df, cross_df, on=["GAPtype"], how="inner")
print(df1)

# assess a species ------------------------------------------
sp = "sp1"
region = "region1" # I think this may have to be done by region (looping)
linked_types = set([])

survey_df2 = survey_df[survey_df["species"] == sp]

region = "region1"
# pull together site and survey data -- that adds region columns
df2 = pd.merge(survey_df2, site_df, on=["site"], how="left") 
df2 = df2[df2[region] == 1]
print(df2)

# do the crosswalks by region
df3 = pd.merge(df2, df1, on=["WVtype", region], how="left")
linked_types = linked_types | set(df3["GAPtype"].tolist())

# the final list
print(linked_types)
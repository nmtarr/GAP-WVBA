library("rebird")

setwd("/Proj6/USGAP-WVBBA/Data/SpeciesLists/")
ebird_wv <- ebirdfreq("states", "US-WV", 2009, 2014, 5, 6)
write_excel_csv(ebird_wv, "ebird_wv.csv")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ebird_wv <- ebirdfreq("states", "US-WV", 1900)
help(ebirdfreq)
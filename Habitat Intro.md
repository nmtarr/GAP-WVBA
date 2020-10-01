## Background
For the 2nd WV Breeding Bird Atlas (2011-2015, WVBBA), observers conducted point counts throughout West Virginia in which they recorded the type of plant community each individual bird was in when detected.  Those data, which are essentially "aspatial" provided an opportunity to assess USGS National Gap Analysis Project (GAP) habitat-associations in a manner that was free of confounding errors that are often present in spatial comparisons.  Errors in data layers confound comparisons of habitat-associations with survey locations and land cover maps because location uncertainty and map errors make it unclear whether disagreement is the result of error in GAP habitat-assocations or spatial data used in the comparison.      

Our __objectives__ were to
* Determine whether we can validate GAP cover type associations with this type of data.
* Identify barriers to this type of comparison.
* Determine whether obtaining useful habitat data in this way (for an atlas) is feasible.

For __each species__, we asked
* Which existing associations are supported (validated)?
* What additional associations are supported?
* How many GAP associations remain unvalidate?
* What proportion of detections were unusable?
* What proportion of detections supported an additional associations?
* What proportion of detections validated an existing association?
* What WVBBA types were entered that couldn't be linked at all?

We explored two questions regarding results __across all species__
* What proportion of the records are usable (averaged across species) in light of uncertainties in links.
* Averages of measure from above.

## Methods
We acquired the 2nd WVBBA data and linked it to GAP data with two crosswalk tables.  One table linked species concepts and common names from the two projects.  The other crosswalk table linked habitat classes ("cover types").  It was possible to link species in a one-to-one fashion, but that was not the case for cover types.  Differences in the scales and "boundaries" of class definitions made several one-to-many links unnavoidable.  We also quantified our confidence in cover type links with a score of "low", "med", or "high" (0.50, 0.75, and 1.00 respectively).

Linking the two data sets allowed us to "translate" WVBBA data into the framework that GAP used and identify cases of validation or improvement.  We incorporated the uncertainty present in our cover type crosswalk into our "translation" by calculating a measure of support for each link.  The support metric was defined as the confidence in a cover type link divided by the number of classes to which the type was linked.  This metric differs by the "direction" of comparison (GAP-to-WVBBA or vice versa), however, we were only interested in the WVBBA-to-GAP direction, so the values used were calculated as the confidence in links of a given WVBBA type divided by the number of GAP types the focal WVBBA type was linked to.  We classified support metric values as low (0.0, 0.49), medium (0.50, 0.80), or high (0.81, 1.00) and only used "high" support metrics for evaluations.  For example, if a species was detected by WVBBA in WVBBA cover type A and we were fully confident (confidence = 1) that WVBBA type A linked to either GAP type AA or BB (2 links), then the support metric had a value of 0.5 ("medium") and was excluded from evaluations.


## Key Findings

Some issues/barriers discovered
* Invalid habitat codes were sometimes recorded
* Cover types are inadequately defined.  As revealed by low cross walk confidence, and strange data (e.g., ACFL in "water"). 

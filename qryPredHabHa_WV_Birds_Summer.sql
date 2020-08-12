-- Generates table of bird species' predicted summer habitat in WV.
-- Manually save results.
-- SGW 23jul20
USE GAP_AnalyticDB;  
GO



WITH State_Hucs AS 
(
	SELECT        
	lu_boundary_species.species_cd AS strUC, 
	tblTaxa.strCommonName,
	tblTaxa.strScientificName,
	tblTaxa.strSubSciNameText,
	state.state_fipscode,
	state.state_name, 
	lu_boundary_species.count*0.09 AS intCount
	FROM
		hucs INNER JOIN lu_boundary 
			 ON hucs.objectid = lu_boundary.hucs 
			 INNER JOIN lu_boundary_species 
			 ON lu_boundary.value = lu_boundary_species.boundary 
			 INNER JOIN state 
			 ON lu_boundary.state = state.objectid 
			 INNER JOIN tblTaxa 
			 ON lu_boundary_species.species_cd = tblTaxa.strUC
	WHERE (state.state_fipscode = 54                                              -- West Virginia
		   AND LEFT(lu_boundary_species.species_cd,1) LIKE 'b'                    -- Birds
		   AND (lu_boundary_species.season = 1 OR lu_boundary_species.season = 3) -- Summer/Year-round
))

SELECT 
State_Hucs.strUC, 
State_Hucs.strCommonName,
State_Hucs.strScientificName,
State_Hucs.strSubSciNameText,
State_Hucs.state_name,  
SUM(State_Hucs.intCount) AS intHa
FROM State_Hucs
GROUP BY 
State_Hucs.strUC, 
State_Hucs.state_name, 
State_Hucs.strCommonName,
State_Hucs.strScientificName,
State_Hucs.strSubSciNameText
--, State_Hucs.strProt, State_Hucs.HUC12RNG
ORDER BY State_Hucs.strUC

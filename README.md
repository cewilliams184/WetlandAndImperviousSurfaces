# WetlandAndImperviousSurfaces
GIS 582 Final Project

Introduction: This project looks at wetland and impervious surfaces locations and in response to increased development in Wake County. The data used for this project has been derived from outside sources. 
Study Site: The study area for this project will be Wake County because it is experiencing a lot of growth in terms of population and development increase. This site was also selected because Wake County’s GIS page has a lot of available GIS resources. The coordinate system used for this project is NC State Plane Feet (NAD83); units area in feet. The project study area is located at coordinates: 35.8032° N, 78.5661° W.
Figure 1: Project Study Area of Wake County Boundary (Wake County, 2019).

Figure 2: Hydric soils and National Wetland Inventory Layer in Wake County, NC
                                                                            
Data sets: The data sources for this project were the National Wetland Inventory (NWI) which can provide a loose approximation on where wetlands are most likely to occur.  I also used NRCS (National Resources Conservation Service) for the NWI for hydrology data, and NRCS for soils and geomorphology data. For impervious surface I sourced data from four different years from the MRLC (Multi-Resolution Land Characteristics Consortium) webpage. 

Methods:Figure 3: process used by State of North Carolina Governor's Office of State Planning Center for Geographic Information and Analysis to classify wetlands when creating land cover maps in 1994. ( State of North Carolina Governor’s Office of State Planning Center for Geographic Information and Analysis, 1994)

In order to compare wetland and impervious surface number and size over time land cover data in Wake county was used by first isolating land cover data (State of North Carolina Governor’s Office of State Planning Center for Geographic Information and Analysis, 1994) for Wake County from the most recent NLCD set. The NLCD data for Wake County was then intersected with data from the National Wetland Inventory, and soils. This resulted in a general overview of where wetlands can occur. The process was then repeated for each year of available land cover data. Next impervious surfaces from various sources were combined (MRLC, City of Raleigh (greenway trails, subdivision, future land use) will be overlaid. First impervious surfaces that had greater than 75 percent surface impervious were modeled then surfaces with percentages of impervious surfaces were shown. This process was then be repeated for the different years of available data. The two data sets (wetland locations over the years and impervious surfaces over the years) were combined to show the locations in impervious surfaces and wetlands over the years (2001,2006,2011, and 2016). For each year the area of impervious and wetland surfaces was then calculated. The number of individual occurrences for each type of data were calculated and shown over time.       

Results and discussion: present and explain the results qualitative and quantitative, tables, graphs, maps/images; compare with results from other studies – confirms previously observed phenomena, shows something new, which questions remain unresolved
The results of the project are locations of wetland and impervious surfaces across Wake County, North Carolina (Fig 1). 
 
Figure 1. Wetland and Impervious Surfaces (where 75 percent of the grid cell is covered by impervious surfaces) across Wake County, NC.
In order to get a closer look to see if there were changes in wetlands and impervious surface sizes or locations across Wake County, two growing and developing areas were focused on; the Town of Cary (Fig 2) and the City of Raleigh (Fig 3). Originally, impervious surfaces where the percentage of the grid cell covered by impervious surface was greater than 75% were looked at. When reviewing these two areas there does not appear to be changes in wetland or impervious surface location or size across the years of available data: 2001, 2006, 2011, and 2016.   

Figure 2. Wetland and Impervious Surfaces (where 75 percent of the grid cell is covered by impervious surfaces) in and near downtown Cary, NC.

Figure 3. Wetland and Impervious Surfaces (where 75 percent of the grid cell is covered by impervious surfaces) in and near downtown Raleigh, NC.
The analysis was run again, this time including all percentages or grid cells covered by impervious surfaces, 0 to 100 percent coverage. In Figure 4 downtown Raleigh is shown in 2001 and in Figure 5 downtown Raleigh is shown in 2016. Surrounding areas were included due to the assumption that there would be more changes to impervious surfaces and wetlands in areas that are not currently made up of high levels of impervious surfaces. 

Figure 4. Impervious Surfaces in downtown Raleigh, and surrounding areas in 2001. Wetlands are represented by muted green (Wood Wetlands) and dark blue (Emergent Herbaceous Wetlands). Percent imperviousness is represented from no impervious surfaces (dark green), to 100 percent impervious surface (red)	Figure 5. Impervious Surfaces in downtown Raleigh, and surrounding areas in 2016. Wetlands are represented by muted green (Wood Wetlands) and dark blue (Emergent Herbaceous Wetlands). Percent imperviousness is represented from no impervious surfaces (dark green), to 100 percent impervious surface (red)
As can be seen when comparing figure 4 to figure 5 here appears to be no change in wetland size or impervious surface percentage. To make sure there were no changes I used map algebra and subtracted the oldest land class data of the impervious surfaces (2001) from the newest set of land class data (2016). Based on the results seen in Figure 6, there were no changes.
 
Figure 6. No difference is shown between impervious surface data from 2001 and 2016.
Since there were no changes in wetland or impervious surfaces changes there were only one set of numbers for the results. There were 4,204 Woody Wetlands in Wake County covering 21,859 acres and 2,554 Emergent Herbaceous Wetland covering 1,642 acres.  
The question that remains to be addressed is, are wetland and impervious surfaces changing over time in Wake County and what data will be useful to answer this question. 

Conclusion: From this project it was found that using land cover data as the main input may not have been the best choice, whether that was due to scale of the project or the intervals of the studied years needs to be determined. For future iterations of this project there are a few factors that can be adjusted. Instead of using land class data as one of the input sources I would use land class data as a guide and work to model water flow and collection in low lying areas. Then I would use map algebra to overlap the low-lying areas with soils data.

References  
Barendregt, A., & Schot, P., & van Horseen, P., (1999). A GIS-based plant prediction model for wetland ecosystems Landscape Ecology, volume 14(3), pp 255.  Retrieved from https://link.springer.com/article/10.1023/A:1008058413152  
Carle, M.V. (2001). Estimating Wetland Losses and Gains in Coastal North Carolina: 1994-2001 (2011). Wetlands, 31(6). 1277. Retrieved from https://link.springer.com/article/10.1007/s13157-011-0242-z 
Chapmann, H. & Cheetam, J. (2002). Monitoring and Modelling Saturation as a Proxy Indicator for in situ Preservation in Wetlands—a GIS-based Approach. Elsevier, volume 29 (3), pp 278.  Retrieved from https://www.sciencedirect.com/science/article/pii/S0305440302907090 
Department of Environment, Health and Natural Resources. Division of Water Quality Water. Quality Section (1997) COMMON WETLAND PLANTS OF NORTH CAROLINA. North Carolina: DWQ 
(2019). Wake County. Retrieved from https://goo.gl/maps/qecZds6k4eykSdcU7
Multi Resolution Land Characteristic Consortium (2001, 2006, 2011,2016). Impervious Surfaces. [Conus All Years]. Retrieved from https://www.mrlc.gov/data?f%5B0%5D=category%3Aland%20cover&f%5B1%5D=category%3Aurban%20imperviousness
Multi Resolution Land Characteristic Consortium (2001, 2004, 2006, 2008, 2011,2013 2016). NLCD Land Cover (CONUS) All Years. Retrieved from https://www.mrlc.gov/data?f%5B0%5D=category%3Aland%20cover&f%5B1%5D=category%3Aurban%20imperviousness
Raleigh GIS. (2019). Future Land Use [Feature Layer]. Raleigh Extraterritorial Jurisdiction (ETJ): Open Data Raleigh. Retrieved from http://data-ral.opendata.arcgis.com/search?q=land%20use
State of North Carolina Governor’s Office of State Planning Center for Geographic Information and Analysis (1994). A Standard Classification System for the Mapping of Land Use and Land Cover. North Carolina.
Townsend, P. (1998). Modeling floodplain inundation using an integrated GIS with radar and optical remote sensing. Geomorphomogy, volume 21(3-4).  Retrieved from https://www.sciencedirect.com/science/article/abs/pii/S0169555X9700069X

Appendix: workflows, commands, scripts, metadata, software-specific issues
To perform the iterations over the data for different years I wrote a python script, shown below that makes use of the arcpy module. 

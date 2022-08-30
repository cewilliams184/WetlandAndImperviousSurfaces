#Extract by mask raster maps to study area
#Chantel Williams
#Nov 2019
#Final Project
#inputs: inputfileloc, PSA, outputfile location,  ImperviousSurfaces, Soils, Landuse
''' example: C:\Project\ProjectFiles\Input C:\Project\ProjectFiles\Input\Wake_County_Line\Wake_County_Line.shp C:\Project\ProjectFiles\Output C:\Project\ProjectFiles\Input\Impervious C:\Project\ProjectFiles\Input\Soils C:\Project\ProjectFiles\Input\LandUse C:\Project\ProjectFiles\Intermediate'''
import sys,arcpy, os  

def Clip2PSA (directory, StudyArea, intermLoc,addText):
    ''' extracts by mask raster files and copies them to
         intermediate location (directory, StudyArea, intermLoc,addText)'''
    arcpy.env.workspace = str(directory)
    RasterList = arcpy.ListRasters()
    print RasterList
    for raster in RasterList:
        rasterpath=os.path.join(directory,raster)
        outTool =arcpy.sa.ExtractByMask(rasterpath,StudyArea)
        outExtractByMaskPath = str(outTool)
        saveNewLoc(RasterList,addText, intermLoc, outTool)
        return RasterList
    
def ExtractValuesRaster (directory,wildcard, query,textAddedToName,intermLoc):
    ''' saves wetland raster to specified location
    (directory,wildcard, query,textAddedToName,intermLoc)'''
    arcpy.env.workspace = str(directory)
    LUIntlist = arcpy.ListRasters(wildcard)
    print LUIntlist
    for raster in LUIntlist:
        rasterpath=os.path.join(directory,raster)
        outTool = arcpy.sa.ExtractByAttributes(raster,query)
        outExtractByAttributePath = str(outTool)
        saveNewLoc(LUIntlist,textAddedToName, intermLoc, outTool)
    return outExtractByAttributePath

def saveNewLoc(RasterList,addText,intermLoc,outTool):
    for raster in RasterList:
        base = str(os.path.basename(raster))
        intbase = "{0}{1}".format(addText,base)
        intPath = str(os.path.join(intermLoc,intbase))
        outintRaster = outTool.save(intPath)
        outintRasterPath = str(outintRaster)
    return outintRasterPath
    

#checkout spatial analyst extension
arcpy.CheckOutExtension("Spatial")

#define inputs
IS = 'C:\Project\ProjectFiles\Input\Impervious'
Landuse = 'C:\Project\ProjectFiles\Input\LandUse'
Soils = 'C:\Project\ProjectFiles\Input\Soils\soilmu_a_nc183.shp'
intermediateimp = 'C:\Project\ProjectFiles\Intermediate\intermediateImpervious'
intermediatewet = 'C:\Project\ProjectFiles\Intermediate\intermediateWetland'
PSA = 'C:\Project\ProjectFiles\Input\Wake_County_Line\Wake_County_Line.shp'
directory = 'C:\Project\ProjectFiles\Input'
output = 'C:\Project\ProjectFiles\Output'

#set workspace
arcpy.env.workspace = directory
arcpy.env.overwriteOutput = True


#extract hydric soils in Wake County
query = "MUSYM = 'AaA' OR MUSYM = 'BbA' OR MUSYM = 'ChA' OR MUSYM = 'DaA' OR MUSYM = 'GoA' OR MUSYM = 'LyA' OR MUSYM = 'MrA' OR MUSYM = 'RaA' OR MUSYM = 'RkA' OR MUSYM ='RoA'"
HydricSoils = os.path.join(intermediateWetland,'HydricSoils') #define hydric soils and new location
arcpy.Select_analysis(Soils, HydricSoils,query)



    
'''with arcpy.SearchCursor(Soils, query, 'MUKEY') as cursor:
        for row in cursor:
            print row
            FieldListValue.append(row)
            print FieldListValue
    #arcpy.SelectAnalysis(Soils, !MUSYM!, InpWhereClause)
    #arcpy.Copy_management
    del cursor'''
   # arcpy.da.SearchCursor(
#overlap landuse wetland, nwi, hydric soils








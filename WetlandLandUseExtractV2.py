
import os, arcpy
             
def Clip2PSA (directory, StudyArea, intermLoc,addText):
    ''' extracts by mask raster files and copies them to intermediate location'''
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
    ''' saves wetland raster to specified location (directory, query, textAddedToName)'''
    arcpy.env.workspace = str(directory)
    LUIntlist = arcpy.ListRasters(wildcard)
    print LUIntlist
    for raster in LUIntlist:
        rasterpath=os.path.join(directory,raster)
        outTool = arcpy.sa.ExtractByAttributes(raster,query)
        outExtractByAttributePath = str(outTool)
        saveNewLoc(LUIntlist,textAddedToName, intermLoc, outTool)
    return LUIntlist

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
Landuse = 'C:\Project\ProjectFiles\Input\LandUse'
intermediate = 'C:\Project\ProjectFiles\Intermediate'
PSA = 'C:\Project\ProjectFiles\Input\Wake_County_Line\Wake_County_Line.shp'
directory = 'C:\Project\ProjectFiles\Input'

arcpy.env.workspace = directory
arcpy.env.overwriteOutput = True

#clip land use rasters to study area
Clip2PSA(Landuse,PSA,intermediate,"C_")

#query wetland landuse classes; values 90(woody wetlands) and 95(emergent wetlands)
queryWet = "Value= 90 OR Value= 95"
ExtractValuesRaster(intermediate,"*LUN*",queryWet,"W",intermediate)
    
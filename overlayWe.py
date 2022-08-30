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
        return "RasterList:{0}".format(RasterList)
    
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
    return "outExtractByAttributePath:{0}".format(outExtractByAttributePath)

def overlayFiles (directory,outdirectory,distLetter,wildcard=""):
    '''if there are rasters converts rasters to shapefiles and intersects files in desired directory"
    (directory,outdirectory,distLetter,{wildcard})'''
    arcpy.env.workspace = str(directory)
    fileList = arcpy.ListRasters("{0}*".format(wildcard))
    print '1-----------------------------\n'  
    print fileList
    #Finished -convert to shapefiles
    for file in fileList:
        outp= os.path.join(directory,file)
        arcpy.RasterToPolygon_conversion(file,outp,"NO_SIMPLIFY","Value")
        print file
    #Finished - then intersect; creae a dicionar wih kes being he ear and he values being he shapefile pahs
    yearDict = {}
    print '2-----------------------------\n'
    
    shapeList = arcpy.ListFeatureClasses(feature_type='Polygon')
    
    for shape in shapeList:
        print shape
        year = shape[-8:-4]
        print "year: {0}".format(year)
        filepath=os.path.join(directory,shape)
        if year not in yearDict:
            yearDict[year]=[filepath]
        else:
            yearDict[year].append(filepath)
    print yearDict
    shapeList = arcpy.ListFeatureClasses(feature_type='Polygon')
    print '3-----------------------------\n'
    print shapeList
    print '4-----------------------------\n'
    for key in yearDict.keys():
        outf = "{0}_intersected_{1}".format(key,distLetter)
        outfpath = os.path.join(outdirectory,outf)
        print outf
        print "key: {0}".format(key)
        count = 0
        index = len(yearDict[key])-1
        while count<index:
            if len(yearDict[key])>=2:
                value = yearDict[key]
                print "value: {0}".format(value)
                arcpy.Intersect_analysis(value,outfpath)
                count += 1
    return yearDict         
    

def saveNewLoc(RasterList,addText,intermLoc,outTool):
    for raster in RasterList:
        base = str(os.path.basename(raster))
        intbase = "{0}{1}".format(addText,base)
        intPath = str(os.path.join(intermLoc,intbase))
        outintRaster = outTool.save(intPath)
        outintRasterPath = str(outintRaster)
        del outintRaster
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
impPercent = 75
impClass = 24

#set workspace
arcpy.env.workspace = directory
arcpy.env.overwriteOutput = True


#Finished - clip impervious surface data to PSA for impervious analsis 
Clip2PSA(IS,PSA,intermediateimp,"CI")
   
#Finished - clip land use rasters to study area for impervious analsis
Clip2PSA(Landuse,PSA,intermediateimp,"CL")

#Finished - clip land use rasters to study area for wetland analsis
Clip2PSA(Landuse,PSA,intermediatewet,"CL")

#Finished - query wetland landuse classes; values 90(woody wetlands) and 95(emergent wetlands)
queryWet = "Value= 90 OR Value= 95"
ExtractValuesRaster(intermediatewet,"*lun*",queryWet,"W",intermediatewet)

'''extract percent impervious surfaces from Wake Count Landuse raster with user defined class;
(impervious surface/developed classes are 21:<20% impervious surface, 22:20-49% impervious surface,
23: 50-79% impervious surface and the default is 24: 80-100%impervious sufaces)(G is used for sorting
purposes and so the impervious land use output classes will match the impervious percent land use output)'''
queryImpClass = "Value= {0}".format(impClass)
ExtractValuesRaster(intermediateimp,"*lun*",queryImpClass,"G",intermediateimp)

#Finished - extract impervious surfaces from impervious surface raster with user defined percentage; default is 75% (G is for greater than and for sorting) 
queryImp = "Value >= {0}".format(impPercent)
ExtractValuesRaster(intermediateimp,"*lui*",queryImp,"G",intermediateimp)

#Finished - extract hydric soils in Wake County
query = "MUSYM = 'AaA' OR MUSYM = 'BbA' OR MUSYM = 'ChA' OR MUSYM = 'DaA' OR MUSYM = 'GoA' OR MUSYM = 'LyA' OR MUSYM = 'MrA' OR MUSYM = 'RaA' OR MUSYM = 'RkA' OR MUSYM ='RoA'"
HydricSoils = os.path.join(intermediatewet,'HydricSoils') #define hydric soils and new location
arcpy.Select_analysis(Soils, HydricSoils,query)

#overlap wetland laers (clipped land use wetland, nwi,hydric soils)
WetOverlap = overlayFiles(intermediatewet,output,"W")                        

#overlap impervious laers (clipped land use
IntOverlap = overlayFiles(intermediateimp,output,"I","g")
   

#overlap landuse wetland, nwi, hydric soils







#Mapping Module
'''#adds a raster layer to an existing map and saves the result as a copy of the mxd in output folder;'C:\Project\ProjectFiles\Output'''
#Initialize data variables
myMap = os.path.join(output,'Impervious_Wetland_OutPut.mxd')
arcpy.env.workspace =myMap

#instantiate mapdocument and DataFrame Objects
mxd=arcpy.mapping.MapDocument(myMap)
dfs = arcpy.mapping.ListDataFrames(mxd)

#instantiate a layer object
layerObjSoils = arcpy.mapping.Layer('C:\Project\ProjectFiles\Intermediate\intermediateWetland\HydricSoils.shp')
layerObjWet = arcpy.mapping.Layer(WetOverlap)
#layerObjImp = arcpy.mapping.Layer(ImpOverlap)

#Get the first data frame
df = dfs[0]

#add new layer to map
arcpy.mapping.AddLayer(df, layerObjSoils)
arcpy.mapping.AddLayer(df, layerObjWet)
arcpy.mapping.AddLayer(df, layerObjImp)

#save copy of the map
copyName = 'C:/gispy/scratch/testAdd.mxd'
mxd.saveACopy(copyName)
print "{0} has been created.".format(copyName)

#example
'''#adds a raster layer to an existing map and saves the result as a cop of he mxd in  'C;\gisp\scrach'
# example: C:/gispy/data/ch24/maps/testAdd.mxd C:/gispy/data/ch24/otherData/getty_rast

import arcpy, sys


#Initialize data variables
myMap = sys.argv[1]
myRaster = sys.argv[2]
arcpy.env.workspace = myMap
arcpy.env.overwrite = True

#instantiate mapdocument and DataFrame Objects
mxd=arcpy.mapping.MapDocument(myMap)
dfs = arcpy.mapping.ListDataFrames(mxd)


#instantiate a layer object
layerObj = arcpy.mapping.Layer(myRaster)

#Get the first data fram
df = dfs[0]

#add new layer to map
arcpy.mapping.AddLayer(df, layerObj)

#save copy of the map
copyName = 'C:/gispy/scratch/testAdd.mxd'
mxd.saveACopy(copyName)
print "{0} has been created.".format(copyName)'''
   
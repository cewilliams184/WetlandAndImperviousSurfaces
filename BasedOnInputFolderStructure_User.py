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
    for raster in RasterList:
        rasterpath=os.path.join(directory,raster)
        outTool =arcpy.sa.ExtractByMask(rasterpath,StudyArea)
        outExtractByMaskPath = str(outTool)
        saveNewLoc(RasterList,addText, intermLoc, outTool)
    message = "Rasters Clipped"
    arcpy.SetProgressor('default',message)    
    return message
    
def ExtractValuesRaster (directory,wildcard, query,textAddedToName,intermLoc):
    ''' saves wetland raster to specified location
    (directory,wildcard, query,textAddedToName,intermLoc)'''
    arcpy.env.workspace = str(directory)
    LUIntlist = arcpy.ListRasters(wildcard)
    for raster in LUIntlist:
        rasterpath=os.path.join(directory,raster)
        outTool = arcpy.sa.ExtractByAttributes(raster,query)
        outExtractByAttributePath = str(outTool)
        saveNewLoc(LUIntlist,textAddedToName, intermLoc, outTool)
    message = "Values Extracted from: {0}".format(raster)
    arcpy.SetProgressor('default',message)
    return message

def overlayFiles (directory,outdirectory,distLetter,wildcard=""):
    '''if there are rasters converts rasters to shapefiles and intersects files in desired directory and calculates area."
    (directory,outdirectory,distLetter,{wildcard})'''
    arcpy.env.workspace = str(directory)
    fileList = arcpy.ListRasters("{0}*".format(wildcard))
    #Finished -convert to shapefiles
    for file in fileList:
        outp= os.path.join(directory,file)
        arcpy.RasterToPolygon_conversion(file,outp,"NO_SIMPLIFY","Value")
    #Finished - then intersect; create a dictionary with keys being he ear and he values being he shapefile pahs
    yearDict = {}
    shapeList = arcpy.ListFeatureClasses(feature_type='Polygon')
    
    for shape in shapeList:
        year = shape[-8:-4]
        filepath=os.path.join(directory,shape)
        if year not in yearDict:
            yearDict[year]=[filepath]
        else:
            yearDict[year].append(filepath)
    shapeList = arcpy.ListFeatureClasses(feature_type='Polygon')
    for key in yearDict.keys():
        outf = "{0}_intersected_{1}".format(key,distLetter)
        outfpath = os.path.join(outdirectory,outf)
        #print "key: {0}".format(key)
        count = 0
        index = len(yearDict[key])-1
        while count<index:
            if len(yearDict[key])>=2:
                value = yearDict[key]
               # print "value: {0}".format(value)
                arcpy.Intersect_analysis(value,outfpath)
                table = outfpath + '.shp'
                arcpy.SetProgressor ('default',table) 
                CalculateArea(table)
                count += 1
    message ="All Years Intersected"
    arcpy.SetProgressor('default',message)             
    return message

def CalculateArea(PolygonFile):
    arcpy.AddField_management(PolygonFile, "AREA", "DOUBLE")
    area = "!shape.area@acres!"
    arcpy.CalculateField_management(PolygonFile, "AREA", area, "PYTHON")
    message = "Area field and area calculated."
    arcpy.SetProgressor('default',message) 
    return message
    

def saveNewLoc(RasterList,addText,intermLoc,outTool):
    for raster in RasterList:
        base = str(os.path.basename(raster))
        intbase = "{0}{1}".format(addText,base)
        intPath = str(os.path.join(intermLoc,intbase))
        outintRaster = outTool.save(intPath)
        outintRasterPath = str(outintRaster)
        del outintRaster
    message = "File Saved: {0}".format(raster)
    arcpy.SetProgressor('default',message)    
    return message
    

#checkout spatial analyst extension
arcpy.CheckOutExtension("Spatial")

#define inputs
IS = sys.argv[1]  #'C:\Project\ProjectFiles\Input\Impervious'
Landuse = sys.argv[2] #'C:\Project\ProjectFiles\Input\LandUse'
Soils = sys.argv[3] #'C:\Project\ProjectFiles\Input\Soils\soilmu_a_nc183.shp'
intermediateimp = sys.argv[4] #'C:\Project\ProjectFiles\Intermediate\intermediateImpervious'
intermediatewet = sys.argv[5] #'C:\Project\ProjectFiles\Intermediate\intermediateWetland'
PSA = sys.argv[6] #'C:\Project\ProjectFiles\Input\Wake_County_Line\Wake_County_Line.shp'
directory = sys.argv[7] #'C:\Project\ProjectFiles\Input'
output = sys.argv[8] #'C:\Project\ProjectFiles\Output'
impPercent = sys.argv[9] #75
impClass = sys.argv[10] #24

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

#Finished - extract impervious surfaces from impervious surface raster with user defined percentage; default is 75% (G is for greater than and for sorting) 
queryImp = "Value >= {0}".format(impPercent)
ExtractValuesRaster(intermediateimp,"*lui*",queryImp,"G",intermediateimp)

#Finished - extract hydric soils in Wake County
query = "MUSYM = 'AaA' OR MUSYM = 'BbA' OR MUSYM = 'ChA' OR MUSYM = 'DaA' OR MUSYM = 'GoA' OR MUSYM = 'LyA' OR MUSYM = 'MrA' OR MUSYM = 'RaA' OR MUSYM = 'RkA' OR MUSYM ='RoA'"
HydricSoils = os.path.join(intermediatewet,'HydricSoils') #define hydric soils and new location
arcpy.Select_analysis(Soils, HydricSoils,query)

#overlap wetland layers (clipped land use wetland, nwi,hydric soils)
WetOverlap = overlayFiles(intermediatewet,output,"W")                        

#overlap impervious layers (clipped land use)
IntOverlap = overlayFiles(intermediateimp,output,"I","g")
   

#Mapping Module
'''#adds a raster layer to an existing map and saves the result as a copy of the mxd in output folder;'C:\Project\ProjectFiles\Output'''
#Initialize data variables
myMap = os.path.join(output,'Impervious_Wetland_OutPut.mxd')
arcpy.env.workspace =output

#instantiate mapdocument and DataFrame Objects
mxd=arcpy.mapping.MapDocument(myMap)
dfs = arcpy.mapping.ListDataFrames(mxd)

#instantiate a layer object
layerObjSoils = arcpy.mapping.Layer('C:\Project\ProjectFiles\Intermediate\intermediateWetland\HydricSoils.shp')
#layerObjWet = arcpy.mapping.Layer(WetOverlap)
#layerObjImp = arcpy.mapping.Layer(ImpOverlap)

#Get the first data frame
df = dfs[0]

#add new  layer to map
arcpy.mapping.AddLayer(df, layerObjSoils)

OutList = arcpy.ListFeatureClasses('*intersected*')
for outfeature in OutList:
    layerOut = os.path.join(output,outfeature)
    layerObjIntersect = arcpy.mapping.Layer(layerOut) #instantiate a layer object
    arcpy.mapping.AddLayer(df, layerObjIntersect)
    message = "Layer: {0} added".format(layerObjIntersect)
    arcpy.SetProgressor('default',message)

#save copy of the map
copyName = 'C:\Project\ProjectFiles\Output\Impervious_Wetland_OutPutV2.mxd'
mxd.saveACopy(copyName)
del mxd
print "{0} has been created. View output in Impervious_Wetland_OutPutV2.mxd located in folder: C:\Project\ProjectFiles\Output".format(copyName)

import arcpy, os

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
arcpy.env.workspace = r'C:\Project\ProjectFiles\Output'
arcpy.env.overwriteOutput = True

#HTML report

import csv, numpy

#write attribute table to csv file
shpList = arcpy.ListFeatureClasses() #create list of xml files in output folder
for shp in shpList:
    shpfile = os.path.join(output, shp) #inputfilepath
    outputCSV = os.path.join(output,"Report_{0}.csv".format(shp))
    reportFile = os.path.join(output,"CombinedReport.txt")
    #create csv
    with open(outputCSV,"w") as csvfile:
        csvwrite = csv.writer(csvfile, delimiter=",", lineterminator = '\n')
        #write field name header line
        field_names = [f.name for f in arcpy.ListFields(shp)]
        csvwrite.writerow(field_names)
        #Write data rows
        with arcpy.da.SearchCursor(shpfile,field_names) as s_cursor:
            for row in s_cursor:
                csvwrite.writerow(row)
            
    csvfile.close()

''' with arcpy.da.SearchCursor(shpfile,field) as cursor:
                for row in cursor:
                    summed_total = summed_total + row[0]
                    print summed_total'''
#sum area in intersected files
reportList = arcpy.ListFiles("*.csv")
summed_total = 0
fieldn = "AREA"
with open(reportFile,"w") as rfile:
    for report in reportList:
        reportFile = os.path.join(output,"CombinedReport.txt")
        #create combined report
        reportpath = os.path.join(output,report)
        field = arcpy.da.TableToNumPyArray(shpfile,fieldn,skip_nulls=True)
        sum = str(field[fieldn].sum())
        sum_txt = "{0} area is {1} acres \n".format(report,sum)
        rfile.write(sum_txt)
        
        
rfile.close()       

#Create HTML for report
htmlFile = os.path.join(output,"CombinedReport.html") #
dir = output #
rfile = open(reportFile,"r")
content = rfile.read()
hfile = open(htmlFile,"w") 
   

myHTML = ''' <!DOCTYPE html>
<html>
    <body>
     <h1> Wetland and Impervious Surface Report </h1> #
     <li>{0}</li>
    </body>
<html>
'''.format(content)   
print myHTML

outFile = open(htmlFile, 'w')
outFile.write(myHTML)
outFile.close()
print '{0} created.'.format(reportFile)



        



#Extract by mask raster maps to study area
#Chantel Williams
#Nov 2019
#GIS 582 Final Project
# example: C:\Student\GIS582\Project\DataCollection\Data\Input C:\Student\GIS582\Project\DataCollection\Data\Wake_County_Line\Wake_County_Line.shp C:\Student\GIS582\Project\DataCollection\Derived

import sys,arcpy, os

def CopyFile (file):
    '''copies output raster in 'outList' list to new location.'''               
    for out in outList:
        #join output path with newly created file
        cfile=str(outList[count]) #raster file in outList
        ext=str(os.path.splitext(cfile))#stores file type raster  in var
        base=str(os.path.basename(cfile)) #stores file name in var
        outRaster=os.path.join(output,base,ext) #joins outfile with file path
        #copy extracted files to a derived folder *need to add if folder doesn't exist create folder*
        arcpy.Copy_management(str(out),outRaster)
        #message= "Your files have been moved"
        
        


#checkout spatial analyst extension
arcpy.CheckOutExtension("Spatial")

#set workspace
file=sys.argv[1] 
arcpy.env.workspace = sys.argv[1]
arcpy.env.overwriteOutput = True

# define PSA and Output directory
output = sys.argv[3]
PSA=sys.argv[2]
FileList = arcpy.ListFiles()
#Check if file is raster or shapefile
for F in FileList:
    #Create Describe Object
    desc = arcpy.Describe(F)
    if desc.dataType == 'RasterDataset':    #if raster
        #Create list of rasters in folder directory with for loop incase input is incorrect
        RasterList = []
        RasterList.append(F)
        print RasterList
        if RasterList == None:
            print " Check the input file"
        else:
            print "You did it right!"
        #use extract by raster tool to apply study area mask
        for raster in RasterList:
            rasterpath=os.path.join(file,raster)
            outExtractByMask=arcpy.sa.ExtractByMask(rasterpath,PSA)
            outExtractByMask.save(str(outExtractByMask))
            outList = []
            outList.append(outExtractByMask)
            print outList
            #count = 0
            #for x in outList:
               # index = int(count+1)
            # CopyFile(x)
            #check if impervious or land class data
            #if land class data
                #extract values 90 (woody wetlands) and 95 (emergent wetlands)
                #save extracted values with value added to file name
    elif desc.extension == '.shp':
        OtherList = arcpy.ListFiles(".shp")
        if OtherList == None:
            print "Check the input file"
        else:
            print "You got a shapefile!"
                # use clip tool to clip data to study area
        for Ofile in OtherList:
            filepath = os.path.join(file,Ofile)
            outClip = os.path.join(output,Ofile,'_clip')
            ClipFeature = arcpy.Clip_analysis(filepath,PSA,outClip)
#intersect all clipped/extracted features


            
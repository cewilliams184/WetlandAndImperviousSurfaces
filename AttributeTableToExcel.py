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
                
    
    
    

htmlFile = os.path.join(output,"CombinedReport.html") #
dir = output #
rfile = open(reportFile,"r")
content = rfile.read()
hfile = open(htmlFile,"w") 
   
#Create HTML for report
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



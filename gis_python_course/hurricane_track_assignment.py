# todo: ASSIGNMENT 7 Vector Data Manipulation and Geometry
# Olivia Drukker

import arcpy
from arcpy import env
env.overwriteOutput = True
env.workspace = r'D:\Python\assignment_project\a7\a7Data'

# todo: TASK 1 - Write a python procedure
print('TASK 1')
# 1a) Create a file object to read the content of the file line-by-line.
f = open(r'D:\Python\assignment_project\a7\hurricane.txt', 'r')
## Line 1: AL022015,               BILL,     22,
## Line 2: 20150616, 0000,  , TS, 27.0, -94.3,  45, 1005,  140,  130,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,

# 1b) In the for-loop, check if a line is a header line with an if-else structure.
# 1c) Split the line by comma to obtain a list of string values. Print out the name of the hurricane.
for line in f:
    # print(line)
    if line.startswith('AL'): ## Use .startswith() to find all lines that begin with 'AL' - these are headers
        # print(line + '- Header line') ## Only print the header lines
        header = line.split(',')
        # print(header)
        ## Result header line 1: ['AL022015', '               BILL', '     22', '\n']
        ## Name of hurricane can be found using index[1]
        print(header[1]) ## Print names of hurricanes
    else:
        continue
f.close()

# todo: TASK 2 - Modify the procedure in Task 1 or create a new procedure
print('TASK 2')
# 2a) Create two file objects - one for reading and one for writing
f = open(r'D:\Python\assignment_project\a7\hurricane.txt', 'r')
fout = open('pt.csv', 'w')

# 2b) Create an if-else block to determine data lines and write them to a new file object
for line in f:
    if line.startswith('AL'):
        continue
    elif 'End Tracking...' in line:
        continue
    else:
        fout.write(line)

## 2c) Close the file
f.close()
fout.close()

# todo: TASK 3 - View the point data in ArcGIS
print('TASK 3')

# todo: TASK 4 - Develop a python procedure to create a line with attribute info based on hurricane.txt
print('TASK 4')
# todo: 4a) Analyze the content of the text file and explain the following as comments
# 4ai) How do you identify the name and number of track points for a hurricane? What types of lines should you use?
#       -if else statement first identifies header lines
#           - if 'AL' in line...
#       -Identify name and number by splitting header lines from hurricane.txt
#           - if 'AL' in line:... splitLine = line.split(',')
#       -Then use index[]
#           - if 'AL' in line:... name = splitLine[1]... tracks = int(splitLine[2])
#       -This creates variables to store the name and tracks information
#       -Use polylines to store hurricane tracks

# 4aii) How do you identify all track points from the same hurricane?
#       -Associate each point with its corresponding hurricane
#       -When a header line is encountered, a new array begins
#       -When a line that is not a header or ending is encountered, point information is extracted
#       -When an ending line is encountered, a polyline with all the previous points is created
#       -Because the lat/lon data comes between the header and ending lines, the function in 4b will correctly sort it

# todo: 4b) Create a new feature layer and additional attribute fields
# 4bi) Create a new line feature layer
# arcpy.management.CreateFeatureclass(out_path, out_name, {geometry_type}, {template}, {has_m}, {has_z}, {spatial_reference}, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3}, {out_alias}, {oid_type})
out_path = r'D:\Python\assignment_project\a7\a7Data'
out_name = 'hurricane.shp'
arcpy.CreateFeatureclass_management(out_path, out_name, "Polyline")

# Define Projection
# arcpy.management.DefineProjection(in_dataset, coor_system)
in_dataset = 'hurricane.shp'
coor_system = arcpy.SpatialReference(4326) ## Spatial reference code for WGS 1984
arcpy.management.DefineProjection(in_dataset, coor_system)

# 4bii) Add additional attributes: NAME of hurricane and NUMBER of tracks
# arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
in_table = 'hurricane.shp'
field_name = 'NAME'
field_type = 'TEXT'
arcpy.management.AddField(in_table, field_name, field_type, '', '', 20)

field_name = 'NUMBER'
field_type = 'LONG'
arcpy.management.AddField(in_table, field_name, field_type)

# todo: 4c) Develop statements to create hurricane paths
# 4ci) Create InsertCursor
# InsertCursor (in_table, field_names, {datum_transformation}, {explicit})
in_table = 'hurricane.shp'
field_names = ['SHAPE@', 'NAME', 'NUMBER']
cursor = arcpy.da.InsertCursor(in_table, field_names)

# 4cii) Create new file object to read hurricane.txt. Create a for loop to access content line by line.
# 4ciii) Build an if else block to check the content to determine three types of lines and perform operations.
f = open('hurricane.txt', 'r')

for line in f:
    if 'AL' in line:
        splitLine = line.split(',')
        name = splitLine[1]
        tracks = int(splitLine[2])
        lineArray = arcpy.Array()
    elif 'End Tracking' in line:
        polyline = arcpy.Polyline(lineArray) ## Create polyline
        cursor.insertRow([polyline, name, tracks]) ## Insert lines with insertCursor
    else:
        splitLineData = line.split(',')
        lat = float(splitLineData[4])
        lon = float(splitLineData[5])
        pt = arcpy.Point(lon, lat) ## Create point object
        lineArray.append(pt) ## Store coordinates in array

del cursor
f.close()

# todo: TASK 5 - In ArcGIS, create a complete map and describe the distributions of the hurricanes
print('TASK 5')




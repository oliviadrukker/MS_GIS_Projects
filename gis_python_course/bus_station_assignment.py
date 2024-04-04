# todo: ASSIGNMENT 6, GIS Data Access and Manipulation
# Olivia Drukker

import arcpy
from arcpy import env
env.overwriteOutput = True
env.workspace = r'D:\Python\assignment_project\a6\Week6_LabData\Data'

# todo: TASK 1: Create a Python procedure to identify the number of bus routes associated with each bus station
print('TASK 1')
# todo: 1a) Create a new field to store the number of routes associated with the station
# arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
in_table = 'BusStops.shp'
field_name = 'NumRoutes'
field_type = 'LONG'
arcpy.management.AddField(in_table, field_name, field_type)

# todo: 1b) Use an UpdateCursor and a loop structure to retrieve attribute values
# todo: 1d) Within the loop for the update cursor, create a procedure that can identify the number of routes based on
#  the attribute information.
# todo: 1e) Within the loop for the update cursor, create statements to update the values for the field created from
#  step 1.a to be the numbers of bus routes through stations
# arcpy.da.UpdateCursor (in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {explicit}, {spatial_filter}, {spatial_relationship}, {search_order})
in_table = 'BusStops.shp'
field_names = ['ROUTES', 'NumRoutes']
cursor = arcpy.da.UpdateCursor(in_table, field_names)
numberRoutes = 0

for row in cursor:
    routes_list = row[0].split(", ")
    numroute = len(routes_list)
    row[1] = numroute
    cursor.updateRow(row)
    # print(str(row[0]) + ' - ' + str(row[1])) ## Look at attribute values
del row
del cursor

# todo: 1c) View the attribute information for the two fields and explain how the attribute info of ROUTES can help you
#  identify the number of routes of every station
# 'ROUTES' is a string that lists the different bus routes separated by '.'. I used the split() method to break up the
# string. Then I created a new variable and used len() to find the number of routes in each feature. I assigned my
# new field to equal the new 'numroute' variable, so that the loop assigned the number of routes listed in the 'ROUTES'
# field to the new 'NumRoutes' field.

# todo: TASK 2: Create and run a model to identify the service level of RTD Park-N-Ride stations
print('TASK 2')
# Completed in ArcGIS Model Builder

# Mapping rule derives the total number of bus stations by taking the SUM of NumRoutes between all bus stations within
# a buffer polygon instead of just the NumRoute value of the FIRST listed bus station

# In the output spatial join shapefile, 'Join_Count' stores the number of bus stations in each buffer and 'NumRoutes'
# stores the number of bus routes of those bus stations in each buffer

# todo: TASK 3: Create a Python procedure to determine the service level of each RTD Park-N-Ride station
print('TASK 3')
# todo: 3a) Describe the ranking method
# HIGH SERVICE
# 4 or more bus stations
# 6 or more bus routes

# MEDIUM SERVICE
# 2 to 3 bus stations
# 3 to 5 bus routes

# LOW SERVICE
# 1 bus station or less
# 2 bus routes or less

# todo: 3b) In the feature class produced from Step 2, create a new field to store the results of ranking
# arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
in_table = 'Buffers.shp'
field_name = 'Service'
field_type = 'TEXT'
arcpy.management.AddField(in_table, field_name, field_type)

# todo: 3c) Use an UpdateCursor to update the values for the new field to store the rank of every Park-N-Ride station
#  based on the ranking method
# arcpy.da.UpdateCursor (in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {explicit}, {spatial_filter}, {spatial_relationship}, {search_order})
in_table = 'Buffers.shp'
field_names = ['NAME', 'Join_Count', 'NumRoutes', 'Service']
cursor = arcpy.da.UpdateCursor(in_table, field_names)

for row in cursor:
    if row[1] > 3 or row[2] > 5:
        row[3] = 'HIGH SERVICE'
    elif 2 <= row[1] <= 3 or 3 <= row[2] <= 5:
        row[3] = 'MEDIUM SERVICE'
    else:
        row[3] = 'LOW SERVICE'
    cursor.updateRow(row)
del row
del cursor

# todo: TASK 4: Create a Python procedure to identify Park-N-Ride stations of low service level
print('TASK 4')
# todo: 4a) Create an empty list to store the names of those stations. Create two variables to store the total number
#  of stations and the total number of low service stations. Use a SearchCursor to find stations.
Stations = []
numStations = 0
numLowService = 0

# arcpy.da.SearchCursor(in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {spatial_filter}, {spatial_relationship}, {search_order})
in_table = 'Buffers.shp'
field_names = ['NAME', 'Service']
cursor = arcpy.da.SearchCursor(in_table, field_names)

# todo: 4b) Create a loop to access the attribute information for every row.
# todo: 4c) Build an if-else block to determine if the service level of the station is low.
for row in cursor:
    name = row[0]
    service = row[1]
    numStations = numStations + 1
    # print(name + " - " + service) ## 4b
    if 'LOW SERVICE' in service:
        Stations.append(name)
        numLowService = numLowService + 1

print('LOW SERVICE stations: ' + str(Stations))
print('There are ' + str(numStations) + ' total stations')
print(str(numLowService) + ' stations are LOW SERVICE')

# todo: 4c) Save the names of the stations stored in the list to a text file
report = open('stationsList.txt', 'w')
result1 = 'LOW SERVICE stations include: ' + str(Stations)
result2 = 'There are ' + str(numStations) + ' total stations'
result3 = str(numLowService) + ' stations are LOW SERVICE'

report.write(result1 + '\n' + result2 + '\n' + result3)
report.close()

# todo: TASK 5: Create a complete map
print('TASK 5')
# Map completed in ArcGIS







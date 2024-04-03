# todo: Research Objective 1.1
# Find area of conservation easements in groups based on establishment date

import csv

import arcpy
from arcpy import env
env.overwriteOutput = True
env.workspace = r'E:\capstone_project\RO1\data'

# todo: Organize easements into establishment time ranges
# Add field
# arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
in_table = 'COL_Conserved_Prop_Bounds_202306.shp'
field_name = 'date_range'
arcpy.management.AddField(in_table, field_name, 'TEXT')

# todo: Add info to new field to sort into date ranges
# arcpy.da.UpdateCursor (in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {explicit}, {spatial_filter}, {spatial_relationship}, {search_order})
field_names = ['Name', 'Year', 'date_range', 'Acres_Calc']
cursor = arcpy.da.UpdateCursor(in_table, field_names)

for row in cursor:
    year = row[1]
    if year < 1990:
        row[2] = '1980_1989'
    elif 1989 < year < 2000:
        row[2] = '1990_1999'
    elif 1999 < year < 2010:
        row[2] = '2000_2009'
    elif 2009 < year < 2020:
        row[2] = '2010_2019'
    else:
        row[2] = '2020_2023'
    cursor.updateRow(row)

del cursor

# todo: Create new shapefiles and calculate area of easements that intersect with elk range for each date period
easements_layer = 'COL_Conserved_Prop_Bounds_202306.shp'
elk_range_layer = 'ElkOverallRange.shp'
# Create new list and populate with date ranges
# arcpy.da.SearchCursor(in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {spatial_filter}, {spatial_relationship}, {search_order})
date_ranges = []
in_table = 'COL_Conserved_Prop_Bounds_202306.shp'
field_names = ['date_range']
cursor = arcpy.da.SearchCursor(in_table, field_names)

for row in cursor:
    if row[0] not in date_ranges:
        date_ranges.append(row[0])

# todo: Iterate through each date range, create shapefiles, and perform calculations
# arcpy.analysis.Select(in_features, out_feature_class, {where_clause})
# arcpy.analysis.Intersect(in_features, out_feature_class, {join_attributes}, {cluster_tolerance}, {output_type})
change_in_elk_range = {}

for date_range in date_ranges:
    # Output shapefile name
    output_shapefile = str('Easements_' + (date_range) + '.shp')
    # Define the where clause based on the date range
    where_clause = "date_range = '" + str(date_range) + "'"
    # Create a new shapefile containing easements with the current date range
    # arcpy.Select_analysis(easements_layer, output_shapefile, where_clause)
    # Calculate the area of easements that intersect with the elk range for each date period
    intersect_output = str('Intersect_' + (date_range) + '.shp')
    # arcpy.analysis.Intersect([output_shapefile, elk_range_layer], intersect_output)
    # Calculate the total area of the intersected features (change in protected elk range)
    total_area = sum([row[0] for row in arcpy.da.SearchCursor(intersect_output, 'SHAPE@AREA')])
    # Store the change in protected elk range in the dictionary
    change_in_elk_range[date_range] = total_area

# todo: Write results to csv file
# Print the dictionary as a table and export to csv
protected_range_csv = r'E:\capstone_project\RO1\COL_protected_range'

# Conversion factor from square meters to acres
sq_meters_to_acres = 1 / 4046.86

# Sort the change_in_elk_range dictionary by date range in ascending order
sorted_changes = sorted(change_in_elk_range.items(), key=lambda x: x[0])

print(str('Acres of Protected Land added to Elk Range through COL Easements'))
with open(protected_range_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Date Range", "Acres of Protected Land added to Elk Range"])
    for date_range, change in sorted_changes:
        change_acres = change * sq_meters_to_acres  # Convert area from square meters to acres
        csvwriter.writerow([str(date_range), str(round(change_acres, 2))])
        print(str(date_range) + "\t" + str(change_acres))










# todo: CAPSTONE TOOL - Merge LCP Polylines and Perform Statistics
# Olivia Drukker

# Preparation
import arcpy
import os
from arcpy import env

# Get parameters
input_folder = arcpy.GetParameterAsText(0)  # Input folder containing LCP shapefiles
output_feature_class = arcpy.GetParameterAsText(1)     # Output merged feature class

# env.overwriteOutput = True
env.workspace = input_folder

# todo: ADD FIELD TO ALL LCP POLYLINES IN A FOLDER TO DENOTE ELK DATA ANALYSIS UNIT
field_name = 'elkDAU'
field_type = 'TEXT'

# List all feature classes in the workspace
# syntax: ListFeatureClasses ({wild_card}, {feature_type}, {feature_dataset})
feature_classes = arcpy.ListFeatureClasses()
# print(feature_classes)

# Create a for loop to iterate through all LCP shapefiles in folder, add elk DAU field, and populate field
# syntax: arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
# syntax: arcpy.management.CalculateField(in_table, field, expression, {expression_type}, {code_block}, {field_type}, {enforce_domains})
for feature_class in feature_classes: ## Iterate over each file in directory (folder)
    elk_unit = feature_class.split('_')[0] ## Split by underscore and take the first part
    arcpy.management.AddField(feature_class, field_name, field_type) ## Add field
    expression = "'{}'".format(elk_unit)  # Construct elk_unit as string expression
    arcpy.management.CalculateField(feature_class, field_name, expression, 'PYTHON3') ## Calculate field

# todo: MERGE LCPS INTO ONE FEATURE CLASS
# syntax: arcpy.management.Merge(inputs, output, {field_mappings}, {add_source})

inputs = arcpy.ListFeatureClasses() ## Use all LCP shapefiles in workspace
# output = r'E:\capstone_project\data\lcps.shp'

arcpy.management.Merge(inputs, output_feature_class)

# todo: STATISTICS
# Create a search cursor to view attribute info of new merged LCP feature class
# syntax: arcpy.da.SearchCursor(in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}, {datum_transformation}, {spatial_filter}, {spatial_relationship}, {search_order})
in_table = output_feature_class
field_names = ['LCP_Length', 'elkDAU']
cursor = arcpy.da.SearchCursor(in_table, field_names)

elk_counts = {} ## Create an empty dictionary to store count information for each analysis unit
elk_lengths = {} ## Create an empty dictionary to store length information for each analysis unit
total_length = 0 ## Create variable to store total length information

for row in cursor:
    elk_unit = row[1]  ## Extract the elk analysis unit from the row
    length = row[0]  # Extract the length of the polyline from the row
    # todo: Calculate the number of LCPs in each elk data analysis unit
    if elk_unit in elk_counts:
        elk_counts[elk_unit] += 1 ## If the elk unit already exists in the dictionary, add to the count
    else:
        elk_counts[elk_unit] = 1 ## If the elk unit does not exist in the dictionary, start the count at 1
    # todo: Calculate the length of LCPs for each elk analysis unit
    if elk_unit in elk_lengths:
        elk_lengths[elk_unit] += length ## If the elk unit exists in the dictionary, add the length to the total
    else:
        elk_lengths[elk_unit] = length ## If the elk unit does not exist in the dictionary, start the total length
    # todo: Calculate length of all LCPs
    length = row[0]
    total_length += length ## Add up lengths

# todo: Print statistics in ArcGIS tool
arcpy.AddMessage('Statistics Results:')
# Print the number of LCPs in each elk analysis unit
for elk_unit, count in elk_counts.items():
    arcpy.AddMessage('Elk Analysis Unit ' + str(elk_unit) + ': ' + str(count) + ' polylines')
# Print the total length of polylines for each elk analysis unit
for elk_unit, total_length in elk_lengths.items():
    arcpy.AddMessage('Elk Analysis Unit ' + str(elk_unit) + ' Total Length = ' + str(total_length) + ' meters')
# Print the total length of polylines
arcpy.AddMessage('Total Length of all Polylines: ' + str(total_length) + ' meters')

del cursor
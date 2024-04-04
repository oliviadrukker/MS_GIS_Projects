// Burn Severity Assessment 
// Google Earth Engine
// Pack Creek Fire, La Sal Mountains, 2021 
// Fire began June 9th; Fully contained July 10

//*******************************************************************************************
// Imports

var S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED"),
    perimeter_buffer = ee.FeatureCollection("users/oliviadrukker/PackCreekFire_2kmBuffer"),
    perimeter = ee.FeatureCollection("users/oliviadrukker/PackCreekFire_Perimeter"),
    Rectangle = 
    /* color: #ffffff */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-109.4146417150306, 38.532748052184985],
          [-109.4146417150306, 38.39295876945226],
          [-109.17809233758919, 38.39295876945226],
          [-109.17809233758919, 38.532748052184985]]], null, false);

//*******************************************************************************************
// SELECT STUDY AREA   

// Upload shapefile of fire perimeter and import into script - 'perimeter'
// Upload shapefile of 2km fire perimeter buffer and import into script - 'geometry'

// Location
var area = ee.FeatureCollection(perimeter_buffer);

// Set study area as map center
Map.centerObject(perimeter_buffer);

//*******************************************************************************************
// FILTER PRE FIRE IMAGES

// Filter PRE-FIRE Sentinel 2 image by location and date
var s_prefireImage1 = S2
  .filterBounds(Map.getCenter())
  .filterDate('2021-05-20', '2021-06-01') // // Image taken May 24 (most recent cloud-free image to fire)
  .first();
  
// Get the image projection
var prefireProj = s_prefireImage1.select('B4')
    .projection();
print('prefire projection', prefireProj); // // EPSG:32612 - WGS 84 / UTM zone 12N

//*******************************************************
// PRE FIRE NATURAL COLOR AND COLOR INFRARED IMAGES

// Display the PRE-FIRE Sentinel 2 image as a NATURAL COLOR
Map.addLayer(s_prefireImage1, {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 2000
}, 'Pre-Fire Natural Color');

// // Display the PRE-FIRE Sentinel 2 image as a COLOR INFRARED
// Map.addLayer(s_prefireImage1, {
//   bands: ['B8', 'B4', 'B3'],
//   min: 0,
//   max: 2000
// }, 'Pre-Fire Color Infrared');

//*******************************************************
// PRE FIRE NORMALIZED DIFFERENCE VEGETATION INDEX - NDVI 
// NDVI = (B8 - B4) / (B8 + B4)

// Calculate NDVI using Normalized Difference
var pre_ndvi = s_prefireImage1.normalizedDifference(['B8', 'B4']);

// Add layer to map with a color pallete 
var vegPalette = ['red', 'white', 'green'];
Map.addLayer(pre_ndvi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Pre-Fire NDVI');

//*******************************************************
// PRE FIRE ENHANCED VEGETATION INDEX - EVI
// EVI = ((NIR - Red) * 2.5) / (NIR + (Red * 6) - (Blue * 7.5) + 1)

// Extract the nir, red, and blue bands and divide by 10000 to account for scaling
var pre_nir = s_prefireImage1.select('B8').divide(10000);
var pre_red = s_prefireImage1.select('B4').divide(10000);
var pre_blue = s_prefireImage1.select('B2').divide(10000);

// Calculate numerator and denominator 
var pre_evi_numerator = (pre_nir.subtract(pre_red)).multiply(2.5);
var pre_evi_denominatorClause1 = pre_red.multiply(6);
var pre_evi_denominatorClause2 = pre_blue.multiply(7.5);
var pre_evi_denominator = pre_nir.add(pre_evi_denominatorClause1).subtract(pre_evi_denominatorClause2).add(1);

// Calculate EVI
var pre_evi = pre_evi_numerator.divide(pre_evi_denominator)

// Add layer to map with a color pallete 
Map.addLayer(pre_evi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Pre-Fire EVI');

//*******************************************************
// PRE FIRE SOIL ADJUSTED VEGETATION INDEX - SAVI 
// SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
// where L is the soil brightness correction factor

// Define the soil brightness correction factor (typical value is 0.5)
var L = 0.5;

// Calculate SAVI
var pre_savi_numerator = pre_nir.subtract(pre_red);
var pre_savi_denominator = pre_nir.add(pre_red).add(L);
var pre_savi = pre_savi_numerator.divide(pre_savi_denominator).multiply(1 + L);

// Add layer to map with a color palette 
Map.addLayer(pre_savi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Pre-Fire SAVI');

//*******************************************************
// PRE FIRE NORMALIZED BURN RATIO - NBR
// NBR = (B8 - B12) / (B8 + B12)

// Extract the nir and swir2 band
var pre_nir = s_prefireImage1.select('B8')
var pre_swir2 = s_prefireImage1.select('B12');

// Calculate numerator and denominator
var pre_nbr_numerator = pre_nir.subtract(pre_swir2);
var pre_nbr_denominator = pre_nir.add(pre_swir2);

// Calculate NBR
var pre_nbr = pre_nbr_numerator.divide(pre_nbr_denominator); 

// Add layer to map with a color pallete 
var burnPalette = ['orange', 'white', 'purple'];
Map.addLayer(pre_nbr, {
    min: -1,
    max: 1,
    palette: burnPalette
}, 'Pre-Fire NBR');

//*******************************************************************************************
// FILTER MID FIRE IMAGES 

// Filter MID-FIRE Sentinel 2 image by location and date
var s_midfireImage1 = S2
  .filterBounds(Map.getCenter())
  .filterDate('2021-06-09', '2021-06-25') // // Image taken June 13
  .first();

//*******************************************************
// MID FIRE NATURAL COLOR AND COLOR INFRARED IMAGES

// Display the MID-FIRE Sentinel 2 image as a NATURAL COLOR
Map.addLayer(s_midfireImage1, {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 2000
}, 'Mid-Fire Natural Color');

// // // Display the MID-FIRE Sentinel 2 image as a COLOR INFRARED
// // Map.addLayer(s_midfireImage1, {
// //   bands: ['B8', 'B4', 'B3'],
// //   min: 0,
// //   max: 2000
// // }, 'Mid-Fire Color Infrared');

//*******************************************************
// MID FIRE NORMALIZED DIFFERENCE VEGETATION INDEX - NDVI 
// NDVI = (B8 - B4) / (B8 + B4)

// Calculate NDVI using Normalized Difference
var mid_ndvi = s_midfireImage1.normalizedDifference(['B8', 'B4']);

// Add layer to map with a color pallete 
Map.addLayer(mid_ndvi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Mid-Fire NDVI');

//*******************************************************
// MID FIRE ENHANCED VEGETATION INDEX - EVI
// EVI = ((NIR - Red) * 2.5) / (NIR + (Red * 6) - (Blue * 7.5) + 1)

// Extract the nir, red, and blue bands and divide by 10000 to account for scaling
var mid_nir = s_midfireImage1.select('B8').divide(10000);
var mid_red = s_midfireImage1.select('B4').divide(10000);
var mid_blue = s_midfireImage1.select('B2').divide(10000);

// Calculate numerator and denominator 
var mid_evi_numerator = (mid_nir.subtract(mid_red)).multiply(2.5);
var mid_evi_denominatorClause1 = mid_red.multiply(6);
var mid_evi_denominatorClause2 = mid_blue.multiply(7.5);
var mid_evi_denominator = mid_nir.add(mid_evi_denominatorClause1).subtract(mid_evi_denominatorClause2).add(1);

// Calculate EVI 
var mid_evi = mid_evi_numerator.divide(mid_evi_denominator)

// Add layer to map with a color pallete 
Map.addLayer(mid_evi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Mid-Fire EVI');

//*******************************************************
// MID FIRE SOIL ADJUSTED VEGETATION INDEX - SAVI 
// SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
// where L is the soil brightness correction factor (0.5)

// Calculate SAVI 
var mid_savi_numerator = mid_nir.subtract(mid_red);
var mid_savi_denominator = mid_nir.add(mid_red).add(L);
var mid_savi = mid_savi_numerator.divide(mid_savi_denominator).multiply(1 + L);

// Add layer to map with a color palette 
Map.addLayer(mid_savi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Mid-Fire SAVI');

//*******************************************************
// MID FIRE NORMALIZED BURN RATIO
// NBR = (B8 - B12) / (B8 + B12)

// Extract the nir and swir2 bands.
var mid_nir = s_midfireImage1.select('B8');
var mid_swir2 = s_midfireImage1.select('B12');

// Calculate numerator and denominator
var mid_numerator = mid_nir.subtract(mid_swir2);
var mid_denominator = mid_nir.add(mid_swir2);

// Calculate NBR
var mid_nbr = mid_numerator.divide(mid_denominator); 

// Add layer to map with a color pallete 
var burnPalette = ['orange', 'white', 'purple'];
Map.addLayer(mid_nbr, {
    min: -1,
    max: 1,
    palette: burnPalette
}, 'Mid-Fire NBR');

//*******************************************************************************************
// FILTER POST FIRE IMAGES 

// Filter POST-FIRE Sentinel 2 image by location and date
var s_postfireImage1 = S2
  .filterBounds(Map.getCenter())
  .filterDate('2021-08-10', '2021-08-15') // // Image taken July 12
  .first();

//*******************************************************
// POST FIRE NATURAL COLOR AND COLOR INFRARED IMAGES 

// Display the POST-FIRE Sentinel 2 image as a NATURAL COLOR
Map.addLayer(s_postfireImage1, {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 2000
}, 'Post-Fire Natural Color');

// // Display the POST-FIRE Sentinel 2 image as a COLOR INFRARED
// Map.addLayer(s_postfireImage1, {
//   bands: ['B8', 'B4', 'B3'],
//   min: 0,
//   max: 2000
// }, 'Post-Fire Color Infrared');

//*******************************************************
// POST FIRE NORMALIZED DIFFERENCE VEGETATION INDEX - NDVI 
// NDVI = (B8 - B4) / (B8 + B4)

// Calculate NDVI using Normalized Difference
var post_ndvi = s_postfireImage1.normalizedDifference(['B8', 'B4']);

// Add layer to map with a color pallete 
Map.addLayer(post_ndvi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Post-Fire NDVI');

//*******************************************************
// POST FIRE ENHANCED VEGETATION INDEX - EVI
// EVI = ((NIR - Red) * 2.5) / (NIR + (Red * 6) - (Blue * 7.5) + 1)

// Extract the nir, red, and blue bands and divide by 10000 to account for scaling
var post_nir = s_postfireImage1.select('B8').divide(10000);
var post_red = s_postfireImage1.select('B4').divide(10000);
var post_blue = s_postfireImage1.select('B2').divide(10000);

// Calculate numerator and denominator 
var post_evi_numerator = (post_nir.subtract(post_red)).multiply(2.5);
var post_evi_denominatorClause1 = post_red.multiply(6);
var post_evi_denominatorClause2 = post_blue.multiply(7.5);
var post_evi_denominator = post_nir.add(post_evi_denominatorClause1).subtract(post_evi_denominatorClause2).add(1);

// Calculate EVI 
var post_evi = post_evi_numerator.divide(post_evi_denominator)

// Add layer to map with a color pallete 
Map.addLayer(post_evi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Post-Fire EVI');

//*******************************************************
// PRE FIRE SOIL ADJUSTED VEGETATION INDEX - SAVI 
// SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
// where L is the soil brightness correction factor (0.5)

// Calculate SAVI 
var post_savi_numerator = post_nir.subtract(post_red);
var post_savi_denominator = post_nir.add(post_red).add(L);
var post_savi = post_savi_numerator.divide(post_savi_denominator).multiply(1 + L);

// Add layer to map with a color palette 
Map.addLayer(post_savi, {
    min: -1,
    max: 1,
    palette: vegPalette
}, 'Post-Fire SAVI');

//*******************************************************
// POST FIRE NORMALIZED BURN RATIO
// NBR = (B8 - B12) / (B8 + B12)

// Extract the nir and swir2 bands.
var post_nir = s_postfireImage1.select('B8');
var post_swir2 = s_postfireImage1.select('B12');

// Calculate numerator and denominator
var post_numerator = post_nir.subtract(post_swir2);
var post_denominator = post_nir.add(post_swir2);

// Calculate NBR
var post_nbr = post_numerator.divide(post_denominator); 

// Add layer to map with a color pallete 
Map.addLayer(post_nbr, {
    min: -1,
    max: 1,
    palette: burnPalette
}, 'Post-Fire NBR');


//*******************************************************************************************
// BURN SEVERITY -- DIFFERENCE IN NBR -- dNBR
// dNBR = preFireNBR - postFireNBR 

var dnbr_unscaled = pre_nbr.subtract(post_nbr);
var dnbr = dnbr_unscaled.multiply(1000) // Scale to meet USGS standards 

// Add layer to map with a color pallette 
var dnbr_Palette = ['orange', 'white', 'purple'];
Map.addLayer(dnbr, {
    min: -1000,
    max: 1000,
    palette: dnbr_Palette
}, 'dNBR');

// Intervals from UN-SPIDER Knowledge Portal 
var sld_intervals =
  '<RasterSymbolizer>' +
    '<ColorMap type="intervals" extended="false" >' +
      '<ColorMapEntry color="#ffffff" quantity="-500" label="-500"/>' +
      '<ColorMapEntry color="#7a8737" quantity="-250" label="-250" />' +
      '<ColorMapEntry color="#acbe4d" quantity="-100" label="-100" />' +
      '<ColorMapEntry color="#0ae042" quantity="100" label="100" />' +
      '<ColorMapEntry color="#fff70b" quantity="270" label="270" />' +
      '<ColorMapEntry color="#ffaf38" quantity="440" label="440" />' +
      '<ColorMapEntry color="#ff641b" quantity="660" label="660" />' +
      '<ColorMapEntry color="#a41fd6" quantity="2000" label="2000" />' +
    '</ColorMap>' +
  '</RasterSymbolizer>';
  
// Add the image to the map using both the color ramp and interval schemes.
Map.addLayer(dnbr.sldStyle(sld_intervals), {}, 'dNBR classified');

// Look at image clipped to the fire perimeter 
// Add fire perimeter polygon as a layer
var studyArea = ee.FeatureCollection(perimeter);
var dnbr_clipped = dnbr.clip(studyArea);
  
Map.addLayer(dnbr_clipped.sldStyle(sld_intervals), {}, 'dNBR classified clipped');

// // *******************************************************
// // EXTRACT BURNED AREA PIXEL INFORMATION TO A CSV

// var dnbr_pixels = dnbr.sampleRegions(studyArea);
// Export.table.toDrive(dnbr_pixels); // CSV by default

//*******************************************************************************************
// ADD FIRE PERIMETER AND RECTANGLE AS LAST VISIBLE LAYER 

// Add fire perimeter polygon as a layer
var studyArea = ee.FeatureCollection(perimeter);

// Style the fire perimeter polygon with a black outline and transparent interior
var styledStudyArea = studyArea.style({
  fillColor: '00000000', // Transparent fill color
  color: '000000', // Black outline color
  width: 2 // Outline width in pixels
});

Map.addLayer(styledStudyArea, {}, 'Fire Perimeter');



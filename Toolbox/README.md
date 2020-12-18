# Terrain Aware Toolbox

## Create Terrain Aware Layers
This tool is the core of the toolbox. It’s the heavy lifter and creates all of the terrain aware data framework that is needed to render the cartographic outputs. The steps involved largely follow those outlined in [this walkthrough](https://warrenrdavison.wixsite.com/maps/post/revisiting-hachure-lines-dynamic-hachure-contours-in-arcgis-pro) with the exception of a few enhancements that were implemented in the process of scripting the python tool.

### Parameters
###### Notes

### Processing Steps
1.	Smoothes the DEM using a Focal Statistics Mean operation with the neighbourhood circle size dictated by the input parameter.
2.	Creates a Slope and Aspect raster from the smoothed DEM.
3.	Extracts cells from the Slope raster where their value is less than 5 degrees (low slope areas) these will be omitted in further processing.
4.	Slices the Slope raster to reclassify the values using Natural Breaks as the classification scheme.
5.	Reclassifies the Aspect raster into 30 degree increments assigning the increment that contains the Azimuth parameter a value of '1' and the adjacent zones an increasing value up to '7'.
6.	Filters both the Slope and Aspect rasters with a Majority Filter operation.
7.	Cleans both the Slope and Aspect rasters with a Boundary Clean operation.
8.	Groups both the Slope and Aspect rasters with a Region Group operation.
9.	Extracts regions that are smaller than the area dictated by the Minimum Polygon Area parameter.
10.	Nibbles both the Slope and Aspect rasters to fill in the regions that were removed by the extract operation.
11.	Converts both the Slope and Aspect rasters to polygons and renames/removes some fields for clarity.
12.	Unions the new Slope and Aspect polygons to create a new terrain polygon layer.
13.	Creates contour lines from the smoothed DEM.
14.	Intersects the contour lines with the terrain polygons to transfer Slope and Aspect attributes to the contour lines.


## Style Terrain Aware Layers
Once the terrain aware layers have been generated, you can use this tool to apply one of the [predefined styles](https://github.com/WarrenDz/terrain-aware/tree/main/Styles). The tool updates the styling of the tool with one of the available styles, based on the geometry of the terrain aware layer, and attempts to adjust the rendering settings to adjust for the intended map scale.

The styles I've included are just samples that I've dreamt up while experimenting, but they showcase some of the possibilities and are useful examples of how the effects can be configured. Try them out, break open the expressions and see how they impact the rendering, and try to tweak them for your own use!

All of the styles included with this toolbox rely on [Attribute-driven Symbology](https://pro.arcgis.com/en/pro-app/latest/help/mapping/layer-properties/attribute-driven-symbology.htm) and make extensive use of [Arcade Expressions](https://developers.arcgis.com/arcade/) to modulate how symbology is rendered. Using these techniques features can be rendered with relatively few symbology layers that are dynamic thanks to the logic of the expressions. The greatest benefit is that the geoprocessing tool can be run once for your area of interest and the rendering can be endlessly configured without having to re-run the processing steps.

### Parameters
###### Notes

# Development Goals
- [x] Correct the `slope_min` criteria of the Swiss-ish layer file to fix the "broken contours" in low slope areas.
- [ ] Author a `elevation_subset` modifier expression that can be applied to various expressions that allows the user to apply a 'defintion query` and only render specific contour intervals of the _'terrain-aware'_ contours.
- [ ] Review the `updateParameters` method of the `CreateTerrainAwareLayers` tool. Prevent the tool overriding a user supplied `minimum_polygon_area` input with the default value.
- [ ] Review all arcade expressions and ensure the default value is supplied as `Text(0)`. This will resolve odd cases when the symbol panel expects the parameter as text vs integer.
- [ ] Review all arcade expressions and convert any instances of technique parameters ex. `hachure_min` to a more consistent `render_min`. This will allow for consistent code if Cartography Information Model (CIM) is achieved.
- [ ] Determine if `arcpy.ApplySymbologyFromLayer_management(in_layer=in_layer, in_symbology_layer=stylePath)` is achievable from python within the `StyleTerrainAwareLayers` tool (appears to be a bug as per BUG-000106281, BUG-000108497).
  - [ ] If we can apply symbology from python, determine if there is a loose `scaling_factor` or relationship between `map scale` and `render parameters`. If so, we can estimate the render settings based on the scale provided by the user as an input to the tool.
  - [ ] With a calculated `scaling_factor` we could access the arcade expressions within the layer file and update the `render parameters` prior to applying the layer file to a layer in the map (this is primarily applicable when the user does not set a `reference scale` and intends to author the map at a scale other than `1:24,000`).

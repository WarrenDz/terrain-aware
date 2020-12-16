# ---------------------------------------------------------------------------
# TerrainAwarenessToolbox.py
# version 1.0 - 2020/12/03
#
# This toolbox was inspired by the Terrain Tools toolbox created by Kenneth Field and Linda Beale, Esri Inc.
#  https://arcg.is/1L9jGO
#
# This technique was built on the methods created by: John Nelson, Esri Inc.
# https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/landscape-map-in-the-spirit-of-erwin-raisz/
#
# Incremental improvements were implemented by: Warren Davison, Esri Inc. including
# the application of a dynamic hachure style symbology.
# https://warrenrdavison.wixsite.com/maps/post/revisiting-hachure-lines-dynamic-hachure-contours-in-arcgis-pro
#
# Description:
# Generates a set of contour lines from a DEM (Digitial Elevation Model) that
# have been enhanced with additional aspects of the terrain, including slope
# and aspect. Through the addition of these attributes the contours become
# 'terrain-aware' and can be styled using a variety of symbology techniques.
# ---------------------------------------------------------------------------

import os, sys
import arcpy
from arcpy.sa import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Terrain Aware Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CreateTerrainAwareLayers, StyleTerrainAwareLayer] ## Would like to comment out style tool until a workaround is found for ApplySymbologyFromLayer


class CreateTerrainAwareLayers(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Terrain Aware Layers"
        self.description = "Generates contour lines and terrain polygons that are enhanced with an 'awareness' of " \
                           "other topographic attributes of the terrain including, slope and aspect. These additional " \
                           "characteristics can be used in symbology for depicting the contours using a number " \
                           "relief techniques."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="DEM",
            name="in_dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Output Contours",
            name="contours",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        # Third parameter
        param2 = arcpy.Parameter(
            displayName="Output Terrain Polygons",
            name="polygons",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        # Fourth parameter
        param3 = arcpy.Parameter(
            displayName="Processing Extent",
            name="map_extent",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # Restrict the inputs to one of two options
        param3.filter.list = ["DEM_EXTENT", "LAYER_EXTENT", "DISPLAY_EXTENT"]
        param3.value = "DEM_EXTENT"

        # Fifth parameter
        param4 = arcpy.Parameter(
            displayName="Extent Layer",
            name="extent_layer",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        # Restrict the Cartographic extent input to a polygon feature layer
        param4.filter.list = ["Polygon"]

        # Sixth parameter
        param5 = arcpy.Parameter(
            displayName="Minimum Terrain Polygon Area",
            name="min_poly_area",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        # Seventh parameter
        param6 = arcpy.Parameter(
            displayName="Smoothing Neighbourhood",
            name="focal_nbhd",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        # Set the default value to a cell neighbourhood of 10
        param6.value = "10"

        # Eighth parameter
        param7 = arcpy.Parameter(
            displayName="Azimuth Angle",
            name="azimuth",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        # Set the default azimuth angle (light source) to 315-upper left
        param7.value = "315"
        # Filter the allowable values for the azimuth to 0 - 360 degrees
        param7.filter.type = "Range"
        param7.filter.list = [0, 360]

        parameters = [param0, param1, param2, param3, param4, param5, param6, param7]

        return parameters

    def isLicensed(self):
        """Allow the tool to execute, only if the ArcGIS Spatial Analyst extension
        is available."""
        try:
            if arcpy.CheckExtension("Spatial") != "Available":
                raise Exception
        except Exception:
            return False  # tool cannot be executed

        return True  # tool can be executed

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Define a variable to keep the scaling consistent
        # this value dictates the percent of total area (DEM extent) that will be used to default the min_polygon_size
        pct_area = 0.0000075

        # Set the default minimum area size to be some tiny percentage of the input feature.
        """Using this method, it's possible to take a dynamic 'best guess' at the amount of generalization.
        # Do not set if there is no input feature yet, or if there is a custom area specified (Altered is true)."""

        # Control vis of layer input
        if parameters[3].valueAsText == "LAYER_EXTENT":
            parameters[4].enabled = True
        else:
            parameters[4].enabled = False

        # Hmmmmmm...
        """Stumped here on a method to update the min_area when the parameters are changed but not when a user overwrites it..."""
        # Calculate minimum area based on DEM extent
        if parameters[3].valueAsText == "DEM_EXTENT" and parameters[0].altered and not parameters[0].valueAsText == "":
            desc = arcpy.Describe(parameters[0].valueAsText)
            min_area = round(((desc.extent.XMax - desc.extent.XMin) * (desc.extent.YMax - desc.extent.YMin)) * pct_area,
                             0)
            # Set the default minimum area
            parameters[5].value = min_area
        else:
            pass

        # Calculate minimum area based on layer extent
        if parameters[3].valueAsText == "LAYER_EXTENT" and parameters[4].altered and not parameters[
                                                                                             4].valueAsText == "":
            fc = parameters[4].valueAsText
            area = [row[0] for row in arcpy.da.SearchCursor(fc,['SHAPE@AREA'])]
            min_area = round(area[0] * pct_area, 0)
            parameters[5].value = min_area
        else:
            pass

        if parameters[3].valueAsText == "DISPLAY_EXTENT":
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            mv = aprx.activeView
            ext = mv.camera.getExtent()
            min_area = round(((ext.XMax - ext.XMin) * (ext.YMax - ext.YMin)) * pct_area,
                             0)
            parameters[5].value = min_area
        else:
            pass

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # Clear messages

        # Provide an info warning if DEM is selected that it needs to align to area of interest
        if parameters[3].valueAsText == "DEM_EXTENT":
            parameters[3].setWarningMessage(
                "Ensure that the input DEM aligns with the intended area of interest. Using a DEM that greatly exceeds the area of interest may include terrain features that could skew the Slope/Aspect values assigned in the contours")
        else:
            pass

        # Ensure that the minimum_polygon_area is greater than 0
        if parameters[5].altered:
            if int(parameters[5].value) < 0:
                parameters[5].setErrorMessage("A positive area value is required. Please specify an area measure.")
            else:
                pass
        else:
            pass

        # Ensure that the focal neighbourhood is greater than 0
        if parameters[6].altered:
            if int(parameters[6].value) < 1:
                parameters[6].setErrorMessage(
                    "A positive neighbourhood value is required. Please specify an cell neighbourhood measure.")
            else:
                pass
        else:
            pass

        # Ensure that the cartographic extent layer has a value
        if parameters[2].valueAsText == "LAYER_EXTENT" and not parameters[4].altered or parameters[4].valueAsText == "":
            parameters[4].setErrorMessage(
                "A layer is required when the Processing Extent has been set to LAYER_EXTENT. Please select a layer from the dropdown to restrict the output processing results.")
        else:
            pass

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Gather parameters
        in_dem = parameters[0].valueAsText
        out_contours = parameters[1].valueAsText
        out_polygons = parameters[2].valueAsText
        map_extent = parameters[3].valueAsText
        extent_layer = parameters[4].valueAsText
        min_poly_area = parameters[5].value
        nbhd = parameters[6].value
        azimuth_angle = parameters[7].value

        # Assign the default workspace based on contour output location
        out_dir = os.path.dirname(out_contours)
        arcpy.env.workspace = out_dir
        arcpy.env.overwriteOutput = True

        # Set extent environment variable to match that of parameters
        if map_extent == "DEM_EXTENT":
            desc = arcpy.Describe(in_dem)
            arcpy.env.extent = "{}, {}, {}, {}".format(desc.extent.XMin, desc.extent.YMin, desc.extent.XMax,
                                                       desc.extent.YMax)
            print("{}, {}, {}, {}".format(desc.extent.XMin, desc.extent.YMin, desc.extent.XMax,
                                                       desc.extent.YMax))
        elif map_extent == "EXTENT_LAYER":
            desc = arcpy.Describe(extent_layer)
            arcpy.env.extent = "{}, {}, {}, {}".format(desc.extent.XMin, desc.extent.YMin, desc.extent.XMax,
                                                       desc.extent.YMax)
        elif map_extent == "DISPLAY_EXTENT":
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            mv = aprx.activeView
            ext = mv.camera.getExtent()
            arcpy.env.extent = "{}, {}, {}, {}".format(ext.XMin, ext.YMin, ext.XMax, ext.YMax)

        try:
            # Check out the Spatial Analyst license for this script
            arcpy.CheckOutExtension("Spatial")

            # SMOOTH DEM
            """Smoothing the input DEM is good practice. It creates a smoother terrain surface and
            reduces the potential of creating highly fragmented aspect & slope outputs."""

            arcpy.AddMessage("Smoothing DEM...")
            """might be able to implement a number of passes here... implement a scratchname for sequentialruns"""
            smooth_dem = arcpy.sa.FocalStatistics(in_raster=in_dem, neighborhood="Circle {0} CELL".format(nbhd),
                                                  statistics_type="MEAN", ignore_nodata="DATA")

            # CREATE TERRAIN RASTERS
            """Generating a slope and aspect raster based on smoothed DEM."""
            arcpy.AddMessage("Generating terrain rasters...")
            arcpy.AddMessage("...Creating slope raster...")
            slope_raster = arcpy.sa.Slope(in_raster=smooth_dem, output_measurement="DEGREE")
            arcpy.AddMessage("...Creating aspect raster...")
            aspect_raster = arcpy.sa.Aspect(in_raster=smooth_dem)

            # PROCESS TERRAIN RASTERS
            """Processing our slope and aspect rasters to reclassify. Will consolidate cell values down to range from
            1-7."""
            arcpy.AddMessage("Processing terrain rasters...")

            # Slice slope raster
            """Using the slice here as it essentially does the same as a reclassify with the exception of being
            able to segment the data in the raster using a classification scheme."""
            arcpy.AddMessage("...Slicing slope raster...")
            # Omit areas of low slope
            extract_slope = arcpy.sa.ExtractByAttributes(in_raster=slope_raster, where_clause="Value > 5")
            del slope_raster
            reclass_slope = arcpy.sa.Slice(in_raster=extract_slope, number_zones=7, slice_type="NATURAL_BREAKS")
            del extract_slope

            # Reclassify aspect raster
            """Processing the aspect is slightly more complex. Since the tool allows for the user to define the
            azimuth we need to be able to reclass based on an initial reference point (the selected azimuth).
            Adjacent 30 degree increment zones will then be assigned a progressively greater value
            (both clockwise and counter-clockwise)."""

            # shade_list contains the values we'd like to eventually assign to our 30 degree zones.
            shade_list = [1, 2, 3, 4, 5, 6, 7]

            # aspect_dict contains a initial index of azimuth ranges that will form the upper/lower values of our reclassification table
            aspect_dict = {0: [0, 30], 1: [31, 60], 2: [61, 90], 3: [91, 120], 4: [121, 150], 5: [151, 180],
                           6: [181, 210], 7: [211, 240], 8: [241, 270], 9: [271, 300], 10: [301, 330], 11: [331, 360]}

            arcpy.AddMessage("...Mapping aspect values based on reference azimuth...")
            # This loop determine which key, value pair best represents the azimuth selected by the user.
            # The aspect_index value assigned as a reference point for determining the remapping of adjacent azimuth zones
            for a in aspect_dict:
                if aspect_dict[a][0] < azimuth_angle < aspect_dict[a][1]:
                    aspect_index = a
                else:
                    pass

            # Now loop the aspect list using our reference index to create our ranges for remapping
            aspect_loop = 0
            # aspect_remap is an empty container that will be populated with our remapping values using the for loop below.
            aspect_remap = []

            # This loop iterates through the potential 'shadiness' assignments and gathers the appropriate azimuth 'bookends' to add to the remapping table.
            for s in shade_list:
                # First loop
                if aspect_loop == 0:
                    aspect_remap.append(
                        ["{0}, {1}, {2}".format(aspect_dict[aspect_index][0], aspect_dict[aspect_index][1], s)])

                # Last loop
                elif aspect_loop == 6:
                    if aspect_index + aspect_loop > 11:
                        aspect_remap.append(["{0}, {1}, {2}".format(
                            aspect_dict[abs((aspect_index + aspect_loop) - 12)][0],
                            aspect_dict[abs((aspect_index + aspect_loop) - 12)][1], s)])
                    else:
                        aspect_remap.append(["{0}, {1}, {2}".format(aspect_dict[aspect_index + 7][0],
                                                                    aspect_dict[aspect_index + 7][1], s)])

                # Any other loop
                else:
                    # Assign with this logic if the index would become a negative number by subtracting our loop increment
                    if aspect_index - aspect_loop < 0:
                        aspect_remap.append(["{0}, {1}, {2}".format(
                            aspect_dict[abs(12 - (aspect_index + aspect_loop))][0],
                            aspect_dict[abs(12 - (aspect_index + aspect_loop))][1], s)])
                        aspect_remap.append(["{0}, {1}, {2}".format(aspect_dict[aspect_index + aspect_loop][0],
                                                                    aspect_dict[aspect_index + aspect_loop][1], s)])

                    # Assign with this logic if the index would exceed our dictionary items by adding our loop increment
                    elif aspect_index + aspect_loop > 11:
                        aspect_remap.append(["{0}, {1}, {2}".format(
                            aspect_dict[abs((aspect_index + aspect_loop) - 12)][0],
                            aspect_dict[abs((aspect_index + aspect_loop) - 12)][1], s)])
                        aspect_remap.append(["{0}, {1}, {2}".format(aspect_dict[aspect_index - aspect_loop][0],
                                                                    aspect_dict[aspect_index - aspect_loop][1], s)])

                    # Assign with this logic if our index and increment end up within the bounds of our dictionary items
                    else:
                        aspect_remap.append(["{0}, {1}, {2}".format(aspect_dict[aspect_index - aspect_loop][0],
                                                                    aspect_dict[aspect_index - aspect_loop][1], s)])
                        aspect_remap.append(["{0}, {1}, {2}".format(aspect_dict[aspect_index + aspect_loop][0],
                                                                    aspect_dict[aspect_index + aspect_loop][1], s)])

                # Increment the loop counter for the next run
                aspect_loop += 1

            # Aspect remapping range table
            arcpy.AddMessage("...Aspect ranges remapped: {0}".format(aspect_remap))

            arcpy.AddMessage("...Reclassifying aspect raster...")
            reclass_aspect = arcpy.sa.Reclassify(in_raster=aspect_raster, reclass_field="Value",
                                                 remap=RemapRange(aspect_remap), missing_values="NODATA")
            del aspect_raster

            # GENERALIZATION OF TERRAIN RASTERS
            """The following steps aim to generalize the terrain rasters. Through generalizing we omit small clusters
            of cells that wouldn't contribute to the overall visual effect and also minimize the fragmentation
            of our future terrain polygons. Ultimately, this improves the rendering of the contour
            lines and simplifies the output."""

            arcpy.AddMessage("Generalizing terrain rasters...")

            # Majority Filter
            arcpy.AddMessage("...Performing Majority Filter on terrain rasters...")
            majority_slope = arcpy.sa.MajorityFilter(in_raster=reclass_slope, number_neighbors="EIGHT",
                                                     majority_definition="HALF")
            del reclass_slope
            majority_aspect = arcpy.sa.MajorityFilter(in_raster=reclass_aspect, number_neighbors="EIGHT",
                                                      majority_definition="HALF")
            del reclass_aspect

            # Boundary Clean
            arcpy.AddMessage("...Performing Boundary Clean on terrain rasters...")
            boundary_slope = arcpy.sa.BoundaryClean(in_raster=majority_slope, sort_type="DESCEND",
                                                    number_of_runs="TWO_WAY")
            del majority_slope
            boundary_aspect = arcpy.sa.BoundaryClean(in_raster=majority_aspect, sort_type="DESCEND",
                                                     number_of_runs="TWO_WAY")
            del majority_aspect

            # Region Group
            arcpy.AddMessage("...Performing Region Group on terrain rasters...")
            region_slope = arcpy.sa.RegionGroup(in_raster=boundary_slope, number_neighbors="FOUR",
                                                zone_connectivity="WITHIN", add_link="ADD_LINK")
            region_slope.save("RegionSlope")
            region_aspect = arcpy.sa.RegionGroup(in_raster=boundary_aspect, number_neighbors="FOUR",
                                                 zone_connectivity="WITHIN", add_link="ADD_LINK")
            region_aspect.save("RegionAspect")

            # Extract by Attributes
            """Convert our minimum area threshold to a count of cells within the raster based on cell size.
            This conversion will be used to extract regions from the raster that satisfy our minimum polygon area. """
            arcpy.AddMessage("...Performing Extract by Attributes on terrain rasters...")

            # Gather cell size properties
            cell_size_x_Result = arcpy.GetRasterProperties_management(in_raster=in_dem, property_type="CELLSIZEX")
            cell_size_y_Result = arcpy.GetRasterProperties_management(in_raster=in_dem, property_type="CELLSIZEY")
            cell_size_x = float(cell_size_x_Result.getOutput(0))
            cell_size_y = float(cell_size_y_Result.getOutput(0))

            # Determine single cell area of raster
            cell_area = cell_size_x * cell_size_y

            # Convert min_poly_area to a count of cells that represent that same area.
            min_cell_count = round((min_poly_area / cell_area), 0)
            arcpy.AddMessage(
                "...Extracting regions with less than {} cells. This cell group was calculated using a cell size of {} x {} (area: {}) and minimum polygon area of: {}...".format(
                    min_cell_count, round(cell_size_x, 2), round(cell_size_y, 2), round(cell_area, 2), min_poly_area))

            # Create selection expression
            select_expr = "Count > {0}".format(min_cell_count)
            extract_slope = arcpy.sa.ExtractByAttributes(in_raster=region_slope, where_clause=select_expr)
            del region_slope
            extract_aspect = arcpy.sa.ExtractByAttributes(in_raster=region_aspect, where_clause=select_expr)
            del region_aspect

            # Nibble
            arcpy.AddMessage("...Performing Nibble on terrain rasters...")
            nibble_slope = arcpy.sa.Nibble(boundary_slope, extract_slope)
            del boundary_slope, extract_slope
            nibble_aspect = arcpy.sa.Nibble(boundary_aspect, extract_aspect)
            del boundary_aspect, extract_aspect

            # CONVERSION OF TERRAIN RASTERS
            # Raster to Polygon
            arcpy.AddMessage("Converting terrain rasters to polygons...")
            arcpy.RasterToPolygon_conversion(in_raster=nibble_slope,
                                             out_polygon_features=os.path.join(out_dir, "Slope_Polygons"),
                                             simplify="SIMPLIFY", raster_field="Value")
            # Rename the gridcode field to SLOPE - this improves clarity with this layer gets merged with aspect polygons
            arcpy.AlterField_management(in_table=os.path.join(out_dir, "Slope_Polygons"), field="gridcode",
                                        new_field_name="SLOPE", new_field_alias="Slope")
            del nibble_slope

            arcpy.RasterToPolygon_conversion(in_raster=nibble_aspect,
                                             out_polygon_features=os.path.join(out_dir, "Aspect_Polygons"),
                                             simplify="SIMPLIFY", raster_field="Value")
            arcpy.AlterField_management(in_table=os.path.join(out_dir, "Aspect_Polygons"), field="gridcode",
                                        new_field_name="ASPECT", new_field_alias="Aspect")
            del nibble_aspect

            # Union terrain rasters
            arcpy.AddMessage("...Unioning terrain rasters...")
            arcpy.Union_analysis(in_features=["Slope_Polygons", "Aspect_Polygons"],
                                 out_feature_class=out_polygons, join_attributes="AlL")

            # Create Contours
            arcpy.AddMessage("Creating countours...")
            arcpy.sa.Contour(in_raster=smooth_dem, out_polyline_features="contours", contour_interval=5, base_contour=0,
                             contour_type="CONTOUR")

            # Intersect contours with terrain polygons
            arcpy.AddMessage("...Intersecting contours with terrain raster...")
            # Create TERRAIN AWARENESS!!!
            arcpy.Intersect_analysis(in_features=["contours", out_polygons], out_feature_class=out_contours,
                                     join_attributes="NO_FID", output_type="LINE")
            arcpy.AddMessage("...dropping some extra fields...")
            """Need to delete the extra fields associated with the polygons here too..."""
            arcpy.DeleteField_management(in_table=out_polygons,
                                         drop_field=["FID_Slope_Polygons", "Id", "FID_Aspect_Polygons", "Id_1"])
            arcpy.DeleteField_management(in_table=out_contours,
                                         drop_field=["FID_Slope_Polygons", "Id_1", "FID_Aspect_Polygons", "Id_12"])

            # Success message
            arcpy.AddMessage("BUCKLE UP - You just create some terrain aware contour lines! Go style them yourself or"
                             "use the 'Style Terrain Aware Contours' tool to apply some pre-defined style files as"
                             "a starting point!")

        except:
            # WOOF something borked here.
            arcpy.AddError("Unable to complete script")
            e = sys.exc_info()[1]
            arcpy.AddError(e.args[0])
            sys.exit()

        return


class StyleTerrainAwareLayer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Style Terrain Aware Layer"
        self.description = "Tool used to apply a collection of predefined styles to Terrain Aware Contours."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Style",
            name="style_type",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # All the style logic of this tool is based on this list
        param0.filter.list = ["CMYK_DOTS", "DOT_LINES", "HACHURES", "HALFTONE_DOTS", "HATCHING", "STIPPLE", "SWISS-ISH", "LINES", "WATERCOLOUR", "WEIGHTED_CONTOURS"]

        # Second Parameter
        param1 = arcpy.Parameter(
            displayName="Terrain Aware Layer",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        # Third Parameter
        param2 = arcpy.Parameter(
            displayName="Map Scale",
            name="map_scale",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        param2.value = 24000

        parameters = [param0, param1, param2]

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Switch the expected geometry type based on the selected style
        line_list = ["DOT_LINES", "HACHURES", "LINES", "SWISS-ISH", "WEIGHTED_CONTOURS"]
        poly_list = ["CMYK_DOTS", "HALFTONE_DOTS", "HATCHING", "STIPPLE", "WATERCOLOUR"]
        if parameters[0].altered:
            if (parameters[0].valueAsText in line_list):
                parameters[1].filter.list = ["Polyline"]
            elif (parameters[0].valueAsText in poly_list):
                parameters[1].filter.list = ["Polygon"]
            else:
                pass
        else:
            pass

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # Check to ensure that the input layer has the required fields
        if parameters[1].altered:
            # Create list of fields in input
            fields = arcpy.ListFields(parameters[1].valueAsText)
            # Convert to names and uppercase
            field_names = [f.name.upper() for f in fields]
            # Test if the layer has the fields we need.
            if 'SLOPE' in field_names and 'ASPECT' in field_names:
                pass
            else:
                parameters[1].setErrorMessage("The input layer does not have the required SLOPE and ASPECT fields.")

        # Ensure that the map scale is greater than 0
        if parameters[2].altered:
            if int(parameters[2].value) < 1:
                parameters[2].setErrorMessage(
                    "A positive map scale value is required.")
            else:
                pass
        else:
            pass

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Gather parameters
        in_style = parameters[0].valueAsText
        in_layer = parameters[1].valueAsText
        in_scale = parameters[2].value

        arcpy.AddMessage(in_style)
        arcpy.AddMessage(in_layer)

        # Dictionary to contain the layer file names
        style_dict = {"CMYK_DOTS" : ["Halftone", "CMYK_Dots.lyrx"],
                      "DOT_LINES" : ["Stipple","Dotted_lines.lyrx"],
                      "HACHURES" : ["Hachure", "Hachure.lyrx"],
                      "HALFTONE_DOTS" : ["Halftone", "Halftone_Dots.lyrx"],
                      "HATCHING" : ["", ""],
                      "STIPPLE" : ["Stipple", "Stipple.lyrx"],
                      "SWISS-ISH" : ["Hachure", "Swiss-ish.lyrx"],
                      "LINES" : ["Hatching", "Lines.lyrx"],
                      "WATERCOLOUR" : ["Watercolour", "Watercolour.lyrx"],
                      "WEIGHTED_CONTOURS" : ["", ""]}

        # Apply the styled layer file from the toolbox folder
        try:
            arcpy.AddMessage(os.path.join(sys.path[0], "Styles"))
            scriptPath = sys.path[0]
            dirPath = os.path.dirname(scriptPath)
            stylePath = os.path.join(dirPath, "Styles", style_dict[in_style][0],style_dict[in_style][1])
            arcpy.AddMessage("Attempting to gather style file for {}...".format(in_style))
            arcpy.AddMessage("...Style file found in directory: {}...".format(stylePath))

            arcpy.AddWarning("Sorry, the ability to Apply Symbology From Layer is currently impacted by a bug (BUG-000106281, BUG-000108497) and does not function from Python a tool. Apply the styles manually for now.")

            # At the moment, the ability to apply symbology from a layer is impacted by BUG-#
            # arcpy.ApplySymbologyFromLayer_management(in_layer=in_layer, in_symbology_layer=stylePath)

            # aprx = arcpy.mp.ArcGISProject("CURRENT")
            # map = aprx.listMaps()[0]
            # layers = map.listLayers()
            #
            # for layer in layers:
            #     if layer.name == in_layer:
            #         arcpy.AddMessage(str(layer.name))
            #         layer.updateConnectionProperties(in_layer, in_layer)


        except:
            arcpy.AddError("Uh oh something went sideways when trying to find the style file, have they been moved?...")
            e = sys.exc_info()[1]
            arcpy.AddError(e.args[0])
            sys.exit()

        return

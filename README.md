# Terrain Aware Toolbox
This python toolbox has been designed to generate and style _'terrain aware'_ features classes based on an input Digital Elevation Model (DEM). The output polyline and polygon feature classes can be styled through the use of [Arcade Expressions](https://developers.arcgis.com/arcade/) in the ArcGIS Pro symbology panel to showcase a collection of artistic methods for rendering 3-dimensional terrain on a 2-dimensional map.

Many of the cartographic techniques rendered by this tool are best discussed and described in additional detail in the collection of [Terrain Tools](arcg.is/1GvWPr) created by Kenneth Field and Linda Beale. Those Terrain Tools were a both source of inspiration and constant reference while creating my toolbox.

## Backstory
The methods behind this madness were inspired by the terrain shading prowess of John Nelson and his adventures in creating a reproduction of [Chevalier’s hachure shading](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/chevalier-shade/) and [Erwin Raisz landscape maps](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/landscape-map-in-the-spirit-of-erwin-raisz/). Entranced and inspired I tried it out myself, and you should too!

The beauty of sharing is that it often inspires others to re-use, adapt, and modify it for their own maps or better yet, fuel even more creativity. In this case, I was hooked, and it led me down a rabbit hole. I dove headlong into how I might further iterate and refine upon the concept. After much experimentation, I arrived at [some methods and results](https://warrenrdavison.wixsite.com/maps/post/revisiting-hachure-lines-dynamic-hachure-contours-in-arcgis-pro) that allowed me to render hachure shading on my own [Chevalier inspired map](https://warrenrdavison.wixsite.com/maps/chevalierhachure).

However, I couldn't just park the idea and leave it alone. I knew there was even more potential buried in these _'terrain aware'_ layers, I'm still accepting a better name, and I wanted to be able to share this in a way that was easy for others to pick up, use, and adapt. Through sharing this tool, the included styles, and configured expressions I hope to inspire others to use it for their maps and find even more artistic methods for depicting terrain. Keep in mind that these are just a starting point as the purpose is to inspire and illustrate some methods for how to further develop, modify, and enhance your own terrain rendering skillset.

Now with the professional preamble out of the way, buckle up, go forth and make great maps! If you ever get stuck or want more details on how the tool, styles, or expressions were configured read the rest of the documentation contained that describes in much more detail the inner workings of the toolbox.

# Installation


# Contents
The contents of this repo are organized into a folder structure as follows.

## Samples
This folder contains all the gratuitous screenshots of the tool outputs in all their rendered glory. Feast your eyes on these symbology snacks, get inspired, and go make your own!

If you do make some maps and want to share, send your screenshots or maps my way @WarrenDz.

## Styles
This folder sub-directories, organized by general technique, containing all of the layer files `.lyrx`, arcade expressions `.lxp`, and the style file `.stylx` required to start rendering your _'terrain aware'_ layers.

### Layer Files
Layer files are all named based on the technique they are designed to render. These layer files `.lyrx` already have the arcade expressions baked into their symbology and are the quickest way to getting started. They reveal where the expressions have been applied within the symbology pane of ArcGIS Pro and how they effect how the style is rendered.

These layer files are provided as a general template and a starting point to fine tune and configure the variables that control the rendering of the layer, further configuration and experimentation are encouraged!

### Arcade Expressions
The arcade expressions are the magic sauce. These expressions consume attributes values assigned to the features within the _'terrain aware'_ layers and modify the symbology variables that control how features are drawn. All expression files have been named following this convention `technique_symbolVariable.lxp`. Therefore, the `Hachure_PlacementDensity.lxp` is used to control the **placement density** of the **hachure** stroke markers of the `Hachure.lyrx` file. Detailed descriptions of the variables within the expressions and how they effect rendering are explained in associated readme files within the respective folders.

Depending on the complexity of the technique, some layer files may have several associated expressions. Use, adapt, and modify as you like to achieve the effect you desire.

### Style
The `.stylx` file is the ArcGIS Pro style that contains the raw symbols used within each of the layer files. These symbols **do not** contain arcade expressions in their symbol rendering logic.

This style catalog serves as a useful as a jumping off point to modify and reconfigure the various symbology. Want to create your own version of hachures or halftone dots? Start with the existing symbols and construct and/or deconstruct to suit your needs.

## Toolbox
The toolbox is authored as a [Python Toolbox](https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-quick-tour-of-python-toolboxes.htm) with **two tools**. These tools are designed to be run in sequence, **Create** then **Style**, and are separated to provide ease of use re-styling geoprocessing results without re-running the geoprocessing.

Further detail describing how these tools function is provided in the associated readme.


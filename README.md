# Terrain Aware Toolbox
This python toolbox has been designed to generate and style _'terrain aware'_ features classes based on an input Digital Elevation Model (DEM). The output polyline and polygon feature classes can be styled through the use of [Arcade Expressions](https://developers.arcgis.com/arcade/) in the ArcGIS Pro symbology panel to showcase a collection of artistic methods for rendering 3-dimensional terrain on a 2-dimensional map.

Many of the cartographic techniques rendered by this tool are best discussed and described in additional detail in the collection of [Terrain Tools](arcg.is/1GvWPr) created by Kenneth Field and Linda Beale. Those Terrain Tools were a both source of inspiration and constant reference while creating this toolbox.

## Backstory
The methods behind this madness were inspired by the terrain shading prowess of John Nelson and his adventures in creating a reproduction of [Chevalier’s hachure shading](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/chevalier-shade/) and [Erwin Raisz landscape maps](https://www.esri.com/arcgis-blog/products/arcgis-pro/mapping/landscape-map-in-the-spirit-of-erwin-raisz/). Entranced and inspired I tried it out myself, and you should too!

The beauty of sharing is that it often inspires others to re-use, adapt, and modify it for their own maps or better yet, fuel even more creativity. In this case, I was hooked, and it led me down a rabbit hole. I dove headlong into how I might further iterate and refine upon the concept.

After much experimentation, I arrived at [some methods and results](https://warrenrdavison.wixsite.com/maps/post/revisiting-hachure-lines-dynamic-hachure-contours-in-arcgis-pro) that allowed me to render hachure shading on my own [Chevalier inspired map](https://warrenrdavison.wixsite.com/maps/chevalierhachure).

However, I couldn't just park the idea and leave it alone. I knew there was even more potential buried in these _'terrain aware'_ layers, I'm still accepting a better name by the way, and I wanted to be able to share this in a way that was easy for others to pick up, use, and adapt. Through sharing this tool, the included styles, and configured expressions I hope to inspire others to use it for their maps and find even more artistic methods for depicting terrain. Keep in mind that these are just a starting point as the purpose is to inspire and demonstrate just a handful of methods for how to further develop, modify, and enhance your own terrain rendering skillset.

Now with the professional preamble out of the way, buckle up, go forth and make great maps! If you ever get stuck or want more details on how the tool, styles, or expressions were configured read the rest of the documentation contained that describes in much more detail the inner workings of the toolbox.

# Installation
If not familiar with GitHub, clicking [here](https://github.com/WarrenDz/terrain-aware/archive/main.zip) will download a `.zip` file of this repository that you can extract to your machine and it will contain everything you need to get started. Alternatively, you can simply click the `Code` dropdown up in the top-right and select `Download  ZIP`.

Add the `TerrainAwarenessToolbox.pyt` python toolbox to your project. Here's some [documentation](https://pro.arcgis.com/en/pro-app/latest/help/projects/connect-to-a-toolbox.htm) on how to Connect to a toolbox.

You're all set, you should now see the toolbox in your project catalog. For a detailed rundown of the tool take a look at the [specific readme](https://github.com/WarrenDz/terrain-aware/tree/main/Toolbox#terrain-aware-toolbox) for the tool.

## Note
The toolbox python script references the style samples using relative paths to the resources so it's best to keep the files in their current organization to ensure everything continues to function.

# Contents
The contents of this repo are organized into a folder structure as follows.

## Toolbox
The toolbox is authored as a [Python Toolbox](https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-quick-tour-of-python-toolboxes.htm) with **two tools**. These tools are designed to be run in sequence, **Create** then **Style**, and are separated to provide ease of use re-styling geoprocessing results without re-running the geoprocessing.

Further detail describing how these tools function is provided in the associated [readme](https://github.com/WarrenDz/terrain-aware/tree/main/Toolbox#terrain-aware-toolbox).

## Samples
This `Samples` folder contains all the gratuitous screenshots of the tool outputs in all their rendered glory. Feast your eyes on these [symbology snacks](), get inspired, and go make your own!

If you do make some maps and want to share, send your screenshots or maps my way @WarrenDz.

## Styles
This folder sub-directories, organized by general technique, containing all of the layer files `.lyrx`, arcade expressions `.lxp`, and the style file `.stylx` required to start rendering your _'terrain aware'_ layers.
link to [styles folder](https://github.com/WarrenDz/terrain-aware/tree/main/Styles#styles)
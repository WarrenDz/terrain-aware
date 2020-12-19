# Halftone Styles
Rather than a perfectly smooth shading, these styles attempt to use halftone dots with varying sizes, depending on the terrain, to produce a gradient effect.

## CMYK Halftone (Polygon)
This style uses a layer of dots for each colour of cyan, magenta, yellow, and black as used in offset printing.
![ScreenAngles](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/CMYK_screen_angles.svg/2560px-CMYK_screen_angles.svg.png)
[CMYK Screen Angles - Wikipedia](https://en.wikipedia.org/wiki/Screen_angle)
The dots vary in size based on terrain to produce a coloured gradient. Feel free to experiment and change the colour ratios or remove a layer of dots for a different effect.

![CYMK Terrain Polygons](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_CMYK_wd.png)

### Parameters
#### Dot Size
The `Halftone_DotSize.lxp` arcade expression has been applied to the `Size` parameter within the **Symbol Pane**. As the terrain becomes more intense and/or shaded, the dot size will be increased.
![CYMK Symbol Panel](https://github.com/WarrenDz/terrain-aware/blob/main/Images/CMYK_SymbolPanel.png)

### CMYK Usage Notes:
- Be sure to set the `Marker Placement > X Step & Y Step` slightly bigger than the `dot_min/max` variable of the `Halftone_DotSize.lxp`. This will allow for a margin of breathing room between the dots at the densest setting and prevent a blob of ink.


## Halftone (Polygon)
![Halftone Terrain Polygons](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Halftone_wd.png)
This style uses a single layer of dots as a marker fill within in a polygon to simulate a single colour halftone print.

### Parameters
#### Dot Size
The `Halftone_DotSize.lxp` arcade expression has been applied to the `Size` parameter within the **Symbol Pane**. As the terrain becomes more intense and/or shaded, the dot size will be increased.

### Halftone Usage Notes:
- Same as the CYMK style, be sure to set the `Marker Placement > X Step & Y Step` slightly bigger than the `dot_min/max` variable of the `Halftone_DotSize.lxp`. This will allow for a margin of breathing room between the dots at the densest setting and prevent a blob of ink.
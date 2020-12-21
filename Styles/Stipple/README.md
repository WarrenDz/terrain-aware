# Stipple Styles
The stipple styles attempt to emulate hand drawn stipple shading to represent the terrain. There are two implementations of the stipple dot technique (I'm partial to the **Dotted Line** version).

## Stipple (Polygon)
This implmentation of stippled dots uses the polygon geometry and fills the polygons with a random dot marker of varying size according to terrain.
![Stipple Polygons](https://github.com/WarrenDz/terrain-aware/blob/main/Images/SanFran_Stipple_wd.png)

### Parameters
Here's where expressions can be supplied to achieve this technique.
![Stipple Symbol Panel](https://github.com/WarrenDz/terrain-aware/blob/main/Images/Stipple_SymbolPanel.png)

#### Dot Size
The dot size is controlled by the `Stipple_DotSize.lxp` as with most other expressions this will return a larger marker in areas of more intense terrain.

#### Marker Spacing (X/Y Step)
The spacing is controlled by the `Stipple_Spacing.lxp` and modifies how closely placed markers are to each other. Where terrain is more instense/shaded the dots will be placed closer together giving a darker shading effect for the viewer.

### Usage Notes:
Generally speaking, this implementation of stippled dots tends to take longer to draw.

## Dotted Lines (Contours)
This style uses stipple dots but aligns them along the contour lines.
![Stipple Symbol Panel](https://github.com/WarrenDz/terrain-aware/blob/main/Images/SanFran_DottedLines_wd.png)

#### Dot Size
The dot size is controlled by the `Dotted_Line_DotSize.lxp` as with most other expressions this will return a larger marker in areas of more intense terrain.

## Usage Notes:
The **Dotted Lines** style makes use of both a `Marker Placement > random offset`, and a `Marker Placement > Along line with variable size` option to add some variability.
![Stipple Symbol Panel](https://github.com/WarrenDz/terrain-aware/blob/main/Images/DottedLine_RandomOffset.png)
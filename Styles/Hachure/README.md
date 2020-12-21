# Hachure Styles
These styles utilize [hachure strokes](https://en.wikipedia.org/wiki/Hachure_map) to represent relief.

## Hachure (Contours)
Your steadfast classic hachures.
![Hachures](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Hachure_Chevalier_wd.png)

### Parameters
![Symbol variable inputs](https://github.com/WarrenDz/terrain-aware/blob/main/Images/Hachure_SymbolPanel.png)

#### Hachure Stroke Weight
The stroke weight (pts) of inidividual hachure marks is controlled by the `width_min` and `width_max` variables of the `Hachure_StrokeWeight.lxp`. Where terrain is more intense (sloped/shaded), the stroke weight will be increased. This expression is entered within the `Line Width` setting within the symbol panel.

    // Hachure Rendering Parameters
    // Dictate the min and max stroke weight of the hachure strokes (pts)
    var width_min = 0.15
    var width_max = 1.5

#### Hachure Row Width (Bandwidth)
The hachure row width is determined by the `Hachure_Bandwidth.lxp` expression and will vary the width of each hachure row based on the terrain. Where terrain is more intense (sloped/shaded), the stroke weight will be decreased to accomodate the more dense packed contours. This expression is entered in the `Size` variable of the symbol panel.

#### Hachure Placement Density
The density of the hachure strokes is modified by the `Hachure_PlacementDensity.lxp` expression and will tighten the spacing of strokes in areas where the terrain is more intense (sloped/shaded). This expression is applied to the `Marker Placement` setting of the symbol.

### Hachure Usage Notes
Modifying the `aspect_min` variable within each of the arcade expressions of this style can be used to constrain how far hachures wrap around the slopes. Setting an `aspect_min=0` will result in full blown 'fuzzy caterpillar' hachures.

!['Fuzzy Caterpillars'](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Hachure_FuzzyCaterpillar_wd.png)

Constraining the `aspect_min=4` will produce hachures only on shaded slopes similar to the [Chevalier hachures](https://www.davidrumsey.com/luna/servlet/s/5u3c4q).

!['Chevalier Hachures'](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Hachure_Chevalier_wd.png)

## Swiss-ish (Contours)
An interpretation of Swiss Topo hachures.

![]()

### Parameters
The symbol parameters for this style are nearly identical to the standard Hachure style. The exception is that the slope settings have been confirgured so that the hachures are only drawn in the steepest sloped portions of the terrain `slope_min = 6`. Where the terrain is less than this value, the symbology will render as contour lines.

#### Contour Stroke Weight
The contour stroke weight is used to 'hide' contour lines in the steepest sloped portions of the terrain. By hiding the contours the hachures will be more visible. The hiding of contour lines is controlled by the `Swissish_ContourWeight.lxp` expression. Evaluating the last criteria in the expression will only draw contours where they are less than the steepest slopes otherwise, they will have a `0` width.

    // Return Terrain Aware Value where criteria is met
    return IIf($feature.SLOPE < slope_limit, Text(width), Text(0))

### Swiss-ish Usage Notes

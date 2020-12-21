# Styles
Buckle up! The following readme provides an overview the style file, the layer files, and some of the features of the Arcade Expressions used to render the symbology.

## Style File
The `.stylx` file is the ArcGIS Pro style that contains the raw symbology elements used within each of the layer files. These symbols **do not** contain arcade expressions in their symbol rendering logic.

This style catalog serves as a useful as a jumping off point to experiment and modify the various symbol elements. Want to create your own version of hachures or halftone dots? Start with the existing symbols and construct and/or deconstruct (as per the culinary trend) to suit your needs.

## Layer Files
Layer files are all named based on the technique they are designed to render. These layer files `.lyrx` already have the arcade expressions baked into their symbology and are the quickest way to getting started. They reveal where the expressions have been applied within the symbology pane of ArcGIS Pro and how they effect how the style is rendered.

These layer files are provided as a general template and a starting point to fine tune and configure the variables that control the rendering of the layer, further configuration and experimentation are encouraged! The Header of each unique readme file indicates the geometry that the layer file is used to style ex. 'Watercolour **(Polygon)**'.

_*Note: For consistency all of the layer files have been configured to display best at `24,000`. Depending on your needs you can either set a reference scale on your map to match `24,000` or adjust the parameters of the expressions to suit your needs. There are plans for a [future improvement](https://github.com/WarrenDz/terrain-aware/tree/main/Toolbox#development-goals) to assist with this configuration._

## Arcade Expressions
The arcade expressions are the magic sauce. These expressions consume attributes values assigned to the features within the _'terrain aware'_ layers and modify the symbology variables that control how features are drawn.

All expression files have been named following this convention `Technique_SymbolVariable.lxp`. Therefore, the `Hachure_PlacementDensity.lxp` is used to control the **placement density** of the **hachure** stroke markers of the `Hachure.lyrx` file. Detailed descriptions of the variables within the expressions and how they effect rendering are explained in associated readme files within the respective folders.

Depending on the complexity of the technique, some layer files may have several associated expressions. Use, adapt, and modify as you like to achieve the effect you desire.

### Expression Parameters
The structure and application of arcade expressions throughout the various styles does vary but there are a few parameters that are used generally through the expressions and worth providing some additional descriptions.

![Expression Diagram](https://github.com/WarrenDz/terrain-aware/blob/main/Images/Expression_Diagram.png)

#### aspect & slope min/max
These input parameters inform the slope contraints of the symbol rendering. Think of these constraints like `definition queries` where features that satisfy the criteria will appear in the map and those that don't will be omitted. The difference with these constraints is that features satisfying these constraints will be drawn and those that don't will not, however the geometry of undrawn features still persist within the map and can be used for labelling if needed.

    var slope_min = 1
    var slope_max = 7
    var aspect_min = 1
    var aspect_max = 7

The constraining effect of these parameters is evaluated in the **last expression** of all of the arcade expression files. Essentially, if the attributes of the feature do not meet the criteria of this expression the feature will recieve the default value, typically `Text(0)`, and will therefore, not be drawn with the symbol treatment.

    return IIf($feature.ASPECT >= aspect_min && $feature.SLOPE >= slope_min, Text((Abs(hachure_size - size_max) + size_min)), Text(0))

Using the combination of `slope` and `aspect` constraints, we can control which features recieve specific symbol treatment and how it is drawn without duplicating the layer in the `table of contents` of our map (and applying the associated definition queries there).

Leveraging this control, we can control which slopes (flat/steep) and aspects (sunlit/shaded) recieve our symbol treatment. For instance, to achieve a similar hachure shading as **August Chevalier** in [this map](https://www.davidrumsey.com/luna/servlet/s/5u3c4q) we can increase our aspect constraint ex. `var aspect_min = 3` of the `Hachure.lyrx` style. This would restrict the rendering of the  hachure strokes to only those slopes where the aspect was **greater than or equal to 3**.

The opposite of the **Chevalier hachure shading** would be the full-blown 'fuzzy caterpillar' hachures wrapping around all slopes of the terrain regardless of aspect. In this case, leave the default of `var slope_min = 1`.

#### terrain min/max
The `terrain` value represents the combination of both of these terrain traits. This variable is used to combine and thereby simplify the `slope` and `aspect` traits of the feature into one variable via an equation (method of combining can vary between expressions). This combined trait is then mapped to a "rendering" variable which dictates the symbol propertiesfor drawing.

    // Terrain Value
    var terrain = (slope * 2)
    var terrain_min = 0
    var terrain_max = 14
    var terrain_range = terrain_max - terrain_min

#### render min/max
In hindsight, I should have named these consitently as `render` throughout the expression files. Instead, I named these based on the technique ex. `hachure_density`, `stroke_weight`, `dot_size`. Although named differently, they all serve to define the minimum and maximum values of the symbol property (ex. `stroke weight`, `size`, `placement spacing`). The value of the [terrain variable](https://github.com/WarrenDz/terrain-aware/tree/main/Styles#terrain-minmax) will be mapped to this defined 'render range' and the feature draw with this property.

    // Hachure Rendering Parameters
    // Dictate the min and max width of the hachure banding (pts)
    var size_min = 0.75
    var size_max = 5
    var size_range = size_max - size_min

# FAQ
**A symbol element is drawing when it shouldn't.**
- Check these `min/max` settings for the symbol properties that have been configured. Chances are something isn't constrained the way you intended.

**I've configured a symbol to appear but it's not showing up.**
- Keep in mind if the properties you're configuring are all applied to the same symbol element the most restrictive `min/max` constraints will determine whether the feature appears. Give them all a once over and double-check they're set consistently.

**At 1:24,000 symbology looks good, but at any other scale the effect breaks down and looks jumbled or sparse.**
- The layer files and their baked in expressions have been configured at a scale of `1:24,000`. This is where the effect will look the best by default. You can tweak the `render min/max` values to suit your desired map scale or set a reference scale.

**The contours are jumbling up my map, How do I omit some contour intervals for clarity?**
- To omit some contour intervals from the map, you can likely apply a definition query to the layer. This will remove features from the map. When using a definition query be sure that none of the other symbol elements of the style (ex. hachures marks) will be impacted by removing that interval. In the case of the **Swiss-ish** style, it may be required that hachures are drawn on **every interval** and contours are drawn on **every other**. To faciliate this you can apply an 'elevation filter' expression to just a single symbol element.

For instance, here's an example of a 'elevation filter' I've applied to contour lines so that intervals are only drawn if they are a multiple of `25`.

    // Terrain Constraints
    var slope_limit = 7
    var slope = $feature.SLOPE

    // Symbol Encoding
    var stroke_weight = 0.5

    // If the elevation value ends in '00, 25, 50, 75' we'll set the width. Otherwise, it will be a hidden contour.
    var elev = Text($feature.Contour)
    var width = When(Right(elev,2) == '00', Text(stroke_weight), Right(elev,2) == '50', Text(stroke_weight),Right(elev,2) == '25', Text(stroke_weight), Right(elev,2) == '75', Text(stroke_weight),Text(0))

    // Return Terrain Aware Value where criteria is met
    return IIf($feature.SLOPE < slope_limit, Text(width), Text(0))


# Styles
Buckle up! The following section breaks down each of the styles and how the Arcade Expressions are used to render the symbology. The structure of all the Arcade Expressions is fairly similar with some common variables that control the symbology. Here's a quick walkthrough of the general structure before we dig into how these expressions are applied within each style.

## Layer Files
Layer files are all named based on the technique they are designed to render. These layer files `.lyrx` already have the arcade expressions baked into their symbology and are the quickest way to getting started. They reveal where the expressions have been applied within the symbology pane of ArcGIS Pro and how they effect how the style is rendered.

These layer files are provided as a general template and a starting point to fine tune and configure the variables that control the rendering of the layer, further configuration and experimentation are encouraged!

## Arcade Expressions
The arcade expressions are the magic sauce. These expressions consume attributes values assigned to the features within the _'terrain aware'_ layers and modify the symbology variables that control how features are drawn. All expression files have been named following this convention `technique_symbolVariable.lxp`. Therefore, the `Hachure_PlacementDensity.lxp` is used to control the **placement density** of the **hachure** stroke markers of the `Hachure.lyrx` file. Detailed descriptions of the variables within the expressions and how they effect rendering are explained in associated readme files within the respective folders.

Depending on the complexity of the technique, some layer files may have several associated expressions. Use, adapt, and modify as you like to achieve the effect you desire.

## Style
The `.stylx` file is the ArcGIS Pro style that contains the raw symbols used within each of the layer files. These symbols **do not** contain arcade expressions in their symbol rendering logic.

This style catalog serves as a useful as a jumping off point to modify and reconfigure the various symbology. Want to create your own version of hachures or halftone dots? Start with the existing symbols and construct and/or deconstruct to suit your needs.

### Notes
The aspect constraints are a great way to apply the effects to specific portions of the aspect. If you only want the effect (ie. Hachures to be drawn on the shade side then increasing the lower threshold to 3 or 4 will constrain the effect to just those slopes that have an equal or greater attribute value.

Also, if you are using several arcade expressions throughout the symbology pane it’s recommended to keep the slope_min, slope_max, aspect_min, and aspect_max all consistent. Nothing will break but it will impact results since these constraints modify the remapping of values and determine what effects render. The rendering of the styles is dictated by the most restrictive variable.

Long story short, if something doesn’t look the way you expect, or hasn’t updated the way you thought it might check these constraints across your expressions.


- include general note on scaling
- elevation modifier
- CIM access

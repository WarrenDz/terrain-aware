# Styles
Buckle up! The following section breaks down each of the styles and how the Arcade Expressions are used to render the symbology. The structure of all the Arcade Expressions is fairly similar with some common variables that control the symbology. Here's a quick walkthrough of the general structure before we dig into how these expressions are applied within each style.

## Notes
The aspect constraints are a great way to apply the effects to specific portions of the aspect. If you only want the effect (ie. Hachures to be drawn on the shade side then increasing the lower threshold to 3 or 4 will constrain the effect to just those slopes that have an equal or greater attribute value.

Also, if you are using several arcade expressions throughout the symbology pane it’s recommended to keep the slope_min, slope_max, aspect_min, and aspect_max all consistent. Nothing will break but it will impact results since these constraints impact the remapping of values and determine what effects render. The rendering of the styles is dictated by the most restrictive variable. Long story short, if something doesn’t look the way you expect, or hasn’t updated the way you thought it might check these constraints across your expressions.


- include general note on scaling

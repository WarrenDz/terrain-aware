# Watercolour (Polygon)
The watercolour style makes use of a modified polygon image fill from John Nelson’s [watercolour style](https://arcg.is/0meKiK). This image fill helps to render the terrain polygons with a painterly effect. Don’t forget to use a paper fill beneath for good measure and slap a blend mode on for bonus points.

![Watercolour Terrain Polygons](https://github.com/WarrenDz/terrain-aware/blob/main/Images/SanFran_Watercolour2_wd.png)

## Parameters
The arcade expressions for this style are applied in the `Vary Symbol by Attribute` tab of the Symbol Panel. 
![Vary Watercolour by Attribute](https://github.com/WarrenDz/terrain-aware/blob/main/Images/Watercolour_Symbology.png)

### Aspect
The `ASPECT` attribute is simply plugged into colour setting.

### Transparency
If desired, you can supply the `Watercolour_Transparency.lxp` expression to the `Transparency` parameter within the same symbol panel. This will fade less intense slopes and slopes oriented towards the azimuth.

### Watercolour Usage Notes:
- The symbol structure for this layer contains 3 identical image fills. Only 1 has been turned on. If you'd like to increase the saturation of this style you can turn additional layers on.

- Combining the Watercolour style beneath another style ex. Hachures or Swiss-ish, with a **Multiply blend mode**, can provide a watercolour terrain underlay.
![Watercolour Terrain Underlay](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/Grand_Canyon_Sample_wd_Thumbnail.png)

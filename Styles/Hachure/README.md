# Hachure Styles
These styles utilize [hachure strokes](https://en.wikipedia.org/wiki/Hachure_map) to represent relief.

## Hachure (Contours)
Your steadfast classic hachures.

![]()

### Parameters
#### Hachure Stroke Weight

#### Hachure Row Width (Bandwidth)

#### Hachure Placement Density

### Hachure Usage Notes
Modifying the `aspect_min` variable within each of the arcade expressions of this style can be used to constrain how far hachures wrap around the slopes. Setting an `aspect_min=0` will result in full blown 'fuzzy caterpillar' hachures.

!['Fuzzy Caterpillars'](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Hachure_FuzzyCaterpillar_wd.png)

Constraining the `aspect_min=4` will produce hachures only on shaded slopes similar to the [Chevalier hachures](https://www.davidrumsey.com/luna/servlet/s/5u3c4q).

!['Chevalier Hachures'](https://github.com/WarrenDz/terrain-aware/blob/main/Samples/SanFran_Hachure_Chevalier_wd.png)

## Swiss-ish (Contours)
An interpretation of Swiss Topo hachures.

![]()

### Parameters
#### Hachure Stroke Weight

#### Hachure Row Width(Bandwidth)

#### Hachure Placement Density

#### Contour Stroke Weight

### Swiss-ish Usage Notes
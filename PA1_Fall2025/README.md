Fall 2025

Chih Han Yeh

CASCS680

PA1 - Scan Conversion


### Line Drawing – `drawLine()`

The `drawLine()` function rasterizes a line between two points using  **Bresenham’s Line Algorithm** , which efficiently determines which pixels best approximate the ideal line using only integer arithmetic.

* **Color Interpolation:** When the `doSmooth` flag is enabled, the algorithm blends colors between the two endpoints, producing smooth transitions along the line.
* **Anti-aliasing:** The `doAA` and `doAAlevel` parameters support optional anti-aliasing via supersampling.

**Key variables:**

* `(x1, y1), (x2, y2)`: Integer coordinates of the endpoints.
* `dx, dy`: Absolute differences in the x and y directions.
* `sx, sy`: Step directions (+1 or –1) depending on slope.
* `P`: The decision variable that drives pixel selection.
* `ColorType`: Stores interpolated color values.
* `Buff`: The pixel buffer where points are drawn.

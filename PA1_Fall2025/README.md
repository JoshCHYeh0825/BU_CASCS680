Fall 2025

Chih Han Yeh

CASCS680

PA1 - Scan Conversion

The main implementations for this assignment focus on the methods `drawLine()` and  `drawTriangle()` , using Bresenham's Line Algorithm and bilinear interpolation .

### Line Drawing – `drawLine()`

The `drawLine()` function rasterizes a line between two points using  **Bresenham’s Line Algorithm** , which efficiently determines which pixels best approximate the ideal line using only integer arithmetic.

* **Color Interpolation:** When the `doSmooth` flag is enabled, the algorithm blends colors between the two endpoints, producing smooth transitions along the line insetead of flat coloring.
* **Anti-aliasing:** The `doAA` and `doAAlevel` parameters support optional anti-aliasing.

**Key variables:**

* `(x1, y1), (x2, y2)`: Integer coordinates of the endpoints.
* `dx, dy`: Differences in the x and y.
* `sx, sy`: Step directions for iterations.
* `P`: The decision variable that drives pixel selection.
* `ColorType`: Stores interpolated color values.
* `Buff`: The pixel buffer where points are drawn.

### Triangle Rasterization – `drawTriangle()`

The `drawTriangle()` function fills a triangle using  **scanline rasterization** , splitting the shape into flat-top and flat-bottom halves. This ensures that filling proceeds row by row (along `y`), with left and right edges computed by interpolation.

* **Shading modes:**
  * Flat shading uses the color of the first vertex (`p1.color`).
  * Smooth shading (when `doSmooth` is enabled) interpolates vertex colors across each scanline.
* **Vertex sorting:** The three vertices are reordered into `v_top`, `v_mid`, and `v_bot` based on their y-coordinates to simplify scanline traversal.
* **Helper functions:**
  * `linterp`: Linear interpolation of scalar values (e.g., x-coordinates).
  * `linterp_color`: Linear interpolation of `ColorType` values.
  * `fill_flat_bottom()` and `fill_flat_top()`: Scanline rasterizers for split triangle halves.

For texture mapping, bilinear interpolation is used. Texture-mapped triangle filling is enabled with `doTexture`, the algorithm computes bounding box coordinates (`min_x`, `max_x`, `min_y`, `max_y`) to normalize texture mapping. Each pixel inside the triangle is mapped to `(u, v)` coordinates within this bounding box.

* **Texture sampling:**
  * `(u, v)` are normalized texture coordinates scaled to the resolution of the loaded texture.
  * `bilinear_text(u, v)` fetches the four nearest texels from `self.texture` and blends them with bilinear interpolation.
  * `queryTextureBuffPoint()` retrieves individual pixels safely from the texture buffer, with clamping to handle out-of-bounds lookups.

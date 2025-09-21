"""
This is the main entry of your program. Almost all things you need to implement is in this file.
The main class Sketch inherit from CanvasBase. For the parts you need to implement, they all marked TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

"""

import os

import wx
import math
import random
import numpy as np

from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Please don't forget to override interrupt methods, otherwise NotImplementedError will throw out
    
    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging
    
    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising super sampling level
        
    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with key board press interruption. Use this to add new keys or new methods
    * drawPoint: method to draw a point
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing
    
    List of methods to override the ones in CanvasBase:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard
        
    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer
        
    """

    debug = 0
    # Change to "./ when submitting"
    texture_file_path = "./pattern.jpg"

    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4

    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            # TODO 0: uncomment this and comment out drawPoint when you finished the drawLine function 
            self.drawLine(self.buff, self.points_l[-2], self.points_l[-1], self.doSmooth, self.doAA, self.doAAlevel)
            # self.drawRectange(self.buff, self.points_l[-2], self.points_l[-1],)
            # self.drawPoint(self.buff, self.points_l[-1]) 
            self.points_l.clear()
            
    """
     # Draws a rectangle
    def drawRectange(self, buff, p1: Point, p2: Point):
        minX = min(p1.coords[0], p2.coords[0])
        maxX = max(p1.coords[0], p2.coords[0])
        minY = min(p1.coords[1], p2.coords[1])
        maxY = max(p1.coords[1], p2.coords[1])
        
        for i in range(minX, maxX + 1):
            for j in range(minY, maxY + 1):
                self.drawPoint(buff, Point([i, j], p1.color))
    """

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            # TODO 0: uncomment this and comment out drawPoint when you finished the drawLine function 
            self.drawLine(self.buff, self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel)
            # self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            # TODO 0: uncomment drawTriangle and comment out drawPoint when you finished the drawTriangle function 
            self.drawTriangle(self.buff, self.points_r[-3], self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel, self.doTexture)
            # self.drawPoint(self.buff, self.points_r[-1])
            self.points_r.clear()

    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        x, y = point.coords
        c = point.color
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255

    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """
        ##### TODO 1: Use Bresenham algorithm to draw a line between p1 and p2 on buff.
        # Requirements:
        #   1. Only integer is allowed in interpolate point coordinates between p1 and p2
        #   2. Float number is allowed in interpolate point color
        
        # Getting coordinates and colors of p1 and p2
        x1, y1 = p1.getCoords()
        x2, y2 = p2.getCoords()
        c1, c2 = p1.getColor(), p2.getColor()

        # Calculate deltas and steps for x and y
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        # Ensuring the lines are always drawn from left to right
        if dy > dx:
            x1, y1, x2, y2 = x2, y2, x1, y1
            dx, dy = dy, dx
            c1, c2 = c2, c1
            sx, sy = sy, sx
        
        # Step direction for y
        sy = 1 if y1 < y2 else -1

        # Initialize decision parameter P
        # Initialize initial points for x and y
        P = (2 * dy) - dx
        curr_x, curr_y = x1, y1
        # For loop for color interpolation
        for curr_x in range(x1, x2 + 1):
            # Color interpolation if doSmooth is True
            if doSmooth and dx != 0:
                t = (curr_x - x1) / dx
                r = (1 - t) * c1.r + t * c2.r
                g = (1 - t) * c1.g + t * c2.g
                b = (1 - t) * c1.b + t * c2.b
                c_draw = ColorType(r, g, b)   
            else:
                c_draw = c1 if abs(curr_x - x1) < abs(curr_x - x2) else c2
        # Plotting the point
            self.drawPoint(buff, Point((curr_x, curr_y), c_draw))     
        # Bresenham's algorithm for line
            if P < 0:
                P += (2 * dy)
            else:
                P += 2 * (dy - dx)
                curr_y += sy 
            curr_x += 1

    def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color
        # Declaring multiple helper functions to simplify the process
        # Linear Interpolation between two points
        
        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Polygon scan fill algorithm and the use of barycentric coordinate are not allowed in this function
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. For texture-mapped fill of triangles, it should be controlled by doTexture flag.        
        # Sorting p1 through p3 by y-coordinates

        # Sorting the vertices by top middle and bottom
        v_top, v_mid, v_bot = sorted([p1, p2, p3], key=lambda point: point.coords[1])
        
        # Computing the bounding box of the triangle
        min_x = min(p1.coords[0], p2.coords[0], p3.coords[0])
        max_x = max(p1.coords[0], p2.coords[0], p3.coords[0])
        min_y = min(p1.coords[1], p2.coords[1], p3.coords[1])
        max_y = max(p1.coords[1], p2.coords[1], p3.coords[1])
        
        # Preventing division by 0
        bbox_w = max(1, max_x - min_x)
        bbox_h = max(1, max_y - min_y)
        
        # Linear interpolation helper
        def linterp(p0, p1, t):
            return p0 + t * (p1 - p0)
        
        # Linear interpolation between colors
        def linterp_color(c0, c1, t):
            return ColorType(
                linterp(c0.r, c1.r, t),
                linterp(c0.g, c1.g, t),
                linterp(c0.b, c1.b, t)
            )
        
        # Helper function for billinear inte4rpolating texture
        def bilinear_text(u, v):
            # Finds nearest indices of texture map
            u0, v0 = int(math.floor(u)), int(math.floor(v))
            u1, v1 = u0 + 1, v0 + 1
            
            # Making sure we stay inbound of the map
            u0 = max(0, min(self.texture.width - 1, u0))
            u1 = max(0, min(self.texture.width - 1, u1))
            v0 = max(0, min(self.texture.height - 1, v0))
            v1 = max(0, min(self.texture.height - 1, v1))
            
            # Fractional change of texture map
            s = u - u0
            t = v - v0
            
            # Get closest 4 texture pixels
            c00 = self.queryTextureBuffPoint(self.texture, u0, v0).getColor()
            c10 = self.queryTextureBuffPoint(self.texture, u1, v0).getColor()
            c01 = self.queryTextureBuffPoint(self.texture, u0, v1).getColor()
            c11 = self.queryTextureBuffPoint(self.texture, u1, v1).getColor()
            
            # Interpolate horizontally then vertically
            c0 = linterp_color(c00, c10, s)  # bottom row blend
            c1 = linterp_color(c01, c11, s)  # top row blend
            return linterp_color(c0, c1, t)  # blend the two rows

        # Precomputer per-vertex texture coordinates
        def vert_uv(v):
            x, y = v.coords
            u = (x - min_x) / bbox_w
            vv = (y - min_y) / bbox_h
            return (u, vv)

        uv_top = vert_uv(v_top)
        uv_mid = vert_uv(v_mid)
        uv_bot = vert_uv(v_bot)
        
        # Helper function to fill the bottom triangle
        def fill_flat_bottom(v0, v1, v2, uv0, uv1, uv2):
            # v0 = top, v1 and v2 share bottom y
            dy = v2.coords[1] - v0.coords[1]
            if dy == 0:
                return
            y0 = v0.coords[1]
            for y in range(y0, v2.coords[1] + 1):
                t0 = (y - v0.coords[1]) / (v1.coords[1] - v0.coords[1] or 1)
                t1 = (y - v0.coords[1]) / dy

                x_left = linterp(v0.coords[0], v1.coords[0], t0)
                x_right = linterp(v0.coords[0], v2.coords[0], t1)

                c_left = linterp_color(v0.color, v1.color, t0) if doSmooth else p1.color
                c_right = linterp_color(v0.color, v2.color, t1) if doSmooth else p1.color

                uv_left_u = linterp(uv0[0], uv1[0], t0)
                uv_left_v = linterp(uv0[1], uv1[1], t0)
                uv_right_u = linterp(uv0[0], uv2[0], t1)
                uv_right_v = linterp(uv0[1], uv2[1], t1)

                if x_left > x_right:
                    x_left, x_right = x_right, x_left
                    c_left, c_right = c_right, c_left
                    uv_left_u, uv_right_u = uv_right_u, uv_left_u
                    uv_left_v, uv_right_v = uv_right_v, uv_left_v
                    
                xL = int(math.ceil(x_left))
                xR = int(math.floor(x_right))
                span = max(1, x_right - x_left)

                for x in range(xL, xR + 1):
                    alpha = (x - x_left) / span
                    if doTexture and self.texture:
                        # Interpolate uv across span (normalized)
                        u_norm = linterp(uv_left_u, uv_right_u, alpha)
                        v_norm = linterp(uv_left_v, uv_right_v, alpha)
                        # Convert normalized uv to texture pixel coords
                        u_px = u_norm * (self.texture.width - 1)
                        v_px = v_norm * (self.texture.height - 1)
                        c_draw = bilinear_text(u_px, v_px)
                    elif doSmooth:
                        c_draw = linterp_color(c_left, c_right, alpha)
                    else:
                        c_draw = p1.color
                    self.drawPoint(buff, Point((x, y), c_draw))
                    
        # Helper function to fill the top triangle
        def fill_flat_top(v0, v1, v2, uv0, uv1, uv2):
            # v0 and v1 share top y, v2 is bottom
            dy = v2.coords[1] - v0.coords[1]
            if dy == 0:
                return
            y0 = v0.coords[1]
            for y in range(y0, v2.coords[1] + 1):
                t0 = (y - v0.coords[1]) / dy
                t1 = (y - v1.coords[1]) / (v2.coords[1] - v1.coords[1] or 1)

                x_left = linterp(v0.coords[0], v2.coords[0], t0)
                x_right = linterp(v1.coords[0], v2.coords[0], t1)

                c_left = linterp_color(v0.color, v2.color, t0) if doSmooth else p1.color
                c_right = linterp_color(v1.color, v2.color, t1) if doSmooth else p1.color

                uv_left_u = linterp(uv0[0], uv2[0], t0)
                uv_left_v = linterp(uv0[1], uv2[1], t0)
                uv_right_u = linterp(uv1[0], uv2[0], t1)
                uv_right_v = linterp(uv1[1], uv2[1], t1)
                
                if x_left > x_right:
                    x_left, x_right = x_right, x_left
                    c_left, c_right = c_right, c_left
                    uv_left_u, uv_right_u = uv_right_u, uv_left_u
                    uv_left_v, uv_right_v = uv_right_v, uv_left_v

                xL = int(math.ceil(x_left))
                xR = int(math.floor(x_right))
                span = max(1, x_right - x_left)
                
                for x in range(xL, xR + 1):
                    alpha = (x - x_left) / span
                    if doTexture and self.texture:
                        u_norm = linterp(uv_left_u, uv_right_u, alpha)
                        v_norm = linterp(uv_left_v, uv_right_v, alpha)
                        u_px = u_norm * (self.texture.width - 1)
                        v_px = v_norm * (self.texture.height - 1)
                        c_draw = bilinear_text(u_px, v_px)
                    elif doSmooth:
                        c_draw = linterp_color(c_left, c_right, alpha)
                    else:
                        c_draw = p1.color
                    self.drawPoint(buff, Point((x, y), c_draw))
         
        # Splitting the triangle if necessary
        if v_mid.coords[1] == v_bot.coords[1]:
            # flat-bottom (v_top, v_mid, v_bot) where mid and bot share y
            fill_flat_bottom(v_top, v_mid, v_bot, uv_top, uv_mid, uv_bot)
        elif v_top.coords[1] == v_mid.coords[1]:
            # flat-top (v_top, v_mid, v_bot) where top and mid share y
            fill_flat_top(v_top, v_mid, v_bot, uv_top, uv_mid, uv_bot)
        else:
            # general triangle -> split at scanline of v_mid
            t = (v_mid.coords[1] - v_top.coords[1]) / (v_bot.coords[1] - v_top.coords[1])
            x_split = linterp(v_top.coords[0], v_bot.coords[0], t)
            # color split (for smooth shading)
            c_split = linterp_color(v_top.color, v_bot.color, t) if doSmooth else p1.color
            # uv split (normalized)
            uv_split_u = linterp(uv_top[0], uv_bot[0], t)
            uv_split_v = linterp(uv_top[1], uv_bot[1], t)

            v_split = Point((int(x_split), v_mid.coords[1]), c_split)
            # call fills with uv for continuity
            fill_flat_bottom(v_top, v_mid, v_split, uv_top, uv_mid, (uv_split_u, uv_split_v))
            fill_flat_top(v_mid, v_split, v_bot, uv_mid, (uv_split_u, uv_split_v), uv_bot)
                
    # test for lines lines in all directions
    def testCaseLine01(self, n_steps):
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal 
    def testCaseLine02(self, n_steps):
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127) / 255,
                                          (128 + math.cos(d_theta * i * 5) * 127) / 255)),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127) / 255,
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127) / 255)),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps):
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()


    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 2
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()

    main()
    # codingDebug()

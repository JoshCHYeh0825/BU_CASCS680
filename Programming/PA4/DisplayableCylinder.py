"""
Define cylinder here.
First version in 11/01/2021

:author: micou(Zezhou Sun), Daniel Scrivener
:version: 2025.11.11
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    sides = 0
    radius = 0
    height = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, sides=36, radius=0.5, height=1, color=ColorType.SOFTBLUE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(sides, radius, height, color)

    def generate(self, sides=36, radius=0.5, height=1, color=ColorType.SOFTBLUE):
        self.sides = sides
        self.radius = radius
        self.height = height
        self.color = color

        cr, cg, cb = color
        vertex = []

        z_top = height / 2.0
        z_bot = -height / 2.0

        vertex.extend([0, 0, z_top, 0, 0, 1, cr, cg, cb, 0.5, 1.0])  # Top Center
        vertex.extend([0, 0, z_bot, 0, 0, -1, cr, cg, cb, 0.5, 0.0])  # Bot Center

        ring_width = sides + 1
        offset_ring0 = 2
        offset_ring1 = 2 + ring_width
        offset_ring2 = 2 + ring_width * 2
        offset_ring3 = 2 + ring_width * 3

        for theta in np.linspace(0, 2 * np.pi, self.sides + 1):
            x = self.radius * np.cos(theta)
            y = self.radius * np.sin(theta)

        self.vertices = np.zeros(0)
        self.indices = np.zeros(0)

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aColor"),
                                  stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aTexture"),
                                  stride=11, offset=9, attribSize=2)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

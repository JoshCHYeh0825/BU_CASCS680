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
        indices = []

        z_top = height / 2.0
        z_bot = -height / 2.0

        center_list = []
        ring0_list = []  # Top Cap Edge
        ring1_list = []  # Top Wall Edge
        ring2_list = []  # Bot Wall Edge
        ring3_list = []  # Bot Cap Edge

        # Center points
        center_list.extend([0, 0, z_top, 0, 0, 1, cr, cg, cb, 0.5, 1.0])  # Top Center
        center_list.extend([0, 0, z_bot, 0, 0, -1, cr, cg, cb, 0.5, 0.0])  # Bot Center

        # Ring points
        for i, theta in enumerate(np.linspace(0, 2 * np.pi, self.sides + 1)):
            x = self.radius * np.cos(theta)
            y = self.radius * np.sin(theta)

            # Texture u-coordinate (horizontal around cylinder)
            u = i / sides

            # Ring 0: N Up
            ring0_list.extend([x, y, z_top, 0, 0, 1, cr, cg, cb, u, 1.0])
            # Ring 1: N Out
            ring1_list.extend([x, y, z_top, np.cos(theta), np.sin(theta), 0, cr, cg, cb, u, 1.0])
            # Ring 2: Bottom Wall (N Out)
            ring2_list.extend([x, y, z_bot, np.cos(theta), np.sin(theta), 0, cr, cg, cb, u, 0.0])
            # Ring 3: Bottom Cap (N Down)
            ring3_list.extend([x, y, z_bot, 0, 0, -1, cr, cg, cb, u, 0.0])

        full_vertex_list = center_list + ring0_list + ring1_list + ring2_list + ring3_list

        self.vertices = np.array(full_vertex_list, dtype=np.float32)

        # Generate indices
        indices = []

        # Offsets (now guaranteed to be correct)
        ring_width = sides + 1
        offset_ring0 = 2
        offset_ring1 = 2 + ring_width
        offset_ring2 = 2 + ring_width * 2
        offset_ring3 = 2 + ring_width * 3

        for i in range(sides):
            current_i = i
            next_i = i+1

            indices.extend([0, offset_ring0 + current_i, offset_ring0 + next_i])

            p1 = offset_ring1 + current_i  # Top Left
            p2 = offset_ring1 + next_i   # Top Right
            p3 = offset_ring2 + current_i  # Bot Left
            p4 = offset_ring2 + next_i   # Bot Right

            indices.extend([p1, p3, p2])  # Triangle 1
            indices.extend([p2, p3, p4])  # Triangle 2

            indices.extend([1, offset_ring3 + next_i, offset_ring3 + current_i])

        self.indices = np.array(indices, dtype=np.uint32)

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

"""
Define displayable cube here. Current version only uses VBO
First version in 10/20/2021

:author: micou(Zezhou Sun), Daniel Scrivener
:version: 2025.11.11
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

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


class DisplayableCube(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, length=1, width=1, height=1, color=ColorType.SOFTBLUE):
        super(DisplayableCube, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(length, width, height, color)

    def generate(self, length=1, width=1, height=1, color=None):
        self.length = length
        self.width = width
        self.height = height
        self.color = color

        # Half Size dimensions
        hl = length / 2.0
        hw = width / 2.0
        hh = height / 2.0

        # Color
        if color is None:
            cr, cg, cb = [1, 1, 1]
        else:
            cr, cg, cb = color

        vertex_list = []
        indices = []

        # 24 vertices, 6 Faces * 4 vertices per face
        faces = [
            # Front (Z+)
            {"n": [0, 0, 1], "v": [[-hl, -hw, hh], [hl, -hw, hh], [hl, hw, hh], [-hl, hw, hh]]},
            # Back (Z-), winding reversed for outward normal
            {"n": [0, 0, -1], "v": [[hl, -hw, -hh], [-hl, -hw, -hh], [-hl, hw, -hh], [hl, hw, -hh]]},
            # Left (X-)
            {"n": [-1, 0, 0], "v": [[-hl, -hw, -hh], [-hl, -hw, hh], [-hl, hw, hh], [-hl, hw, -hh]]},
            # Right (X+)
            {"n": [1, 0, 0], "v": [[hl, -hw, hh], [hl, -hw, -hh], [hl, hw, -hh], [hl, hw, hh]]},
            # Top (Y+)
            {"n": [0, 1, 0], "v": [[-hl, hw, hh], [hl, hw, hh], [hl, hw, -hh], [-hl, hw, -hh]]},
            # Bottom (Y-)
            {"n": [0, -1, 0], "v": [[-hl, -hw, -hh], [hl, -hw, -hh], [hl, -hw, hh], [-hl, -hw, hh]]},
        ]

        # Texture coordinates
        texture_coords = [[0, 0], [1, 0], [1, 1], [0, 1]]

        for i, face in enumerate(faces):
            nx, ny, nz, = face["n"]

            # Add 4 vertices per face
            for j, pos in enumerate(face["v"]):
                x, y, z = pos
                u, v = texture_coords[j]

                vertex_list.extend([x, y, z, nx, ny, nz, cr, cg, cb, u, v])

            offset = i * 4

            # Triangle 1: 0 - 1 - 2
            indices.extend([offset + 0, offset + 1, offset + 2])
            # Triangle 2: 0 - 2 - 3
            indices.extend([offset + 0, offset + 2, offset + 3])

        self.vertices = np.array(vertex_list, dtype=np.float32)
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
                                  stride=11, offset=6, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

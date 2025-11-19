"""
Define sphere here.
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

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    stacks = 0
    slices = 0
    radius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radius=0.5, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        super(DisplayableSphere, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, stacks, slices, color)

    def generate(self, radius, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        self.radius = radius
        self.stacks = stacks
        self.slices = slices
        self.color = color
        
        # 1. Torus Parameters
        # r = tube radius, R = major radius
        r = (outerRadius - innerRadius) / 2.0
        R = innerRadius + r

        # 2. Generate Grid of Vertices (Using TF's linspace logic)
        # We use (rings + 1) and (nsides + 1) to include the seam
        vertex_list = []
        
        # phi (major angle) and theta (minor angle)
        # We flatten the nested loop into a single vertex list
        for phi in np.linspace(0, 2 * np.pi, rings + 1):
            for theta in np.linspace(0, 2 * np.pi, nsides + 1):
                
                # --- Torus Math ---
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)
                cos_theta = np.cos(theta)
                sin_theta = np.sin(theta)

                # Position [x, y, z]
                x = (R + r * cos_theta) * cos_phi
                y = (R + r * cos_theta) * sin_phi
                z = r * sin_theta
                
                # Normal [nx, ny, nz]
                nx = cos_theta * cos_phi
                ny = cos_theta * sin_phi
                nz = sin_theta

                # Texture Coords [u, v]
                # Map indices to [0, 1] based on loop progress
                u_coord = theta / (2 * np.pi) 
                v_coord = phi / (2 * np.pi)

                # Color [r, g, b]
                cr, cg, cb = color

                # Append 11 attributes per vertex
                vertex_list.extend([x, y, z, nx, ny, nz, cr, cg, cb, u_coord, v_coord])

        # 3. Generate Indices (Triangulation)
        # This replaces the "tris.append" part of TF's code to use EBO
        indices = []
        width = nsides + 1  # The number of vertices in one 'stack' or ring row

        # We loop up to 'rings' and 'nsides' (not +1) to create the quads
        for st in range(rings):
            for sl in range(nsides):
                
                # Calculate the 4 indices of the quad
                # current row
                p1 = st * width + sl
                p2 = p1 + 1
                # next row
                p3 = (st + 1) * width + sl
                p4 = p3 + 1

                # Triangle 1
                indices.extend([p1, p3, p2])
                # Triangle 2
                indices.extend([p2, p3, p4])

        # 4. Store as Numpy Arrays
        self.vertices = np.array(vertex_list, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)

        # if doing texcoords: will need to pad one more column for slice seam,
        # to assign correct texture coord
        self.vertices = np.zeros(0)

        self.indices = np.zeros(0)

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is here, switch from vbo to ebo
        self.vbo.draw()
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

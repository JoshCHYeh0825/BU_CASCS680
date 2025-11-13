'''
Define extra attributes and methods supported by a scene
Created on Oct 31, 2018

:authors: micou(Zezhou Sun), Daniel Scrivener
:version: 2025.11.10

'''

from Component import Component
from Point import Point
import numpy as np
import GLUtility

class Scene(Component):
    """
    Extends Component class. Objects that inherit from this should implement animationUpdate.
    """

    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None
    sceneAmbient = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))

        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        self.lTransformations = [self.glutility.translate(0, 2, 0, False),
                                 self.glutility.rotate(60, [0, 0, 1], False),
                                 self.glutility.rotate(120, [0, 0, 1], False)]
        self.lRadius = 3
        self.lAngles = [0, 0, 0]
        self.sceneAmbient = np.array([0.1, 0.1, 0.1])

    def animationUpdate(self):
        """
        Called when animation object need to update
        """
        raise NotImplementedError("animationUpdate method not implemented yet")
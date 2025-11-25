"""
Third scene for TODO5
Shapes: Cube, Cylinder, Sphere
"""
import math
import numpy as np

import ColorType
from Scene import Scene
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableSphere import DisplayableSphere
from DisplayableCylinder import DisplayableCylinder
from DisplayableCube import DisplayableCube


class SceneThree(Scene):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # ambient lighting contribution from the scene
        self.sceneAmbient = np.array([0.2, 0.2, 0.2])

        # Obsidian Cube
        cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.0, 1.0, 1.0, color=ColorType.BLACK))
        m_Obsidian = Material(
            np.array([0.05, 0.05, 0.07, 0.82]),  # Ambient
            np.array([0.18, 0.17, 0.63, 0.82]),  # Diffuse
            np.array([0.33, 0.33, 0.35, 0.82]),     # Specular
            38
        )
        cube.setMaterial(m_Obsidian)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        # Pearl Sphere
        sphere = Component(Point((1.2, 0, 0)), DisplayableSphere(shaderProg, 0.6, color=ColorType.WHITE))
        m_pearl = Material(
            np.array([0.25, 0.21, 0.21, 0.92]),  # Ambient
            np.array([1.00, 0.83, 0.83, 0.92]),  # Diffuse
            np.array([0.30, 0.30, 0.30, 0.92]),  # Specular
            11
        )
        sphere.setMaterial(m_pearl)
        sphere.renderingRouting = "lighting"
        self.addChild(sphere)

        # Copper Cylinder
        cylinder = Component(Point((-1.2, 0, 0)), DisplayableCylinder(shaderProg, 0.3, 1.2, color=np.array([185/255, 115/255, 51/255])))
        m_copper = Material(
            np.array((0.19, 0.07, 0.02, 1.0)),  # Ambient
            np.array((0.70, 0.27, 0.08, 1.0)),  # Diffuse
            np.array((0.26, 0.14, 0.09, 1.0)),  # Specular
            13
        )
        cylinder.setMaterial(m_copper)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        # Lights
        # Light 1: INFINITE LIGHT (Sunlight)
        l0 = Light(
            color=np.array([0.8, 0.8, 0.8, 1.0]),
            infiniteDirection=np.array([-1.0, -1.0, -0.5]) 
        )
        # Note: Infinite lights don't need a position cube

        # Light 2: Point light
        l1_pos = np.array([0.0, 0.0, 4.0])
        l1 = Light(
            position=l1_pos,
            color=np.array([0.4, 0.4, 0.4, 1.0])
        )

        lightCube1 = Component(Point(l1_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube1.renderingRouting = "vertex"
        self.addChild(lightCube1)

        self.lights = [l0, l1]
        self.lightCubes = [None, lightCube1]  # Keep list aligned with lights list

    def animationUpdate(self):
        pass

    def initialize(self):
        self.shaderProg.clearAllLights()
        self.shaderProg.setVec3("sceneAmbient", self.sceneAmbient)
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()

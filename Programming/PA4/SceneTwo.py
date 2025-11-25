"""
Second scene for TODO5
Shapes: Ellipsoid, Torus, Cylinder
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

from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableCylinder import DisplayableCylinder
from DisplayableTorus import DisplayableTorus
from DisplayableCube import DisplayableCube


class SceneTwo(Scene):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # ambient lighting contribution from the scene
        self.sceneAmbient = np.array([0.1, 0.1, 0.1])

        # Gold Ellipsoid
        ellipsoid = Component(Point((-1.0, 0.5, 0)), DisplayableEllipsoid(shaderProg, 0.5, 0.6, 0.7, color=ColorType.YELLOW))
        m_gold = Material(
            np.array([0.25, 0.22, 0.06, 1.0]),  # Ambient
            np.array([0.35, 0.31, 0.09, 1.0]),  # Diffuse
            np.array([0.8, 0.7, 0.2, 1.0]),     # Specular
            83
        )
        ellipsoid.setMaterial(m_gold)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

        # Emerald Cylinder
        cylinder = Component(Point((1.0, 1.0, 0)), DisplayableCylinder(shaderProg, radius=0.5, height=2, color=ColorType.GREEN))
        m_emerald = Material(
            np.array([0.02, 0.18, 0.02, 0.55]),  # Ambient
            np.array([0.08, 0.61, 0.08, 0.55]),  # Diffuse
            np.array([0.63, 0.73, 0.63, 0.55]),  # Specular
            77
        )
        cylinder.setMaterial(m_emerald)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        # Silver Torus
        torus = Component(Point((0, 0.5, 1.0)), DisplayableTorus(shaderProg, 0.1, 0.4, 36, 36, color=ColorType.SILVER))
        m_silver = Material(
            np.array((0.19, 0.19, 0.19, 1.0)),  # Ambient
            np.array((0.51, 0.51, 0.51, 1.0)),  # Diffuse
            np.array((0.51, 0.51, 0.51, 1.0)),  # Specular
            51
        )
        torus.setMaterial(m_silver)
        torus.renderingRouting = "lighting"
        self.addChild(torus)

        # Lights
        
        # Light 1: Spotlight
        l0_pos = np.array([0.0, 3.0, 0.0])
        l0 = Light(
            position=l0_pos,
            color=np.array([1.0, 1.0, 1.0, 1.0]),
            spotDirection=np.array([0.0, -1.0, 0.0]), 
            spotAngleLimit=np.deg2rad(45)
        )
        # Visual Marker for L0
        lightCube0 = Component(Point(l0_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"
        self.addChild(lightCube0)

        # Light 2: Point light
        l1_pos = np.array([3.0, 1.0, 2.0])
        l1 = Light(
            position=l1_pos,
            color=np.array([1.0, 0.6, 0.2, 1.0])
        )
        # Visual Marker for L1
        lightCube1 = Component(Point(l1_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.ORANGE))
        lightCube1.renderingRouting = "vertex"
        self.addChild(lightCube1)

        self.lights = [l0, l1]
        self.lightCubes = [lightCube0, lightCube1]

    def animationUpdate(self):
        pass

    def initialize(self):
        self.shaderProg.clearAllLights()
        self.shaderProg.setVec3("sceneAmbient", self.sceneAmbient)
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
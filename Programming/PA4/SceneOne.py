"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2025.11.11
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

from DisplayableCube import DisplayableCube
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableSphere import DisplayableSphere
from DisplayableCylinder import DisplayableCylinder
from DisplayableTorus import DisplayableTorus

class SceneOne(Scene):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None


    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # ambient lighting contribution from the scene
        self.sceneAmbient = np.array([0.4, 0.4, 0.4])

        cube = Component(Point((-0.75, 0, -0.75)), DisplayableCube(shaderProg, 1.0))
        m1 = Material(np.array((0.0, 0.05, 0.1, 1.0)), np.array((0, 0.3, 0.6, 1)),
                      np.array((0, 0.3, 0.6, 1.0)), 64)
        cube.setMaterial(m1)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        torus = Component(Point((0.75, 0, -0.75)), DisplayableTorus(shaderProg, 0.15, 0.3, 36, 36, ColorType.SOFTRED))
        m2 = Material(np.array((0.1, 0., 0., 1.0)), np.array((0.3, 0.05, 0.05, 1)),
                      np.array((0.3, 0.3, 0.3, 1.0)), 64)
        torus.setMaterial(m2)
        torus.setTexture(shaderProg, "./assets/marble.jpg")
        torus.renderingRouting = "lighting texture"
        torus.rotate(90, torus.uAxis)
        self.addChild(torus)

        sphere = Component(Point((0.75, 0, 0.75)), DisplayableSphere(shaderProg, 0.5, 36, 36, ColorType.SOFTGREEN))
        m3 = Material(np.array((0.0, 0.1, 0.05, 1.0)), np.array((0, 0.6, 0.3, 1)),
                      np.array((0, 0.2, 0.1, 1)), 4)
        sphere.setMaterial(m3)
        sphere.setTexture(shaderProg, "./assets/earth.jpg")
        sphere.renderingRouting = "lighting texture"
        self.addChild(sphere)

        cylinder = Component(Point((-0.75, 0, 0.75)), DisplayableCylinder(shaderProg, color=ColorType.ORANGE))
        m4 = Material(np.array((0.1, 0.02, 0.01, 1.0)), np.array((0.3, 0.2, 0.1, 1)),
                      np.array((0.3, 0.2, 0.1, 1.0)), 64)
        cylinder.setMaterial(m4)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        plane = Component(Point((0, -2., 0.)), DisplayableCube(shaderProg, 5, 0.1, 5, ColorType.GRAY))
        m5 = Material(np.array((0.1, 0.1, 0.1, 1.0)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.2, 0.2, 0.2, 1.0)), 64)
        plane.setMaterial(m5)
        plane.renderingRouting = "lighting"
        self.addChild(plane)

        l0_pos = np.array([0., 2.0, 0.])
        l0 = Light(l0_pos, np.array([1.0, 1.0, 1.0, 1.0]), spotDirection=np.array((0.,-1.,0.)), spotAngleLimit=30*np.pi/180, spotRadialFactor=np.array([0.0, 0.25, 0.0]))
        # l0 = Light(l0_pos, np.array([0, 0, 0, 1.0]), spotDirection=np.array((0.,-1.,0.)), spotAngleLimit=30*np.pi/180)
        lightCube0 = Component(Point(l0_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        l1_pos = np.array([-2., 0., 0.])
        l1 = Light(l1_pos, np.array([*ColorType.SOFTRED, 1.0]))
        # l1 = Light(l1_pos, np.array([0, 0, 0, 1.0]))
        lightCube1 = Component(Point(l1_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTRED))
        lightCube1.renderingRouting = "vertex"

        l2_pos = np.array([2., 0., 0.])
        l2 = Light(l2_pos, np.array([*ColorType.SOFTBLUE, 1.0]))
        # l2 = Light(l2_pos, np.array([0, 0, 0, 1.0]))
        lightCube2 = Component(Point(l2_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTBLUE))
        lightCube2.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.lights = [l0, l1, l2]
        self.lightCubes = [lightCube0, lightCube1, lightCube2]

    def animationUpdate(self):
        # if you'd like to animate your lights (update their positions)
        # you can use the following structure

        # for i, v in enumerate(self.lights):
        #     lPos = ...
        #     self.lightCubes[i].setCurrentPosition(Point(lPos))
        #     self.lights[i].setPosition(lPos)
        #     self.shaderProg.setLight(i, v)

        pass

    def initialize(self):
        self.shaderProg.clearAllLights()
        self.shaderProg.setVec3("sceneAmbient", self.sceneAmbient)
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()

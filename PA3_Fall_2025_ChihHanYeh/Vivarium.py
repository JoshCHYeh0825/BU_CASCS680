"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener
"""

import numpy as np
import random
from Point import Point
from Component import Component
from ModelTank import Tank
from EnvironmentObject import EnvironmentObject
from ModelLinkage import Prey, Predator
from Shapes import Sphere
import ColorType as Ct


class Food(Component, EnvironmentObject):
    """
    Food object that descends slowly into the bottom of the vivarium
    Can be eaten
    """
    def __init__(self, parent, position, shaderProg):
        super(Food, self).__init__(position)
        self.contextParent = parent
        self.velocity = np.array([0.0, -0.002, 0.0])  # slow fall
        self.eaten = False
        self.bound_radius = 0.05

        # Sizing and color
        self.color = Ct.ColorType(1.0, 0.7, 0.1)  # orange-yellow
        self.sphere = Sphere(Point((0, 0, 0)), shaderProg, [0.1, 0.1, 0.1], self.color)
        self.addChild(self.sphere)

    def stepForward(self, tank_dimensions):
        # Drop motion
        nextPos = self.currentPos.coords + self.velocity

        bottom_y = -(tank_dimensions[1] / 2) + self.bound_radius
        if nextPos[1] < bottom_y:
            nextPos[1] = bottom_y
            self.velocity = np.array([0.0, 0.0, 0.0])

        self.setCurrentPosition(Point(nextPos))


class Vivarium(Component):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent, shaderProg):
        self.parent = parent
        self.shaderProg = shaderProg

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(Point((0, 0, 0)), shaderProg, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]
        self.creatures = []  # Separate list for prey and predator
        self.food_obj = []  # List for food objects

        # Adding the creatures: 2 preys, 1 predator
        # Adding the predator, setting up initial position then instantiating
        predator_start = Point([random.uniform(-self.tank_dimensions[i] * 0.45, self.tank_dimensions[i] * 0.45) for i in range(3)])
        Hunter = Predator(parent, predator_start, shaderProg)  # Use parent from Sketch
        self.addNewObjInTank(Hunter)
        self.creatures.append(Hunter)

        # Adding the prey, setting up initial position then instantiating 2 with a for loop
        for _ in range(2):
            prey_pos = Point([random.uniform(-self.tank_dimensions[i] * 0.45, self.tank_dimensions[i] * 0.45) for i in range(3)])
            Hunted = Prey(parent, prey_pos, shaderProg)  # Use parent from Sketch
            self.addNewObjInTank(Hunted)
            self.creatures.append(Hunted)

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """

        for creature in self.creatures[::-1]:
            creature.stepForward(self.creatures, self.tank_dimensions, self)
            creature.animationUpdate()  # Pass self.creatures

        for food in self.food_obj[::-1]:
            food.stepForward(self.tank_dimensions)
            # Check if any creature eats the food
            for creature in self.creatures:
                dist = np.linalg.norm(np.array(creature.currentPos.coords) - np.array(food.currentPos.coords))
                if dist < (creature.bound_radius + food.bound_radius):
                    # Food eaten
                    self.delObjInTank(food)
                    self.food_obj.remove(food)
                    break

        self.update()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components

    def spawnFood(self):
        # Spawn a new food particle randomly near the top of the tank

        # Near top of y but random x/z
        x = random.uniform(-self.tank_dimensions[0] * 0.4, self.tank_dimensions[0] * 0.4)
        y = self.tank_dimensions[1] * 0.3
        z = random.uniform(-self.tank_dimensions[2] * 0.4, self.tank_dimensions[2] * 0.4)
        pos = Point((x, y, z))

        food = Food(self.parent, pos, self.shaderProg)

        self.addNewObjInTank(food)
        self.food_obj.append(food)
        food.initialize()
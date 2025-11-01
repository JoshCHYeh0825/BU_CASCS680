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


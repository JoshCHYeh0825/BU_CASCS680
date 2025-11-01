'''
Define Our class which is stores collision detection and environment information here
Created on Nov 1, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener 08/2022
'''

import math
from Point import Point
from Quaternion import Quaternion
import numpy as np


class EnvironmentObject:
    """
    Define properties and interface for a object in our environment
    """
    env_obj_list = None  # list<Environment>
    item_id = 0
    species_id = 0

    bound_radius = None
    bound_center = Point((0,0,0))

    def addCollisionObj(self, a):
        """
        Add an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.append(a)

    def rmCollisionObj(self, a):
        """
        Remove an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.remove(a)

    def animationUpdate(self):
        """
        Perform the next frame of this environment object's animation.
        """
        self.update()

    def stepForward(self):
        """
        Have this environment object take a step forward in the simulation.
        """
        return

    ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. Creatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.
        
    def rotateDirection(self, v1):
        """
        change this environment object's orientation to v1.
        :param v1: targed facing direction
        :type v1: Point
        """
        # Establish creature's local axis and basis for front facing directions
        forward_v = Point([0, 0, 1])
        v1.normalize()
        dot_prod = forward_v.dot(v1)
        q = Quaternion()

        # Edge cases
        if dot_prod > 0.999:
            self.clearQuaternion()
            return

        elif dot_prod < -0.999:
            # Flip and face backwards
            angle = math.pi
            # Calculate quarternion components (s, v0 to v2)
            s = math.cos(angle / 2.0)
            v0 = 0 * math.sin(angle / 2.0)  # v0 = 0
            v1 = 1 * math.sin(angle / 2.0)  # v1 = 1
            v2 = 0 * math.sin(angle / 2.0)  # v2 = 0
            q.set(s, v0, v1, v2)

        else:
            # Standard cases
            axis = v1.cross3d(forward_v).normalize()
            angle = math.acos(dot_prod)
            half_sin = math.sin(angle / 2.0)
            half_cos = math.cos(angle / 2.0)

            q.set(half_cos, 
                  (axis[0] * half_sin), 
                  (axis[1] * half_sin), 
                  (axis[2] * half_sin))

        self.setQuaternion(q)
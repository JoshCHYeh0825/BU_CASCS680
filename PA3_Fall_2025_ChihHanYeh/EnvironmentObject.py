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
        
    def rotateDirection(self, v1, local_forward=Point([0, 0, 1])):
        """
        change this environment object's orientation to v1.
        :param v1: targed facing direction
        :type v1: Point
        """
        # Normalize both vectors
        v1 = Point(v1.coords / np.linalg.norm(v1.coords))
        fwd = Point(local_forward.coords / np.linalg.norm(local_forward.coords))

        dot_prod = fwd.dot(v1)
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
            v = np.array([0, 1, 0]) * math.sin(angle / 2.0)
            q.set(s, v[0], v[1], v[2])

        else:
            # Standard cases
            axis = fwd.cross3d(v1).normalize()
            angle = math.acos(np.clip(dot_prod, -1.0, 1.0))
            half_sin = math.sin(angle / 2.0)
            half_cos = math.cos(angle / 2.0)
            q.set(half_cos, axis[0] * half_sin,
                  axis[1] * half_sin,
                  axis[2] * half_sin)

        self.setQuaternion(q)

    def distance_to(self, other):
        # Compute Euclidean distance to another EnvironmentObject
        return np.linalg.norm(self.currentPos.coords - other.currentPos.coords)

    def detect_collision(self, other):
        # Detect bounding-sphere collision
        if self is other:
            return False
        dist = self.distance_to(other)
        return dist < (self.bound_radius + other.bound_radius)

    def reflect_direction(self, normal):
        # Reflect movement direction defined by normal
        n = normal / np.linalg.norm(normal)
        self.direction = self.direction - 2 * np.dot(self.direction, n) * n
        self.direction /= np.linalg.norm(self.direction)
        self.rotateDirection(Point(self.direction))

    def apply_attraction(self, target, strength=0.01):
        # Move slightly towards a target object.
        delta = target.currentPos.coords - self.currentPos.coords
        delta /= np.linalg.norm(delta)
        self.direction += strength * delta
        self.direction /= np.linalg.norm(self.direction)
        self.rotateDirection(Point(self.direction))

    def apply_repulsion(self, target, strength=0.02):
        # Move slightly away from a target object.
        delta = self.currentPos.coords - target.currentPos.coords
        delta /= np.linalg.norm(delta)
        self.direction += strength * delta
        self.direction /= np.linalg.norm(self.direction)
        self.rotateDirection(Point(self.direction))

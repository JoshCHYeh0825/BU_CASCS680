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
        
    def rotateDirection(self, v1, local_forward=Point([0, 0, 1]), world_up=Point([0, 1, 0])):
        """
        change this environment object's orientation to v1.
        :param v1: targed facing direction
        :type v1: Point
        """
        # Normalize input vectors
        target = np.array(v1.coords, dtype=float)
        target /= np.linalg.norm(target)
        fwd = np.array(local_forward.coords, dtype=float)
        fwd /= np.linalg.norm(fwd)
        
        # Edge cases
        axis = np.cross(target, fwd)

        if np.linalg.norm(axis) < 1e-6:
            # if vectors are parallel or anti-parallel
            if np.dot(fwd, target) > 0.999:
                self.clearQuaternion()
                return
            else:
                # 180° rotation around up-axis
                axis = np.array(world_up.coords)
                angle = math.pi
        else:
            axis /= np.linalg.norm(axis)
            angle = math.acos(np.clip(np.dot(fwd, target), -1.0, 1.0))

        # Construct quaternion
        s = math.cos(angle / 2.0)
        x, y, z = axis * math.sin(angle / 2.0)
        q = Quaternion()
        q.set(s, x, y, z)
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

    def potential_force(self, target, strength=0.02, range_scale=1.5, mode="attract"):
        """
        Computes gaussian potential function for potential of attraction between objects and creatures.
        mode: "attract" (negative gradient of attractive potential)
            "repel"   (negative gradient of repulsive potential)
        """
        delta = np.array(target.currentPos.coords) - np.array(self.currentPos.coords)
        dist = np.linalg.norm(delta)
        if dist < 1e-6:
            return np.zeros(3)

        dir_vec = delta / dist
        sigma = range_scale

        # Gaussian-shaped influence
        exp_term = np.exp(- (dist / sigma)**2)

        if mode == "attract":
            # Attraction
            force_mag = strength * exp_term
            return force_mag * dir_vec

        elif mode == "repel":
            # Repulsion
            force_mag = strength * (1.0 / (dist**2 + 1e-3)) * exp_term * 5.0
            return -force_mag * dir_vec

        return np.zeros(3)

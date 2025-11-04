"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random
import numpy as np
import math
from Component import Component
from Quaternion import Quaternion
from Shapes import Cube, Cone, Cylinder, Sphere
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

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

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Linkage(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    
    def __init__(self, parent, position, shaderProg):
        super(Linkage, self).__init__(position)
        arm1 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2.setDefaultAngle(120, arm2.vAxis)
        arm3 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm3.setDefaultAngle(240, arm3.vAxis)

        self.components = arm1.components + arm2.components + arm3.components
        self.addChild(arm1)
        self.addChild(arm2)
        self.addChild(arm3)

        self.rotation_speed = []
        for comp in self.components:

            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.5, 0, 0])

        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
        self.vAngle = (self.vAngle + 3) % 360

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.
        nextPos = self.currentPos.coords + self.direction * self.step_size
        if ((nextPos[0] + self.bound_radius) > tank_dimensions[0] / 2) or ((nextPos[0] - self.bound_radius) < -(tank_dimensions[0] / 2)):
            self.direction[0] *= -1
        if ((nextPos[1] + self.bound_radius) > tank_dimensions[1] / 2) or ((nextPos[1] - self.bound_radius) < -(tank_dimensions[1] / 2)):
            self.direction[1] *= -1
        if ((nextPos[2] + self.bound_radius) > tank_dimensions[2] / 2) or ((nextPos[2] - self.bound_radius) < -(tank_dimensions[2] / 2)):
            self.direction[2] *= -1

        finalPos = self.currentPos.coords + self.direction * self.step_size

        self.setCurrentPosition(Point(finalPos))


class ModelArm(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]


class Prey(Component, EnvironmentObject):
    
    def __init__(self, parent, position, shaderProg):
        self.species_id = 2  # ID for Prey
        self.eaten = False
        
        # Setting colors
        color_body = Ct.ColorType(0.8, 0.7, 0.5)
        color_tail = Ct.ColorType(0.6, 0.5, 0.3)
        color_legs = Ct.ColorType(0.6, 0.5, 0.2)
        
        # Setting shapes for the creature
        sizing_scale = 0.5
        # Main body -- Parent
        body_size = [i * sizing_scale for i in [0.4, 0.4, 0.6]]  # Egg-shaped
        super().__init__(position)
        self.contextParent = parent
        
        # Body Shape
        self.body = Sphere(Point((0, 0, 0)), shaderProg, body_size, color_body, limb=False)
        self.addChild(self.body)

        # Tail
        # Segment 1 - Cylinder attached to the back of the body        
        tail_s1_size = [i * sizing_scale for i in [0.08, 0.08, 0.4]]
        self.tail_s1 = Cylinder(Point((0, 0, (-body_size[2] * 0.9))), shaderProg, tail_s1_size, color_tail)
        
        # Compose pre-rotation for segment 1
        R1 = self.glUtility.rotate(180, self.vAxis, False)
        self.tail_s1.setPreRotation(R1)
        
        self.body.addChild(self.tail_s1)
        
        # Segment 2 - Moving cylinder atttached to segment 1
        tail_s2_size = [i * sizing_scale for i in [0.08, 0.08, 0.3]]
        self.tail_s2 = Cylinder(Point((0, 0, tail_s1_size[2])), shaderProg, tail_s2_size, color_tail)
        self.tail_s1.addChild(self.tail_s2)
        
        # Segment 3 - Cone tip attached to segment 1
        tail_s3_size = [i * sizing_scale for i in [0.08, 0.08, 0.3]]
        self.tail_s3 = Cone(Point((0, 0, tail_s3_size[2])), shaderProg, tail_s3_size, color_tail)
        self.tail_s2.addChild(self.tail_s3)

        # Legs
        leg_s1_size = [i * sizing_scale for i in [0.03, 0.03, 0.2]]
        leg_s2_size = [i * sizing_scale for i in [0.02, 0.02, 0.1]]
        foot_size = [i * sizing_scale for i in [0.03, 0.03, 0.1]]
        
        # Leg attachment point
        leg_att_x = body_size[0] * 0.3
        leg_att_y = -body_size[1] * 0.8
        leg_att_z = -body_size[2] * 0.2
        
        # Orientation transforms
        leg_flip = self.glUtility.rotate(180, self.vAxis, False)
        leg_mirror_l = self.glUtility.rotate(180, self.uAxis, False)
        leg_bend = self.glUtility.rotate(-40, self.uAxis, False)

        # Right leg
        self.leg_r1 = Cylinder(Point((leg_att_x, leg_att_y, leg_att_z)), shaderProg, leg_s1_size, color_legs)
        self.leg_r1.setPreRotation(leg_flip)
        self.body.addChild(self.leg_r1)

        self.leg_r2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_legs)
        self.leg_r2.setPreRotation(leg_bend)
        self.leg_r1.addChild(self.leg_r2)

        self.leg_rfoot = Sphere(Point((0, 0, leg_s2_size[2])), shaderProg, foot_size, color_legs)
        self.leg_r2.addChild(self.leg_rfoot)

        # Left leg (Mirrors Right)
        self.leg_l1 = Cylinder(Point((-leg_att_x, leg_att_y, leg_att_z)), shaderProg, leg_s1_size, color_legs)
        self.leg_l1.setPreRotation(leg_flip @ leg_mirror_l)
        self.body.addChild(self.leg_l1)

        self.leg_l2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_legs)
        self.leg_l2.setPreRotation(leg_bend)
        self.leg_l1.addChild(self.leg_l2)
        
        self.leg_lfoot = Sphere(Point((0, 0, leg_s2_size[2])), shaderProg, foot_size, color_legs)
        self.leg_l2.addChild(self.leg_lfoot)
        
        # Components Storage
        self.tail_segments = [self.tail_s1, self.tail_s2, self.tail_s3]
        self.legs_segments = [self.leg_r1, self.leg_r2, self.leg_rfoot,
                              self.leg_l1, self.leg_l2, self.leg_lfoot]
        self.components = [self.body, self.tail_s1, self.tail_s2, self.tail_s3,
                           self.leg_r1, self.leg_r2, self.leg_rfoot, self.leg_l1,
                           self.leg_l2, self.leg_lfoot]
        self.componentList = self.components
        self.componentDict = {
            "body": self.body,
            "tail_s1": self.tail_s1,
            "tail_s2": self.tail_s2,
            "tail_s3": self.tail_s3,
            "leg_r1": self.leg_r1,
            "leg_r2": self.leg_r2,
            "leg_rfoot": self.leg_rfoot,
            "leg_l1": self.leg_l1,
            "leg_l2": self.leg_l2,
            "leg_lfoot": self.leg_lfoot
        }

        # Animation & Collision
        self.tail_wiggle_speed = 0.8
        self.leg_paddle_speed = 1.0
        self.direction = np.random.random(3)
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.step_size = 0.01

        # Set Orientation
        self.forwardAxis = np.array([0, 0, 1])
        self.rotateDirection(Point(self.direction), local_forward=Point([0, 0, 1]))

        # Properties for wall collisions
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = body_size[2] * 1.1

        # Set Pose and Limits
        self.setJointLimits()
        self.setDefaultPose()

    def setJointLimits(self):
        # Tail segment 2 wiggles left/right around the vertical (Y/v) axis
        self.tail_s2.setRotateExtent(self.tail_s2.vAxis, -30, 30)
        self.leg_r1.setRotateExtent(self.leg_r1.vAxis, -20, 20)
        self.leg_l1.setRotateExtent(self.leg_l1.vAxis, -20, 20)

    def setDefaultPose(self):
        # Start with tail straight
        self.tail_s2.setDefaultAngle(0, self.tail_s2.vAxis)
        self.leg_r1.setDefaultAngle(0, self.leg_r1.vAxis)
        self.leg_l1.setDefaultAngle(0, self.leg_l1.vAxis)

    def animationUpdate(self):
        # Tail animation
        # Rotation on segment 2
        self.tail_s2.rotate(self.tail_wiggle_speed, self.tail_s2.vAxis)
        if self.tail_s2.vAngle <= self.tail_s2.vRange[0] or self.tail_s2.vAngle >= self.tail_s2.vRange[1]:
            self.tail_wiggle_speed *= -1
            self.tail_s2.vAngle = max(min(self.tail_s2.vAngle, self.tail_s2.vRange[1]), self.tail_s2.vRange[0])

        # Legs animation
        self.leg_r1.rotate(self.leg_paddle_speed, self.leg_r1.uAxis)
        self.leg_l1.rotate(-self.leg_paddle_speed, self.leg_l1.uAxis)

        # Direction reversal
        # Reverse direction when reaching limits
        if (self.leg_r1.uAngle <= self.leg_r1.uRange[0]) or (self.leg_r1.uAngle >= self.leg_r1.uRange[1]) or \
           (self.leg_l1.uAngle <= self.leg_l1.uRange[0]) or (self.leg_l1.uAngle >= self.leg_l1.uRange[1]):
            self.leg_paddle_speed *= -1
            self.leg_r1.vAngle = np.clip(self.leg_r1.uAngle, *self.leg_r1.uRange)
            self.leg_l1.vAngle = np.clip(self.leg_l1.uAngle, *self.leg_l1.uRange)

        self.update()  # Apply transformations

    def stepForward(self, components, tank_dimensions, vivarium):
        # Creature interactions
        for obj in vivarium.creatures:
            if obj is self:
                continue

            dist = self.distance_to(obj)

            # Evading predator
            if obj.species_id == 2 and dist < 3:
                self.apply_repulsion(obj, strength=0.02)

            # Bounce away from non prey/other predator upon collision
            elif obj.species_id == 1 and self.detect_collision(obj):
                normal = self.currentPos.coords - obj.currentPos.coords
                self.reflect_direction(normal)

        # Probe the next position
        nextPos = self.currentPos.coords + self.direction * self.step_size

        # Wall collision reflection
        half_x, half_y, half_z = tank_dimensions[0] / 2, tank_dimensions[1] / 2, tank_dimensions[2] / 2
        bounce = False
        normals = []

        # X-axis bounce
        if (nextPos[0] + self.bound_radius) > half_x:
            normals.append(np.array([-1, 0, 0]))
            nextPos[0] = half_x - self.bound_radius
        elif (nextPos[0] - self.bound_radius) < -half_x:
            normals.append(np.array([1, 0, 0]))
            nextPos[0] = -half_x + self.bound_radius

        # Y-axis bounce
        if (nextPos[1] + self.bound_radius) > half_y:
            normals.append(np.array([0, -1, 0]))
            nextPos[1] = half_y - self.bound_radius
        elif (nextPos[1] - self.bound_radius) < -half_y:
            normals.append(np.array([0, 1, 0]))
            nextPos[1] = -half_y + self.bound_radius

        # Z-axis bounce
        if (nextPos[2] + self.bound_radius) > half_z:
            normals.append(np.array([0, 0, -1]))
            nextPos[2] = half_z - self.bound_radius
        elif (nextPos[2] - self.bound_radius) < -half_z:
            normals.append(np.array([0, 0, 1]))
            nextPos[2] = -half_z + self.bound_radius

        # Reflect direction across all hit walls
        if normals:
            for n in normals:
                n = n / np.linalg.norm(n)
                self.direction = self.direction - 2 * np.dot(self.direction, n) * n
            self.direction /= np.linalg.norm(self.direction)
            bounce = True

        self.setCurrentPosition(Point(nextPos))
        if bounce:
            self.rotateDirection(Point(self.direction))
            self.applyUprightCorrection()

    def applyUprightCorrection(self):

        up = np.array([0, 1, 0])  # World up
        facing = self.direction / np.linalg.norm(self.direction)
        right = np.cross(facing, up)
        if np.linalg.norm(right) < 1e-6:
            return
        corrected_forward = np.cross(up, right)
        corrected_forward /= np.linalg.norm(corrected_forward)

        self.direction = 0.95 * self.direction + 0.5 * corrected_forward
        self.direction /= np.linalg.norm(self.direction)


class Predator(Component, EnvironmentObject):
    """
    Predator: Similar to prey but green and have moving pincers
    """
    def __init__(self, parent, position, shaderProg):
        self.contextParent = parent
        self.species_id = 1         # ID for Predator
        
        # Creature is too big so this is to scale everything down
        sizing_scale = 0.5
        
        # Setting colors
        color_body = Ct.ColorType(0, 1, 0)      # Bright green
        color_tail = Ct.ColorType(0.8, 0.9, 0)  # Soft Green
        color_pincer = Ct.ColorType(0, 0.4, 0)  # Dark Green
        color_legs = Ct.ColorType(0, 0.5, 0)
        
        # Setting shapes for the creature
        # Main body -- Parent
        body_size = [i * sizing_scale for i in [0.5, 0.5, 0.7]]  # Larger than prey
        super().__init__(position)
        self.contextParent = parent

        self.body = Sphere(Point((0, 0, 0)), shaderProg, body_size, color_body, limb=False)
        self.addChild(self.body)

        # Tail
        # Tail segment sizes and scaling
        tail_s1_size = [i * sizing_scale for i in [0.1, 0.1, 0.25]]
        tail_s2_size = [i * sizing_scale for i in [0.1, 0.1, 0.3]]

        # Segment 1 (Base)
        base_attach_z = -body_size[2] * 0.6 - tail_s1_size[2] / 2.0
        self.tail_s1 = Cylinder(Point((0, 0, base_attach_z + tail_s1_size[2] / 2)), shaderProg, tail_s1_size, color_tail)

        # Compose pre-rotation for segment 1
        R1 = self.glUtility.rotate(180, self.vAxis, False)
        self.tail_s1.setPreRotation(R1)

        self.body.addChild(self.tail_s1)

        # Segment 2 (Middle) - Attached to s1, needs similar pre-rotation to align orientation
        # Position segment 2 at the end of segment 1 (half-length offset)
        self.tail_s2 = Cylinder(Point((0, 0, 2*tail_s1_size[2])), shaderProg, tail_s2_size, color_tail)
        self.tail_s1.addChild(self.tail_s2)

        # Segment 3 (Tip) - Cone attached to the end of segment 2
        tail_s3_size = [i * sizing_scale for i in [0.1, 0.1, 0.2]]
        self.tail_s3 = Cone(Point((0, 0, tail_s2_size[2])), shaderProg, tail_s3_size, color_tail)
        self.tail_s2.addChild(self.tail_s3)

        # Pincer
        pincer_s1_size = [i * sizing_scale for i in [0.08, 0.08, 0.4]]
        pincer_s2_size = [i * sizing_scale for i in [0.08, 0.08, 0.2]]
        pincer_attach_z = body_size[2]/2 - (0.1 * sizing_scale)
        pincer_attach_x = body_size[0]/2

        # Right Pincer
        self.pincer_r1 = Cylinder(Point((pincer_attach_x, 0, pincer_attach_z)), shaderProg, pincer_s1_size, color_pincer)
        self.body.addChild(self.pincer_r1)
        self.pincer_r2 = Cone(Point((0, 0, pincer_s1_size[2])), shaderProg, pincer_s2_size, color_pincer)
        self.pincer_r1.addChild(self.pincer_r2)

        # Left Pincer (Mirrored)
        self.pincer_l1 = Cylinder(Point((-pincer_attach_x, 0, pincer_attach_z)), shaderProg, pincer_s1_size, color_pincer)
        self.body.addChild(self.pincer_l1)
        self.pincer_l2 = Cone(Point((0, 0, pincer_s1_size[2])), shaderProg, pincer_s2_size, color_pincer)
        self.pincer_l1.addChild(self.pincer_l2)            
        
        # Legs
        leg_s1_size = [i * sizing_scale for i in [0.04, 0.04, 0.2]]
        leg_s2_size = [i * sizing_scale for i in [0.02, 0.02, 0.1]]
        foot_size = [i * sizing_scale for i in [0.04, 0.04, 0.2]]
        
        # Leg attachment point
        leg_att_x = body_size[0] * 0.3
        leg_att_y = -body_size[1] * 0.8
        leg_att_z = -body_size[2] * 0.2
        
        # Orientation transforms
        leg_flip = self.glUtility.rotate(180, self.vAxis, False)
        leg_mirror_l = self.glUtility.rotate(180, self.uAxis, False)
        leg_bend = self.glUtility.rotate(-40, self.uAxis, False)
        
        # Right leg
        self.leg_r1 = Cylinder(Point((leg_att_x, leg_att_y, leg_att_z)), shaderProg, leg_s1_size, color_legs)
        self.leg_r1.setPreRotation(leg_flip)
        self.body.addChild(self.leg_r1)

        self.leg_r2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_legs)
        self.leg_r2.setPreRotation(leg_bend)
        self.leg_r1.addChild(self.leg_r2)

        self.leg_rfoot = Sphere(Point((0, 0, leg_s2_size[2])), shaderProg, foot_size, color_legs)
        self.leg_r2.addChild(self.leg_rfoot)

        # Left leg (Mirrors Right)
        self.leg_l1 = Cylinder(Point((-leg_att_x, leg_att_y, leg_att_z)), shaderProg, leg_s1_size, color_legs)
        self.leg_l1.setPreRotation(leg_flip @ leg_mirror_l)
        self.body.addChild(self.leg_l1)

        self.leg_l2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_legs)
        self.leg_l2.setPreRotation(leg_bend)
        self.leg_l1.addChild(self.leg_l2)
        
        self.leg_lfoot = Sphere(Point((0, 0, leg_s2_size[2])), shaderProg, foot_size, color_legs)
        self.leg_l2.addChild(self.leg_lfoot)
        
        # Components Storage
        self.tail_segments = [self.tail_s1, self.tail_s2, self.tail_s3]
        self.right_pincer = [self.pincer_r1, self.pincer_r2]
        self.left_pincer = [self.pincer_l1, self.pincer_l2]
        self.legs_segments = [self.leg_r1, self.leg_r2, self.leg_rfoot,
                              self.leg_l1, self.leg_l2, self.leg_lfoot]
        # Include ALL parts for animation and selection
        self.components = [self.body] + self.tail_segments + self.right_pincer + self.left_pincer + self.legs_segments
        self.componentList = self.components  # For Sketch.py
        self.componentDict = {
            "body": self.body,
            "tail_s1": self.tail_s1, "tail_s2": self.tail_s2, "tail_s3": self.tail_s3,
            "pincer_r1": self.pincer_r1, "pincer_r2": self.pincer_r2,
            "pincer_l1": self.pincer_l1, "pincer_l2": self.pincer_l2,
            "leg_r1": self.leg_r1, "leg_r2": self.leg_r2, "leg_rfoot": self.leg_rfoot,
            "leg_l1": self.leg_l1, "leg_l2": self.leg_l2,"leg_lfoot": self.leg_lfoot
            }

        # Animation & Collision Setup
        self.tail_wiggle_speed = 0.8
        self.pincer_snap_speed = 0.5
        self.leg_paddle_speed = 1.0
        self.direction = np.random.random(3)
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.step_size = 0.01
        
        # Set Orientation
        self.rotateDirection(Point(self.direction))

        # Properties for wall collisions
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = body_size[2] * 1.1

        # Set Pose and Limits
        self.setJointLimits()
        self.setDefaultPose()

    def setJointLimits(self):
        self.tail_s2.setRotateExtent(self.tail_s2.vAxis, -30, 30)  # Wiggle L/R
        self.pincer_r1.setRotateExtent(self.pincer_r1.vAxis, -10, 30)  # Open/Close R
        self.pincer_l1.setRotateExtent(self.pincer_l1.vAxis, -30, 10)  # Open/Close L (mirrored)

    def setDefaultPose(self):
        self.tail_s1.setDefaultAngle(0, self.tail_s1.vAxis)
        self.pincer_r1.setDefaultAngle(15, self.pincer_r1.vAxis)  # Pincers start slightly open
        self.pincer_l1.setDefaultAngle(-15, self.pincer_l1.vAxis)

    def animationUpdate(self):
        # Tail animation
        # Rotation on segment 2
        self.tail_s2.rotate(self.tail_wiggle_speed, self.tail_s2.vAxis)
        if self.tail_s2.vAngle <= self.tail_s2.vRange[0] or self.tail_s2.vAngle >= self.tail_s2.vRange[1]:
            self.tail_wiggle_speed *= -1
            self.tail_s2.vAngle = max(min(self.tail_s2.vAngle, self.tail_s2.vRange[1]), self.tail_s2.vRange[0])

        # Snap pincers
        self.pincer_r1.rotate(self.pincer_snap_speed, self.pincer_r1.vAxis)
        self.pincer_l1.rotate(-self.pincer_snap_speed, self.pincer_l1.vAxis)
        # Reverse both if one hits limit
        if self.pincer_r1.vAngle == self.pincer_r1.vRange[0] or \
           self.pincer_r1.vAngle == self.pincer_r1.vRange[1] or \
           self.pincer_l1.vAngle == self.pincer_l1.vRange[0] or \
           self.pincer_l1.vAngle == self.pincer_l1.vRange[1]:
            self.pincer_snap_speed *= -1

        # Legs animation
        self.leg_r1.rotate(self.leg_paddle_speed, self.leg_r1.uAxis)
        self.leg_l1.rotate(-self.leg_paddle_speed, self.leg_l1.uAxis)

        # Direction reversal
        # Reverse direction when reaching limits
        if (self.leg_r1.uAngle <= self.leg_r1.uRange[0]) or (self.leg_r1.uAngle >= self.leg_r1.uRange[1]) or \
           (self.leg_l1.uAngle <= self.leg_l1.uRange[0]) or (self.leg_l1.uAngle >= self.leg_l1.uRange[1]):
            self.leg_paddle_speed *= -1
            self.leg_r1.vAngle = np.clip(self.leg_r1.uAngle, *self.leg_r1.uRange)
            self.leg_l1.vAngle = np.clip(self.leg_l1.uAngle, *self.leg_l1.uRange)

        self.update()

    def applyUprightCorrection(self):
        """
        Apply a small correction to keep the creature upright (y-axis pointing up)
        """
        up = np.array([0, 1, 0])  # World up
        facing = self.direction / np.linalg.norm(self.direction)
        right = np.cross(facing, up)
        if np.linalg.norm(right) < 1e-6:
            return
        corrected_forward = np.cross(up, right)
        corrected_forward /= np.linalg.norm(corrected_forward)

        self.direction = 0.95 * self.direction + 0.05 * corrected_forward
        self.direction /= np.linalg.norm(self.direction)                                

    def stepForward(self, components, tank_dimensions, vivarium):
        # Creature interactions
        for obj in vivarium.creatures:
            if obj is self:
                continue    

            dist = self.distance_to(obj)

            # Chasing prey
            if obj.species_id == 2 and dist < 4.5:
                self.apply_attraction(obj, strength=0.02)
                
            # Eating prey if close enough
            if obj.species_id == 2 and self.detect_collision(obj):
                vivarium.delObjInTank(obj)
                vivarium.creatures.remove(obj)
                continue  # prey is gone

            # Bounce away from non prey/other predator upon collision
            elif obj.species_id == 1 and self.detect_collision(obj):
                normal = self.currentPos.coords - obj.currentPos.coords
                self.reflect_direction(normal)

        # Probe the next position
        nextPos = self.currentPos.coords + self.direction * self.step_size

        # Wall collision reflection
        half_x, half_y, half_z = tank_dimensions[0] / 2, tank_dimensions[1] / 2, tank_dimensions[2] / 2
        bounce = False
        normals = []

        # X-axis bounce
        if (nextPos[0] + self.bound_radius) > half_x:
            normals.append(np.array([-1, 0, 0]))
            nextPos[0] = half_x - self.bound_radius
        elif (nextPos[0] - self.bound_radius) < -half_x:
            normals.append(np.array([1, 0, 0]))
            nextPos[0] = -half_x + self.bound_radius

        # Y-axis bounce
        if (nextPos[1] + self.bound_radius) > half_y:
            normals.append(np.array([0, -1, 0]))
            nextPos[1] = half_y - self.bound_radius
        elif (nextPos[1] - self.bound_radius) < -half_y:
            normals.append(np.array([0, 1, 0]))
            nextPos[1] = -half_y + self.bound_radius

        # Z-axis bounce
        if (nextPos[2] + self.bound_radius) > half_z:
            normals.append(np.array([0, 0, -1]))
            nextPos[2] = half_z - self.bound_radius
        elif (nextPos[2] - self.bound_radius) < -half_z:
            normals.append(np.array([0, 0, 1]))
            nextPos[2] = -half_z + self.bound_radius

        # Reflect direction across all hit walls
        if normals:
            for n in normals:
                n = n / np.linalg.norm(n)
                self.direction = self.direction - 2 * np.dot(self.direction, n) * n
            self.direction /= np.linalg.norm(self.direction)
            bounce = True

        self.setCurrentPosition(Point(nextPos))
        if bounce:
            self.rotateDirection(Point(self.direction))
            self.applyUprightCorrection()
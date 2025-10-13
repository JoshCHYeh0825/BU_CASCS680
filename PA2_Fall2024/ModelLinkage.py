"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cube
from Shapes import Cylinder
from Shapes import Cone
from Shapes import Sphere
import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent
        
        # Creature design
        """
        - Facehugger. Circular/Oval body
        - 4 three segmented legs
        - 1 four-segmented tail
        - No head, all on a body 
        """
        # Setting color for the creature
        color_body = Ct.ColorType(0.8, 0.7, 0.5)  # Beige for the body
        color_limbs = Ct.ColorType(0.6, 0.5, 0.3)  # Darker color for limbs
        color_limbs_s2 = Ct.ColorType(1, 0.5, 0)     # Color distinction for each segment
        color_limbs_s3 = Ct.ColorType(0, 0.5, 1)

        # Body
        body_size = [0.7, 0.4, 1.2]
        self.body = Sphere(Point((0, 0, 0)), shaderProg, body_size, color_body, limb=False)
        self.addChild(self.body)

        # 8 triple-jolinted limbs
        """
        8 limbs will be built using mirrored pairs (lefct and right).
        Each leg will copntain 3 cylinder segments, each a child of the previous one to establish the triple segmented nature
        """
        # Storing all leg components to left and right
        self.right_legs = []
        self.left_legs = []

        # Leg size
        leg_s1_size = [0.08, 0.08, 0.35]
        leg_s2_size = [0.07, 0.07, 0.25]
        leg_s3_size = [0.06, 0.06, 0.2]

        # Attachment to body
        x_positions = [0.4, 0.5, 0.5, 0.4]
        z_positions = [0.5, 0.15, -0.15, -0.5]
        leg_attach_y = -0.2
        
        # Using a loop to create the 4 pairs of legs
        for i, z_pos in enumerate(z_positions):
            x_pos = x_positions[i]
            
            # Right Leg
            leg_r_s1 = Cylinder(Point((x_pos, leg_attach_y, z_pos)), shaderProg, leg_s1_size, color_limbs)
            self.body.addChild(leg_r_s1)
            leg_r_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs_s2)
            leg_r_s1.addChild(leg_r_s2)
            leg_r_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs_s3)
            leg_r_s2.addChild(leg_r_s3)
            self.right_legs.append([leg_r_s1, leg_r_s2, leg_r_s3])

            # Left Leg (mirrored)
            leg_l_s1 = Cylinder(Point((-x_pos, leg_attach_y, z_pos)), shaderProg, leg_s1_size, color_limbs)
            self.body.addChild(leg_l_s1)
            leg_l_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs_s2)
            leg_l_s1.addChild(leg_l_s2)
            leg_l_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs_s3)
            leg_l_s2.addChild(leg_l_s3)
            self.left_legs.append([leg_l_s1, leg_l_s2, leg_l_s3])

        # 4-jointed Tail
        tail_s1_size = [0.10, 0.10, 0.35]
        tail_s2_size = [0.09, 0.09, 0.28]
        tail_s3_size = [0.08, 0.08, 0.22]
        tail_s4_size = [0.07, 0.07, 0.18]
        
        tail_attach_y = -0.1 
        tail_attach_z = -0.55

        self.tail_s1 = Cylinder(Point((0, tail_attach_y, tail_attach_z)), shaderProg, tail_s1_size, color_limbs)
        self.body.addChild(self.tail_s1)
        self.tail_s2 = Cylinder(Point((0, 0, tail_s1_size[2])), shaderProg, tail_s2_size, color_limbs_s2)
        self.tail_s1.addChild(self.tail_s2)
        self.tail_s3 = Cylinder(Point((0, 0, tail_s2_size[2])), shaderProg, tail_s3_size, color_limbs_s3)
        self.tail_s2.addChild(self.tail_s3)
        self.tail_s4 = Cylinder(Point((0, 0, tail_s3_size[2])), shaderProg, tail_s4_size, color_limbs)
        self.tail_s3.addChild(self.tail_s4)
        self.tail_segments = [self.tail_s1, self.tail_s2, self.tail_s3, self.tail_s4]
        
        # Eye
        sclera_size = [0.15, 0.15, 0.15]
        self.sclera = Sphere(Point((0, 0.2, 0.6)), shaderProg, sclera_size, Ct.WHITE, limb=False)
        self.body.addChild(self.sclera)

        pupil_size = [0.07, 0.07, 0.07]
        self.pupil = Sphere(Point((0, 0, 0.075)), shaderProg, pupil_size, Ct.BLACK, limb=False)
        self.sclera.addChild(self.pupil)
        
        # Components Storage
        self.componentList = [self.body]
        self.componentDict = {"body": self.body}
        
        for leg_pair in self.right_legs + self.left_legs:
            self.componentList.extend(leg_pair)
            
        self.componentList.extend(self.tail_segments)
        
        self.componentList.extend([self.sclera, self.pupil])
        self.componentDict['sclera'] = self.sclera
        self.componentDict['pupil'] = self.pupil

        for i, leg in enumerate(self.right_legs):
            self.componentDict[f'leg_r{i+1}_s1'], self.componentDict[f'leg_r{i+1}_s2'], self.componentDict[f'leg_r{i+1}_s3'] = leg
        for i, leg in enumerate(self.left_legs):
            self.componentDict[f'leg_l{i+1}_s1'], self.componentDict[f'leg_l{i+1}_s2'], self.componentDict[f'leg_l{i+1}_s3'] = leg
        for i, seg in enumerate(self.tail_segments):
            self.componentDict[f'tail_s{i+1}'] = seg
        print(f"--- ModelLinkage initialized with {len(self.componentList)} components. ---")

        self.setJointLimits()
        self.setDefaultPose()
        
        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        
    def setJointLimits(self):
        # Define rotation extents for all creature joints
            
        # Leg rotation limits
        s1_u, s1_v = [-70, 50], [-20, 90]
        s2_u = [0, 140]
        s3_u = [-60, 60]

        for i in range(len(self.right_legs)):
            # Right leg limits
            upper, mid, low = self.right_legs[i]
            upper.setRotateExtent(upper.uAxis, *s1_u)
            upper.setRotateExtent(upper.vAxis, *s1_v)
            mid.setRotateExtent(mid.uAxis, *s2_u)
            low.setRotateExtent(low.uAxis, *s3_u)

            # Left leg limits (mirror v-axis)
            upper, mid, low = self.left_legs[i]
            upper.setRotateExtent(upper.uAxis, *s1_u)
            upper.setRotateExtent(upper.vAxis, -s1_v[1], -s1_v[0])
            mid.setRotateExtent(mid.uAxis, *s2_u)
            low.setRotateExtent(low.uAxis, *s3_u)
    
        # Tail
        tail_u, tail_v = [-45, 45], [-20, 60]
        for seg in self.tail_segments:
            seg.setRotateExtent(seg.uAxis, *tail_u)
            seg.setRotateExtent(seg.vAxis, *tail_v)
        
    def setDefaultPose(self):    
        # Set default angles to form a natural resting pose
        for leg in self.right_legs:
            upper, mid, low = leg
            upper.setDefaultAngle(50, upper.uAxis)  # Flap downward
            upper.setDefaultAngle(45, upper.vAxis)   # Sweep outward
            mid.setDefaultAngle(-70, mid.uAxis)       # Bend up at the 'knee'
            low.setDefaultAngle(30, low.uAxis)      # Bend down at the 'foot'

        for leg in self.left_legs:
            upper, mid, low = leg
            upper.setDefaultAngle(50, upper.uAxis)  # Same downward flap
            upper.setDefaultAngle(-45, upper.vAxis)  # MIRRORED outward sweep
            mid.setDefaultAngle(-75, mid.uAxis)       # Same knee bend
            low.setDefaultAngle(35, low.uAxis)      # Same foot bend

        # Tail points up
        for i, seg in enumerate(self.tail_segments):
            seg.setDefaultAngle(-20 - i * 10, seg.uAxis)   # Curl each segment upward
            
    def pose_idle(self):
        # Default position
        self.setDefaultPose()
        
    def pose_attack(self):
        # tail up, legs flared
        for leg in self.right_legs + self.left_legs:
            upper, mid, low = leg
            upper.setDefaultAngle(60, upper.uAxis)
            mid.setDefaultAngle(-80, mid.uAxis)
            low.setDefaultAngle(30, low.uAxis)
        for seg in self.tail_segments:
            seg.setDefaultAngle(-70, seg.uAxis)
    
    def pose_jump(self):
        # All legs bent  
        for leg in self.right_legs + self.left_legs:
            upper, mid, low = leg
            upper.setDefaultAngle(80, upper.uAxis)
            mid.setDefaultAngle(-100, mid.uAxis)
            low.setDefaultAngle(60, low.uAxis)
        for seg in self.tail_segments:
            seg.setDefaultAngle(-90, seg.uAxis)

    def pose_crawl(self):
        # Crawling pose
        for i, leg in enumerate(self.right_legs + self.left_legs):
            upper, mid, low = leg
            offset = 10 if i % 2 == 0 else -10
            upper.setDefaultAngle(30 + offset, upper.uAxis)
            mid.setDefaultAngle(-40, mid.uAxis)
            low.setDefaultAngle(15, low.uAxis)
        for seg in self.tail_segments:
            seg.setDefaultAngle(-30, seg.uAxis)

    def pose_curl(self):
        # Tail curled into the body
        for seg in self.tail_segments:
            seg.setDefaultAngle(-110, seg.uAxis)
        for leg in self.right_legs + self.left_legs:
            upper, mid, low = leg
            upper.setDefaultAngle(20, upper.uAxis)
            mid.setDefaultAngle(-60, mid.uAxis)
            low.setDefaultAngle(40, low.uAxis)
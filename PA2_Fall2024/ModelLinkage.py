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
        - Facehugger with horns. Circular/Oval body
        - 4 three segmented legs
        - 1 four-segmented tail
        - 2 horns
        - No head, all on a body
        
        """
        # Creating the body
        # Setting color for the creature
        color_body = Ct.ColorType(0.8, 0.7, 0.5)  # Beige for the body
        color_limbs = Ct.ColorType(0.6, 0.5, 0.3)  # Darker color for limbs
        color_limbs_s2 = Ct.ColorType(1, 0, 0)     # Color distinction for each segment
        color_limbs_s3 = Ct.ColorType(0, 0, 1)

        self.body = Sphere(Point((0, 0, 0)), shaderProg, [0.8, 0.5, 1.5], color_body, limb=False)
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
        leg_s1_size = [0.08, 0.08, 0.8]
        leg_s2_size = [0.07, 0.07, 0.7]
        leg_s3_size = [0.06, 0.06, 0.6]

        # Attachment to body
        z_positions = [0.6, 0.2, -0.2, -0.6]
        
        # Using a loop to create the 4 pairs of legs
        for z_pos in z_positions:
            # First (upper) leg segment
            leg_r_s1 = Cylinder(Point((0.5, -0.1, z_pos)), shaderProg, leg_s1_size, color_limbs, limb=True)
            self.body.addChild(leg_r_s1)
            
            # Rotate outward (around z) and downward (around x)
            leg_r_s1.setDefaultAngle(-40, leg_r_s1.vAxis)  # downward tilt
            leg_r_s1.setDefaultAngle(30, leg_r_s1.wAxis)   # outward tilt

            # Second segment (middle joint)
            leg_r_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs_s2, limb=True)
            leg_r_s1.addChild(leg_r_s2)
            leg_r_s2.setDefaultAngle(-50, leg_r_s2.vAxis)  # bend down

            # Third segment (lower joint)
            leg_r_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs_s3, limb=True)
            leg_r_s2.addChild(leg_r_s3)
            leg_r_s3.setDefaultAngle(30, leg_r_s3.vAxis)   # small upward bend

            self.right_legs.append([leg_r_s1, leg_r_s2, leg_r_s3])

            # Left Leg (mirrored)
            leg_l_s1 = Cylinder(Point((-0.5, -0.1, z_pos)), shaderProg, leg_s1_size, color_limbs, limb=True)
            self.body.addChild(leg_l_s1)

            # Mirror local axes for left leg
            leg_l_s1.setU([-1, 0, 0])  # mirror x-axis
            leg_l_s1.setDefaultAngle(-40, leg_l_s1.vAxis)  # downward tilt
            leg_l_s1.setDefaultAngle(-30, leg_l_s1.wAxis)  # outward (mirrored) tilt

            leg_l_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs_s2, limb=True)
            leg_l_s1.addChild(leg_l_s2)
            leg_l_s2.setDefaultAngle(-50, leg_l_s2.uAxis)

            leg_l_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs_s3, limb=True)
            leg_l_s2.addChild(leg_l_s3)
            leg_l_s3.setDefaultAngle(30, leg_l_s3.uAxis)

            self.left_legs.append([leg_l_s1, leg_l_s2, leg_l_s3])
        
        # Horns: 2 Cones in the front
        horn_size = [0.1, 0.1, 0.4]
        self.horn_r = Cone(Point((0.2, 0.2, 0.75)), shaderProg, horn_size, color_body)
        self.horn_l = Cone(Point((-0.2, 0.2, 0.75)), shaderProg, horn_size, color_body)
        self.body.addChild(self.horn_r)
        self.body.addChild(self.horn_l)

        # 4-jointed Tail
        tail_s1_size = [0.12, 0.12, 0.6]
        tail_s2_size = [0.11, 0.11, 0.6]
        tail_s3_size = [0.10, 0.10, 0.5]
        tail_s4_size = [0.09, 0.09, 0.4]
        
        self.tail_s1 = Cylinder(Point((0, 0, -0.75)), shaderProg, tail_s1_size, color_limbs)
        self.body.addChild(self.tail_s1)
        self.tail_s2 = Cylinder(Point((0, 0, tail_s1_size[2])), shaderProg, tail_s2_size, color_limbs)
        self.tail_s1.addChild(self.tail_s2)
        self.tail_s3 = Cylinder(Point((0, 0, tail_s2_size[2])), shaderProg, tail_s3_size, color_limbs)
        self.tail_s2.addChild(self.tail_s3)
        self.tail_s4 = Cylinder(Point((0, 0, tail_s3_size[2])), shaderProg, tail_s4_size, color_limbs)
        self.tail_s3.addChild(self.tail_s4)
        self.tail_segments = [self.tail_s1, self.tail_s2, self.tail_s3, self.tail_s4]
        
        # Shapes/Components Storage
        # Initialize the lists with the body and horns
        self.componentList = [self.body, self.horn_r, self.horn_l]
        self.componentDict = {"body": self.body, "horn_r": self.horn_r, "horn_l": self.horn_l}

        for leg_pair in self.right_legs + self.left_legs:
            self.componentList.extend(leg_pair)
        self.componentList.extend(self.tail_segments)

        for i, leg in enumerate(self.right_legs):
            self.componentDict[f'leg_r{i+1}_s1'] = leg[0]
            self.componentDict[f'leg_r{i+1}_s2'] = leg[1]
            self.componentDict[f'leg_r{i+1}_s3'] = leg[2]
        for i, leg in enumerate(self.left_legs):
            self.componentDict[f'leg_l{i+1}_s1'] = leg[0]
            self.componentDict[f'leg_l{i+1}_s2'] = leg[1]
            self.componentDict[f'leg_l{i+1}_s3'] = leg[2]
        for i, seg in enumerate(self.tail_segments):
            self.componentDict[f'tail_s{i+1}'] = seg
        
        print(f"--- ModelLinkage initialized with {len(self.componentList)} components. ---")
        
        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        
        # Segment 1 (Connects to body): Can sweep forward/back and flap up/down.
        s1_u_range = [-70, 50]  # Flap range (around local x-axis)
        s1_v_range = [-20, 90]  # Sweep range (around local y-axis)

        # Segment 2 (Knee): Can only bend one way.
        s2_u_range = [0, 140]   # Bend range
        
        # Segment 3 (Foot): Can flex up and down.
        s3_u_range = [-60, 60]  # Flex range

        for i in range(len(self.right_legs)):
            # Right legs
            self.right_legs[i][0].setRotateExtent(self.right_legs[i][0].uAxis, s1_u_range[0], s1_u_range[1])
            self.right_legs[i][0].setRotateExtent(self.right_legs[i][0].vAxis, s1_v_range[0], s1_v_range[1])
            self.right_legs[i][1].setRotateExtent(self.right_legs[i][1].uAxis, s2_u_range[0], s2_u_range[1])
            self.right_legs[i][2].setRotateExtent(self.right_legs[i][2].uAxis, s3_u_range[0], s3_u_range[1])

            # Left legs (mirrored sweep range)
            self.left_legs[i][0].setRotateExtent(self.left_legs[i][0].uAxis, s1_u_range[0], s1_u_range[1])
            self.left_legs[i][0].setRotateExtent(self.left_legs[i][0].vAxis, -s1_v_range[1], -s1_v_range[0]) # Mirrored
            self.left_legs[i][1].setRotateExtent(self.left_legs[i][1].uAxis, s2_u_range[0], s2_u_range[1])
            self.left_legs[i][2].setRotateExtent(self.left_legs[i][2].uAxis, s3_u_range[0], s3_u_range[1])
            
        # --- Set Joint Limits for Tail ---
        tail_u_range = [-45, 45] # Wag left/right
        tail_v_range = [-20, 60] # Curl up/down

        for seg in self.tail_segments:
            seg.setRotateExtent(seg.uAxis, tail_u_range[0], tail_u_range[1])
            seg.setRotateExtent(seg.vAxis, tail_v_range[0], tail_v_range[1])
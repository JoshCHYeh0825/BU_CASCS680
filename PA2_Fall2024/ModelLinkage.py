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
        - 4 three-jointed limbs/legs
        - 1 four-jointed tail
        - 2 horns on its 2 eyes
        - No head, all on a body
        
        """
        # Creating the body
        # Setting color for the creature
        color_body = Ct.ColorType(0.8, 0.7, 0.5)  # Beige for the body
        color_limbs = Ct.ColorType(0.6, 0.5, 0.3)  # Darker color for limbs

        # Setting Dimensions
        """
        Oval with size [0,8, 0,5, 1.5]
        Beige color
        Body at origin 0, 0, 0
        """
        self.body = Sphere(Point(0, 0, 0), shaderProg, [0.8, 0.5, 1.5], color_body, limb=False)
        self.addChild(self.body)

        # 8 triple-jolinted limbs
        """
        8 limbs will be built using mirrored pairs (lefct and right).
        Each leg will copntain 3 cylinder segments, each a child of the previous one to establish the triple-jointed nature
        
        """
        # Storing all leg components to left and right
        self.right_legs = []
        self.left_legs = []
        
        # Defining the size of the legs
        leg_s1_size = [0.08, 0.08, 0.8]
        leg_s2_size = [0.07, 0.07, 0.7]
        leg_s3_size = [0.06, 0.06, 0.6]
        
        # Using a loop to create the 4 pairs of legs
        for z_pos in [0.6, 0.2, -0.2, -0.6]:
            # Right Leg
            leg_r_s1 = Cylinder(Point((0.5, 0, z_pos)), shaderProg, leg_s1_size, color_limbs)
            self.body.addChild(leg_r_s1)
            leg_r_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs)
            leg_r_s1.addChild(leg_r_s2)
            leg_r_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs)
            leg_r_s2.addChild(leg_r_s3)
            self.right_legs.append([leg_r_s1, leg_r_s2, leg_r_s3])

            # Left Leg (Mirrored)
            leg_l_s1 = Cylinder(Point((-0.5, 0, z_pos)), shaderProg, leg_s1_size, color_limbs)
            self.body.addChild(leg_l_s1)
            leg_l_s2 = Cylinder(Point((0, 0, leg_s1_size[2])), shaderProg, leg_s2_size, color_limbs)
            leg_l_s1.addChild(leg_l_s2)
            leg_l_s3 = Cylinder(Point((0, 0, leg_s2_size[2])), shaderProg, leg_s3_size, color_limbs)
            leg_l_s2.addChild(leg_l_s3)
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
        
        # Shapes/Components Storage
        # Initialize the lists with the body and horns
        self.componentList = [self.body, self.horn_r, self.horn_l]
        self.componentDict = {"body": self.body, "horn_r": self.horn_r, "horn_l": self.horn_l}

        # Create the list of tail segments
        self.tail_segments = [self.tail_s1, self.tail_s2, self.tail_s3, self.tail_s4]

        # Add all the legs to the componentList
        for leg_pair in self.right_legs + self.left_legs:
            self.componentList.extend(leg_pair)

        # Add the tail to the componentList
        self.componentList.extend(self.tail_segments)

        # Add all the legs to the componentDict
        for i, leg in enumerate(self.right_legs):
            self.componentDict[f'leg_r{i+1}_s1'] = leg[0]
            self.componentDict[f'leg_r{i+1}_s2'] = leg[1]
            self.componentDict[f'leg_r{i+1}_s3'] = leg[2]
        for i, leg in enumerate(self.left_legs):
            self.componentDict[f'leg_l{i+1}_s1'] = leg[0]
            self.componentDict[f'leg_l{i+1}_s2'] = leg[1]
            self.componentDict[f'leg_l{i+1}_s3'] = leg[2]

        # Add all the tail segments to the componentDict
        for i, seg in enumerate(self.tail_segments):
            self.componentDict[f'tail_s{i+1}'] = seg
        
        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
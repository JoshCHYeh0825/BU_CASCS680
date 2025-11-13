Fall 2025
Chih Han Yeh
CASCS680

PA2 - 3D Modeling and Transformation

Changes made for each TODOs:

### myTransformation – `Component.py`

To implement the correct transformation logic, the correct order of matrixs multiplication is implemented.
Order of matrix transformation: Scale, Rotate (U, V, then W), and translate.
`myTransformation = translationMat @ rotationMatW @ rotationMatV @ rotationMatU @ scalingMat`

### Creature Creation – `ModelLinkage.py`

Under the `def __init__()` function is where I defined all the shapes and components to the creature I had in mind.
The creature is componsed of:

* A central body - Using a scaled `Sphere` object to create a 3 dimensional oval, making it the root/parent of the hierarchy
* 8 triple-jointed legs - All built using the `Cylinder` object, linking three cylinders end to end and attaching them to the body
  * First it was 4 legs on the right side, then mirrored to the left
* A quad-jointed tail - Similar to the legs, built using the `Cylinder` object, attached to the rear of the main body
* An eye - composed of two `Sphere` objects, a sclera and a child object for the pupil

### Joint Behavior and Default Pose – `ModelLinkage.py`

The joint behavior are defined using two new methods within `ModelLinkage`.

* `setJointLimits()` : A method using `setRotateExtent()` which sets limits to the the rotation range of motion. Since the left side is mirrored on the right, the rotation axis on the `vAxis` are negated or rather inversionf of the right.
* `setDefaultPose())`: A method whgich sets the initial angle and positions of the limb segments I want for the creature, as the name suggests to its default.

### Multi-Select and Multiposes – `Sketch.py`

* Pressing the 'L' key toggles all Leg components
* Pressing the 'T' Key toggles all Tail components
* Both are managed by a helper funciton, `toggle_group_selection` which would rotate the aforementioned components using the Up/DOwn and axis selection logic that was already implemented
* Keys 1-5 wouldn change the pose of the creature to 5 pre-determined poses, all poses does not move the body but rather just the tail and leg segments

### Eye Tracking w/ Quaternionis– `Sketch.py & ModelLinkage.py`

* An consisting of a black sclera and white pupil is implemented wihthin the ModelLinkage.py file, same as the other body components of the creature.
* Eye-tracking is featured within the `Interrupt_MouseMoving` function, which would calculate the mouse cursoe using `unprojectCancas`, determining the direciton vector from the eye's perception to the mouse's position.
* Rotation is achieved using quarternions. Rotaiton axes are calculated through the cross product of the eye's default forward vector (0, 0, -1) and the new direction vector. The rotation angle is calculated from the dot product of these two vectors. A quaternion is then constructed from this axis-angle pair and applied directly to the pupil component using `pupil.setQuaternion(q)`, making it follow the cursor.

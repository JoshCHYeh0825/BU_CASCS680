Fall 2025
Chih Han Yeh
CASCS680

PA3 - 3D Vivarium

# Creature Design

## Prey

* Components
  * A spherical main body that uses a `Sphere`.
  * Two cylinders and a cone tip acting as the tail that would be animated.
* Joint limitations and movement
  * The middle tail segment `tail_s2` which is animated would move with limits of -30 to 30 degrees on its v-axis, acting as if it is a tail.

## Predator

* Components
  * A spherical main body that uses a `Sphere`.
  * Two cylinders and a cone tip acting as the tail that would be animated.
  * Mirrored symmetrical cylinders and cones acting as pincers that would also be animated.
* Joint limitations and movement
  * The middle tail segment `tail_s2` which is animated would move with limits of -30 to 30 degrees on its v-axis, just like the prey.
  * The pincers are similarly animated but limited to -10 to 30 and 10 to 30 degrees respectively for the mirrored pincors. The animated segment of the pincers are the cylinders.

# Movement, Collision, and Positions

## stepForward()

`def stepForward(self, components, tank_dimensions, vivarium)` is the function implemented to both preys and predators with some subtle changes to how one interact with the other

* First the creature would loop over every other creature so it wouldn't interact with itself

```
for obj in vivarium.creatures:
    if obj is self:
        continue
```

* Next is the logic where we apply the predator chasing prey behavior and the prey evading predator behavior.
  For the predator:

  ```
  # Chasing prey
  if obj.species_id == 2 and dist < 4.5:
  	self.apply_attraction(obj, strength=0.01)

  # Bounce away from non prey/other predator upon collision
  elif obj.species_id == 1 and self.detect_collision(obj):
  	normal = self.currentPos.coords - obj.currentPos.coords
  	self.reflect_direction(normal)
  ```

  `obj.species_id` identifies if the creature is a prey or predator, with prey being 2 and predator being 1. If the predator is within the certain range (4.5) of the prey it would be attracted towards it, otherwise it would bounce away.

For the prey:

```
 # Evading predator
if obj.species_id == 1and dist <3:
	self.apply_repulsion(obj, strength=0.02)

# Bounce away from non prey/other predator upon collision
elif obj.species_id == 2andself.detect_collision(obj):
	normal = self.currentPos.coords - obj.currentPos.coords
	self.reflect_direction(normal)

 # Eaten when colliding with predator
	if obj.species_id == 1 and self.detect_collision(obj):
		vivarium.delObjInTank(self)
                vivarium.creatures.remove(self)
               	return
```

`self.reflect_direction(normal)` and computing normal within the collision loop allows the creature to bounce away with other creatures with the same id.
Additionally, when the prey collides with a predator, `delObjInTank` is called and the prey would remove itself.

Next is the boundary collision and reflection behaviors of the creature with the vivarium wall.

```
# Probe the next position
nextPos = self.currentPos.coords + self.direction * self.step_size
# Track whether a bounce happened
bounce = False

# X-axis bouce
if ((nextPos[0] + self.bound_radius) > tank_dimensions[0] / 2) or ((nextPos[0] - self.bound_radius) < -(tank_dimensions[0] / 2)):
	self.direction[0] *= -1
	bounce = True
	# Clamp inside wall
	nextPos[0] = np.clip(nextPos[0], -(tank_dimensions[0] / 2 - self.bound_radius), (tank_dimensions[0] / 2 - self.bound_radius))

# Y-axis bounce
if ((nextPos[1] + self.bound_radius) > tank_dimensions[1] / 2) or ((nextPos[1] - self.bound_radius) < -(tank_dimensions[1] / 2)):
	self.direction[1] *= -1
	bounce = True
	nextPos[1] = np.clip(nextPos[1], -(tank_dimensions[1] / 2 - self.bound_radius), (tank_dimensions[1] / 2 - self.bound_radius))

# Z-axis bounce
if ((nextPos[2] + self.bound_radius) > tank_dimensions[2] / 2) or ((nextPos[2] - self.bound_radius) < -(tank_dimensions[2] / 2)):
	self.direction[2] *= -1
	bounce = True
	nextPos[2] = np.clip(nextPos[2], -(tank_dimensions[2] / 2 - self.bound_radius), (tank_dimensions[2] / 2 - self.bound_radius))
```

`nextPos` is the next postiion variabl that would cehck for boundary collisions along each axis.
For each of the three axes (x, y, z), if the new position moves beyond the wall of the vavarium (half of the tank dimension - radius of creature bounding sphere), the motion direction on the axis is inverted and the position is clamped back inside the vivarium `self.direction[i] *= -1`. This would keep the creatures within the vivarium.

```
# Compute final position
finalPos = self.currentPos.coords + self.direction * self.step_size
self.setCurrentPosition(Point(finalPos))

# Only reorient if a bounce occurred — prevents rapid flipping along wall
if bounce:
	self.rotateDirection(Point(self.direction))
```

The final parts of `stepForward()` is the final position calculations, where the final position is updated just as `nextPos` and the predator's orientation is updated to match the direction of travesal with the call of `rotateDirection`.

## rotateDirection()

As mentioned above `rotateDirection` is the function that was implemented spcifically for the creature to continuously face the direction it is traversing within the bounds of the vivarium box. That way the creatures would continuously face the normal vector upon colliding with any of the walls of the environment.
The function is defined within `ENvironmentbject.py` as part of `TODO 4`.

```
def rotateDirection(self, v1):
    forward_v = Point([0, 0, 1])
    v1.normalize()
    dot_prod = forward_v.dot(v1)
    q = Quaternion()
```

* `forward_v` defines the local "forward" facing vector (positive z-axis)
* The target direction `v1` is normalized and dotted with `forward_v` as a measure of how aligned the creature is with `v1`

### Case 1

```
if dot_prod > 0.999:
    self.clearQuaternion()
    return
```

If the creature's facing direction is the same as `v1` no rotation is required, `clearQuarternion()` would reset any rotational offsets.

### Case 2

```
elif dot_prod < -0.999:
    angle = math.pi
    s = math.cos(angle / 2.0)
    v0 = 0 * math.sin(angle / 2.0)
    v1 = 1 * math.sin(angle / 2.0)
    v2 = 0 * math.sin(angle / 2.0)
    q.set(s, v0, v1, v2)
```

If the target direction is the opposite of the forward vector (180 degrees apart), a quarternion is constructed with the purpose of rotation of $\pi$ - radians around the y-axis. This ensures the creature would rotate normally when it reverse the direction.

### Case 3

```
else:
    axis = v1.cross3d(forward_v).normalize()
    angle = math.acos(dot_prod)
    half_sin = math.sin(angle / 2.0)
    half_cos = math.cos(angle / 2.0)

    q.set(half_cos,
          (axis[0] * half_sin),
          (axis[1] * half_sin),
          (axis[2] * half_sin))
```

This is the general case. The rotation axis is computed using the cross product between the forward and target directions `axis = v1.cross3d(forward_v).normalize()`. The rotation angle is computed via the arc cosine of the dot product. Then the quarternion is set as: $q=(cos(θ/2), \hat u_x sin(θ/2), \hat u_y sin(θ/2), \hat u_z sin(θ/2))$ where $\hat u$ is the normalized axis. The rotation is set at the end using `self.setQuaternion(q)`.

# Additions to EnvironmentObject.py

There are several different helper functions that were defined within EnvironmentObject.py assisting in the `stepForward()` functions used to define creature movements of both the Prey and Predator, besides `rotateDirection`.

```
def distance_to(self, other):
        # Compute Euclidean distance to another EnvironmentObject
        return np.linalg.norm(self.currentPos.coords - other.currentPos.coords)
```

`distance_to()` is a helper function used in `stepForward()` which computes the euclidean distance between the creature and another object. Using `currentPos` the function would return a scalar distance value with the normalize function.

```
def detect_collision(self, other):
        # Detect bounding-sphere collision
        if self is other:
            return False
        dist = self.distance_to(other)
        return dist < (self.bound_radius + other.bound_radius)
```

`detect_collision()` detects whether two creatures' bounding spheres would interact by checking if the distance between the centers of the spheres are less than the sum of the radii.

```
    def reflect_direction(self, normal):
        # Reflect movement direction defined by normal
        n = normal / np.linalg.norm(normal)
        self.direction = self.direction - 2 * np.dot(self.direction, n) * n
        self.direction /= np.linalg.norm(self.direction)
        self.rotateDirection(Point(self.direction)
```

`reflect_direction` reflects a movement vector off of surface after collision/bounce. The normalized collision normal vector is used to compute the rflected direction vector: $r = d - 2(d * n) n$. d is the incoming direction and r is the reflected vector. r is normalized and `rotateDirection()` iis called to visually rotate the creature to face this new direction.

```
def apply_attraction(self, target, strength=0.01):
    delta = target.currentPos.coords - self.currentPos.coords
    delta /= np.linalg.norm(delta)
    self.direction += strength * delta
    self.direction /= np.linalg.norm(self.direction)
    self.rotateDirection(Point(self.direction))
```

`apply_attraction()` computes the vector from the predator to the prey, normalizes that vector, Gradually add the vector (fractionally) to the predator's direction before being normalized and reorientated to the creature. This steers the predator towards the prey.

```
def apply_repulsion(self, target, strength=0.02):
    delta = self.currentPos.coords - target.currentPos.coords
    delta /= np.linalg.norm(delta)
    self.direction += strength * delta
    self.direction /= np.linalg.norm(self.direction)
    self.rotateDirection(Point(self.direction))

```

`apply_repulsion` applies the same logic to the prey but normalizes the predator-prey vector and scale it by strength so the prey would be more repulsed than the predator's attraction.

# Simulating Food

## Food Class

The simulating of dropping food is defined within `Vivarium.py`. The food objects would fall slowly to the bottom by the tank unless it is consumed first by the creatures they collide with. Below are a list of attribtues given to a `Food` object:

* `velocity` - Small downward velocity vector [0, -0.002, 0] which controls how fast the object falls within the vivarium
* `bound_radius` - Radius of the bounding sphere used to detect collision with creatures and the vivariu environment
* `eaten` - A flag which tracks if the food object collides with a creature and would be consumed by any creature

```
def stepForward(self, tank_dimensions):
    nextPos = self.currentPos.coords + self.velocity
    bottom_y = -(tank_dimensions[1] / 2) + self.bound_radius
    if nextPos[1] < bottom_y:
        nextPos[1] = bottom_y
        self.velocity = np.array([0.0, 0.0, 0.0])
    self.setCurrentPosition(Point(nextPos))
```

The same `stepForward()` method that is used to define the creatures' movement applied to the food objects. The difference is the direction of movement is negative y and given the velocity with the attributes that were defined within `def __init__()`. Another distinct feature between this `stepForward()` from the others' is that the motion of the object is stopped when it reaches the bottom of the tank, and would not reflect.

## Changes in the Vivarium Class

There are several different changes made to the provided `Vivarium.py` file aside from the addition of the `Food` class.

Within `def animationUpdate()` is the addition of a for loop in order to define the logic for a food object being consumed.

```
for food in self.food_obj[::-1]:
	food.stepForward(self.tank_dimensions)
        for creature in self.creatures:
            dist = np.linalg.norm(np.array(creature.currentPos.coords) - + np.array(food.currentPos.coords))
            if dist < (creature.bound_radius + food.bound_radius):
                self.delObjInTank(food)
                self.food_obj.remove(food)
                break
```

The logic goes: If the distance between a creature and food object is less than the sum of their sphere radii, the `eaten` flag turns true indicative of food being eaten, then the food object is deleted from the tank and `food_obj` list using `delObjInTank()`.

Food is spawned through the function `def spawnFood().`

```
def spawnFood(self):
    x = random.uniform(-self.tank_dimensions[0] * 0.4, self.tank_dimensions[0] * 0.4)
    y = self.tank_dimensions[1] * 0.3
    z = random.uniform(-self.tank_dimensions[2] * 0.4, self.tank_dimensions[2] * 0.4)
    pos = Point((x, y, z))

    food = Food(self.parent, pos, self.shaderProg)
    self.addNewObjInTank(food)
    self.food_obj.append(food)
    food.initialize()
```

The function would randomly generate a position near the top of the vivarium. It would then create a new instance of Food in that position, adds it to the environment with `addNewObjInTank()` whilst simultaneously updating the `food_obj` list, then calls `initialize()` to render it into the GUI.

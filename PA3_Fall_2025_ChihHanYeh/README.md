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

## Movement and Collision

### stepForward()

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

# Compute final position
finalPos = self.currentPos.coords + self.direction * self.step_size
self.setCurrentPosition(Point(finalPos))

# Only reorient if a bounce occurred — prevents rapid flipping along wall
if bounce:
	self.rotateDirection(Point(self.direction))
```

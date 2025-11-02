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

`stepForward()` is the function implemented to both preys and predators with some subtle changes to how one interact with the other

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
```

`self.reflect_direction(normal)` and computing normal within the collision loop allows the creature to bounce away with other creatures with the same id.

Next is the boundary collision and reflection behaviors of the creature with the vivarium wall.

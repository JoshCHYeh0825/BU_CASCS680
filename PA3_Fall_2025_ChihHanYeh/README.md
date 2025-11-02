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

`stepForward()` is the function implemented to both

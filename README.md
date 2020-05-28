# Particle-Filter

## Monte Carlo Localization of a mobile robot using landmarks


Consider a planar robot with three DOFs x = (x, y, θ) operating in a world of size 100 × 100. The world
includes six landmarks at: m = {(20, 20),(50, 20),(80, 20),(80, 80),(50, 80),(20, 80)} .

The robot can take two motor commands, a turn movement command u1, (u1 ∈ [0, 2π)) and a forward
movement command u2 (u2 > 0). The deterministic motion model of the robot is given by

- θ '= θ + u1 ,
- x' = x + u2 cos θ' ,
- y' = y + u2 sin θ'

The World class defines the world of the robot and includes a plot function. The Robot class initializes a robot with an arbitrary
pose in the world. This class includes the following functions:

- set: sets new pose of the robot

- print: prints the pose of the robot

- plot: plots the robot in the world [different colors and different plot styles - ’robot’ and ’particle’
- can be chosen]

- set noise: sets the noise parameters (forward noise, turn noise, sense noise range,
sense noise bearing)

**Remarks:**
1. It is assumed that the world is cyclic, i.e., if the robot exits on one side it will re-enter on the opposing
side.
2. It is assumed that the problem of correspondences between measurement and number of landmark is
solved, i.e., the i-th measurement corresponds to the i-th landmark.

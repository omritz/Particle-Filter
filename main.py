import World
import Robot
import Ploter
import numpy as np
import random
import matplotlib.pyplot as plt
import copy

np.random.seed(321)


def ex_a(myWorld, robi, bob, matan):
    robi.set(45, 45, 0)
    bob.set(50, 60, np.pi/2)
    matan.set(70, 30, 3*np.pi/4)
    myWorld.plot(show=False)
    robi.plot("green",show=False)
    bob.plot("red",show=False)
    matan.plot(show=False)
    plt.show()


def draw_path(tupleList, linestyle, color):
    x, y = zip(*tupleList)
    plt.plot(x, y, color=color, markersize = 2, linestyle = linestyle)     

def ex_e_f():
    commands_set = {'1': (0, 60), '2': (np.pi/3, 30), '3': (np.pi/4, 30), '4': (np.pi/4, 20), '5': (np.pi/4, 40)}
    world= World.World()
    bob = Robot.Robot()
    bob.set_noise(0, 0, 0, 0)
    bob.set(10, 15, 0)
    world.plot(show=False)
    bob.plot("green", show=False, markersize=5)
    commandedPath = []
    truePath = []
    commandedPath.append((bob.x, bob.y))
    truePath.append((bob.x, bob.y))
    for key, command in commands_set.items():
        bob.move(command[0], command[1])
        commandedPath.append((bob.x, bob.y))
        bob.plot("green", show=False, markersize=5)
    draw_path(commandedPath, "dotted", 'green')
    bob.set_noise(6, 0.1, 5, 0.3)
    bob.set(10, 15, 0)
    for key, command in commands_set.items():   
        bob.move(command[0], command[1])
        truePath.append((bob.x, bob.y))
        bob.plot("b", show=False, markersize=5)
    draw_path(truePath, "solid", 'blue')
    plt.show()    


def calcMean(particles):
    x = 0
    y = 0
    for particle in particles:    
        x += particle.x
        y += particle.y 
    return (x/len(particles), y/len(particles))


def particle_filter():
    world = World.World()
    rob = Robot.Robot()
    rob.set(10, 15, 0)
    rob.set_noise(6, 0.1, 5, 0.3)
    commands_set = {'1': (0, 60), '2': (np.pi/3, 30), '3': (np.pi/4, 30), '4': (np.pi/4, 20), '5': (np.pi/4, 40)}
    particles = []
    commandedPath = []
    truePath = []
    particlesMeans = []
    commandedPath.append((rob._x, rob._y))
    truePath.append((rob.x, rob.y))
    particlesMeans.append((rob.x, rob.y))
    N = 1000
    world.plot(show=False)
    rob.plot("black",show=False)
    for i in range(N):
        ''' Initiate particles'''
        p = Robot.Robot()
        p.set(10,15,0)
        p.set_noise(6, 0.1, 5, 0.3)
        particles.append(p)
    for key, command in commands_set.items():
        ''' Robot's move'''
        rob.move(command[0],command[1])
        commandedPath.append((rob._x, rob._y))
        truePath.append((rob.x, rob.y))
        ''' Robot's measurements '''
        measurements = []
        measurements = rob.sense(world.get_landmarks())
        for particle in particles:
            ''' Particle's move  '''
            particle.move(command[0],command[1])
            particle.plot("black",style="particle",show=False)
        weights = []
        for particle in particles:
            ''' Calculate weights for each particle '''
            weights.append(particle.measurementProb(world.get_landmarks(), measurements))
        ''' Normalize weights '''    
        sumWeights = sum(weights)
        weights = np.array(weights)
        weights = weights/sumWeights
        ''' Resample particles '''
        indexes = np.random.choice(np.arange(0,N) ,size = N, p = weights)
        resampleParticles = []
        for index in indexes:
            resampleParticles.append(copy.deepcopy(particles[index]))
        particles = resampleParticles    
        rob.plot("black",show=False)
        for particle in particles:
            particle.plot("grey",style="particle",show=False)
        particlesMeans.append(calcMean(particles)) 
    draw_path(commandedPath, "dotted", 'green')
    draw_path(truePath, "solid", 'blue')
    draw_path(particlesMeans, "dashdot", 'red')       
    plt.show()


if __name__ == "__main__":
    myWorld = World.World()
    robi = Robot.Robot()
    bob = Robot.Robot()
    matan = Robot.Robot()
    ex_a(myWorld, robi, bob, matan)
    ex_e_f()
    particle_filter()

import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.stats import norm
from Ploter import config_plot


class Robot:
    """
    the robot class, we will use this to describe a robot
    """
    def __init__(self, world_size=100):
        """
        creating a robot object
        :param world_size: the world size in pixels
        """
        self._world_size = world_size
        # pose declaration
        self.x = np.random.rand() * self._world_size
        self.y = np.random.rand() * self._world_size
        self.theta = np.random.rand() * 2 * np.pi
        # noise declaration
        self.forward_noise = 0
        self.turn_noise = 0
        self.sense_noise_range = 0
        self.sense_noise_bearing = 0
        # addatives
        self.measurments = []
        self._theta = 0
        self._x = 0
        self._y = 0

    def set(self, new_x, new_y, new_orientation):
        """
        setting the configuration of the robot
        :param new_x: the new x coordinate
        :param new_y: the new y coordinate
        :param new_orientation: the new orientation
        """
        if new_x < 0 or new_x >= self._world_size:
            raise Exception('X coordinate out of bound')

        if new_y < 0 or new_y >= self._world_size:
            raise Exception('Y coordinate out of bound')

        if new_orientation < 0.0 or new_orientation >= 2 * np.pi:
            Exception('Orientation must be in [0,2pi]')

        self.x = new_x
        self.y = new_y
        self.theta = new_orientation
        self._theta = new_orientation
        self._x = new_x
        self._y = new_y


    def print(self):
        """"
        printing the pose
        """
        print('[x= {} y={} heading={}]'.format(self.x, self.y, self.theta))

    def plot(self, mycolor="b", style="robot", show=True, markersize=2):
        """
        plotting the pose of the robot in the world
        :param mycolor: the color of the robot
        :param style: the style to plot with
        :param show: if to show or not show - used to create a new figure or not
        """
        if style == "robot":
            phi = np.linspace(0, 2 * np.pi, 101)
            r = 1
            # plot robot body
            plt.plot(self.x + r * np.cos(phi), self.y + r * np.sin(phi), color=mycolor)
            # plot heading direction
            plt.plot([self.x, self.x + r * np.cos(self.theta)], [self.y, self.y + r * np.sin(self.theta)], color=mycolor)

        elif style == "particle":
            plt.plot(self.x, self.y, '.', color=mycolor, markersize=markersize)
        else:
            print("unknown style")

        if show:
            plt.show()

    def set_noise(self, new_forward_noise, new_turn_noise,new_sense_noise_range, new_sense_noise_bearing):
        """
        setting the noise if pose of the robot
        :param new_forward_noise: the noise for moving forward
        :param new_turn_noise: the noise in the turn of the robot
        :param new_sense_noise_range: the noise in range measurement
        :param new_sense_noise_bearing: the noise in bearing measurement
        """
        self.forward_noise = new_forward_noise
        self.turn_noise = new_turn_noise
        self.sense_noise_range = new_sense_noise_range
        self.sense_noise_bearing = new_sense_noise_bearing



    def get_pose(self):
        """
        returning the pose vector
        :return: (x, y, theta) the pose vector
        """
        return self.x, self.y, self.theta


    def move(self, turn_movement_command, forward_movement_command):
        ''' Ex B '''
    
        if turn_movement_command < 0 or turn_movement_command >= 2*np.pi :
            raise Exception('Turn movement command out of bound')
        if forward_movement_command <= 0 :
            raise Exception('Forward movement command out of bound')

        '''Store the commanded points '''
        self._theta += turn_movement_command   
        self._x += forward_movement_command*np.cos(self._theta) 
        self._y += forward_movement_command*np.sin(self._theta) 
        self._theta %= (2*np.pi)   
        self._x  %= self._world_size
        self._y %= self._world_size

        ''' Add noise '''
        turn_movement_command += np.random.normal(0, self.turn_noise)
        forward_movement_command += np.random.normal(0, self.forward_noise)
  
        self.theta += turn_movement_command
        self.x += forward_movement_command*np.cos(self.theta)
        self.y += forward_movement_command*np.sin(self.theta)
        self.theta %= (2*np.pi) 
        self.x %= self._world_size
        self.y %= self._world_size

    def calculateDistance(self,mx,my):
        return (math.sqrt((mx - self.x)**2 + (my - self.y)**2)) % self._world_size
         

    def calculateBearing(self, mx, my):
        return (math.atan2(my - self.y, mx - self.x) - self.theta) % np.pi

    def sense(self, landmarks):
        ''' Ex C '''
        self.measurments.clear()
        for landmark in landmarks:
            distance = float(self.calculateDistance(landmark[0],landmark[1]) + np.random.normal(0, self.sense_noise_range, 1))
            bearing  = float(self.calculateBearing(landmark[0],landmark[1]) + np.random.normal(0, self.sense_noise_bearing, 1))
            self.measurments.append((distance, bearing))   
        return self.measurments    

    def measurementProb(self, landmarks, measurments):
        ''' Ex D '''
        q = 1  
        for i in range(len(landmarks)):
            dist = float(self.calculateDistance(landmarks[i][0],landmarks[i][1]))
            bear = float(self.calculateBearing(landmarks[i][0],landmarks[i][1]))
            q *= norm.pdf(dist, measurments[i][0] , self.sense_noise_range) * norm.pdf(bear, measurments[i][1], self.sense_noise_bearing)
        return q

    




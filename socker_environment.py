import gym
from gym import spaces
from socker_constants import *
from socker_render import SockerRender
from socker_field import Field
import numpy as np

class SockerEnvironement(gym.Env):
    """SSL Socker Junior Env"""
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.team = "blue" # TODO !!!
        
        super(SockerEnvironement, self).__init__()
        # Actions of robots : [x1 y1 o1 kick1, x2, y2, o2, kick2]
        low_action = [-MAX_SPEED, -MAX_SPEED, -MAX_ANGULAR_SPEED, 0]
        high_action = [MAX_SPEED, MAX_SPEED, MAX_ANGULAR_SPEED, 1]
        self.action_space = spaces.Box(shape=(2,4), 
                                       low=np.array([low_action, low_action]), 
                                       high=np.array([high_action, high_action]), 
                                       dtype=np.float32)
        # Observations : [x, y, o, °x, ..., °°x, ...] Ball, Robot1, ...
        ball_low_observation = [-FIELD_WIDTH/2, -FIELD_HEIGHT/2, 0, -MAX_BALL_SPEED, -MAX_BALL_SPEED, 0, -999,-999, 0]
        ball_high_observation = [FIELD_WIDTH/2, FIELD_HEIGHT/2, 0, MAX_BALL_SPEED, MAX_BALL_SPEED, 0, 999,999, 0]
        robot_low_observation = [-FIELD_WIDTH/2+ROBOT_SIZE/2, -FIELD_HEIGHT/2+ROBOT_SIZE/2, -180, -MAX_SPEED, -MAX_SPEED, -MAX_ANGULAR_SPEED, -999,-999, -999]
        robot_high_observation = [FIELD_WIDTH/2-ROBOT_SIZE/2, FIELD_HEIGHT/2-ROBOT_SIZE/2, 180, MAX_SPEED, MAX_SPEED, MAX_ANGULAR_SPEED, 999, 999, 999]
        self.observation_sace = spaces.Box(shape=(5,9), 
                                           low=np.array([ball_low_observation, robot_low_observation, robot_low_observation, robot_low_observation, robot_low_observation]),
                                           high=np.array([ball_high_observation, robot_high_observation, robot_high_observation, robot_high_observation, robot_high_observation]),
                                           dtype=np.float32)
        self.field = Field()
        self._sockerRender = None
        
    def step(self, actions):
        self.field.step(actions, self.team)
        # Calculation to do here
        #return obs, reward, done, infos
        
    def reset(self):
        self.field.reset('classic')
    
    def render(self, mode='human', close=False):
        self.sockerRender.render(self.field)
    
    @property
    def sockerRender(self):
        if self._sockerRender is None:
            self._sockerRender = SockerRender()
        return self._sockerRender
    
test = SockerEnvironement()
import time
test.field.robots[0].coord = (-200, 0, 0)
for i in range(100):
    test.render()
    test.step( [200, 0, 0, 0,
                0, 0, 0, 0] )
    time.sleep(TIME_STEP)
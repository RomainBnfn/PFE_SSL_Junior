import gym
from gym import spaces
from PygameRender import PygameRender

class SockerEnvironement(gym.Env):
    """SSL Socker Junior Env"""
    metadata = {'render.modes': ['human']}
    def __init__(self, width, height, x, y):
        super(SSLSockerEnvironement, self).__init__()
        # Actions of robots : [x1 y1 o1 kick1, x2, y2, o2, kick2]
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255, shape=
                        (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)
        #
        self.field = Field(w, h, a, b)
        self.pygameRender = PygameRender()
        
    def step(self, action):
        return self.field.step(action, t)
        
    def reset(self):
        self.field.reset()
    
    def render(self, mode='human', close=False):
        self.pygameRender.render(self.field)
    
class Movable:
    def __init__(self, x, y, o, ddX, ddY, ddO, weight):
        self.reset(x, y, o, ddX, ddY, ddO)
        self.weight = weight
        
    def move(t, dX, dY, dO, r): #r : rugosite ?
        # Caculate new x, y, o, ddx, ddy, ddo
        return x, y, o
    
    def reset(x, y, o, ddX, ddY, ddO):
        self.coord = (x, y, o)
        self.acceleration = (ddX, ddY, ddO)
    
class Field:
    def __init__(self, width, height, a, b):
        self.width = width
        self.height = height
        # robot weight
        self.redTeam = [Robot(a, b, 180), Robot(a, -b, 180)]
        self.blueTeam = [Robot(-a, b, 0), Robot(-a, -b, 0)]
        self.ball = Ball(0, 0)
        self.ended = False
    
    def reset(mode='classic'):
        if mode == 'classic':
            a =
            b =
            self.ball.reset(0, 0, 0, 0, 0, 0)
            self.redTeam[0].reset(a, b, 180)
            self.redTeam[1].reset(a, -b, 180)
            self.blueTeam[0].reset(-a, b, 0)
            self.blueTeam[1].reset(-a, -b, 0)
        
    def step(actions, t):
        # Execute one time step within the environment
        (dx1, dy1, do1, kick1, dx2, dy2, do2, kick2) = action
        # update directive
        return obs, reward, done, infos
        
    def render():
        pass
        
class Robot(Movable):
    def __init__(self, x, y, o):
        super().__init__(x, y, o, 0, 0, 0, 250)
        print(self.x)

class Ball(Movable):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 0, 0, 10)
        print(self.x)
)

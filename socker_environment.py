import gym
from gym import spaces

class SockerEnvironement(gym.Env):
  """SSL Socker Junior Env"""
  
  metadata = {'render.modes': ['human']}

  def __init__(self, width, height, x, y):
      """[summary]

      Args:
          width ([float]): Width of the field (x)
          height ([float]): Height of the field (y)
          x ([float]): [description]
          y ([float]): [description]
      """
    super(SSLSockerEnvironement, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
    # Example for using image as input:
    self.observation_space = spaces.Box(low=0, high=255, shape=
                    (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

  def step(self, action):
    # Execute one time step within the environment
    ...
  def reset(self):
    # Reset the state of the environment to an initial state
    ...
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...
    

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
    
    def reset():
        self.ball.reset(0, 0, 0, 0, 0, 0)
        self.redTeam[0].reset()
        self.redTeam[1].reset()
        self.blueTeam[2].reset()
        self.redTeam[3].reset()
        
    def step(actions):
        # --> Return obs, reward, done?, infos
        
    def render():
        pass
        
class Robot(Movable):
    def __init__(self, x, y, o):
        super().__init__(x, y, o, 0, 0, 0, 30)
        print(self.x)

class Ball(Movable):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 0, 0, 10)
        print(self.x)
)
env = Field(300, 300)
env.reset()
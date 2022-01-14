from socker_render import SockerRender
from socker_constants import *

class Movable:
    def __init__(self, x, y, o, dX, dY, dO, ddX, ddY, ddO, weight):
        self.coord = (x, y, o)
        self.actualSpeed = (dX, dY, dO)
        self.acceleration = (ddX, ddY, ddO)
        self.weight = weight
        
    def move(t, dX, dY, dO, field):
        pass
    
class Field:
    def __init__(self):
        self.reset("classic")
    
    def reset(self, mode='classic'):
        if mode == 'classic':
            self.robots = [Robot(X_POS, Y_POS, 180, 'blue', 1), 
                        Robot(X_POS, -Y_POS, 180, 'blue', 2),
                        Robot(-X_POS, Y_POS, 0, 'red', 1),
                        Robot(-X_POS, -Y_POS, 0, 'red', 2)]
            self.ball = Ball(0, 0)
        # ...
        else:
            raise ValueError('Unknown "'+ mode+'" mode for reset.')
        
    def step(actions, t):
        # Execute one time step within the environment
        (dx1, dy1, do1, kick1, dx2, dy2, do2, kick2) = actions
        # update directive
        # collision here...
        
class Robot(Movable):
    def __init__(self, x, y, o, color, number):
        super().__init__(x, y, o, 0, 0, 0, 0, 0, 0, 250)
        self.color = color
        self.number = number
        
    def move(t, dX, dY, dO, field):
        (old_x, old_y, old_o) = self.coord
        (old_dX, old_dY, old_dO) = self.actualSpeed
        self.speedOrder = (dX, dY, dO)
        # Update acceleration
        # Update speed
        (dX, dY, dO) = self.actualSpeed
        # Update coord
        coordIntented = (old_x+dX*t, old_y+dY*t, old_o+dO*t)
        # Colision
        for robot in field.robots:
            pass
        self.coord = coordIntented
        (x, y, o) = self.coord
        #
        self.actualSpeed = ((x-old_x)/t, (y-old_y)/t, (o-old_o)/t)  
        self.acceleration = ((dX-old_dX)/t, (dY-old_dY)/t, (dO-old_dO)/t)
        return x, y, o
    

class Ball(Movable):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 0, 0, 0, 0, 0, 10)
        
    def move(dt, field):
        pass
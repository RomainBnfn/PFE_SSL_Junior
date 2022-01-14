from socker_render import SockerRender
from socker_constants import *
from math import dist, atan, degrees, cos, sin

class Movable:
    def __init__(self, x, y, o, dX, dY, dO, ddX, ddY, ddO, weight):
        self.coord = (x, y, o)
        self.actualSpeed = (dX, dY, dO)
        self.acceleration = (ddX, ddY, ddO)
        self.weight = weight
        
    def generic_move(self, obj_dX, obj_dY, obj_dO, weight, isRobot):
        # dX, dY and dO are the objective speed
        dt = TIME_STEP
        # We use the third newton law :
        # SUM(FORCE) = M . A
        # F + R = M . A
        # F is a part (a ratio because it can't be reach instantly) of expected acceleration
        # A = (F + R)/M
        (aX, aY, aO) = self.acceleration
        (dX, dY, dO) = self.actualSpeed
        (fX, fY, fO) = (0, 0, 0)
        # The resistance of the floor  
        (rX, rY, rO) = (-FRICTION_COEF*dX*weight,
                      -FRICTION_COEF*dY*weight,
                      -FRICTION_COEF*dO*weight)
        if isRobot:
            # To limit the increase of acceleration
            ratio = 2 * TIME_STEP/TIME_TO_REACH_SPEED
            # The force is brought by robot motors
            (fX, fY, fO) = (
                (obj_dX-dX)*ratio*ROBOT_P,
                (obj_dY-dY)*ratio*ROBOT_P,
                (obj_dO-dO)*ratio*ROBOT_P)
        # Update acceleration
        self.acceleration = (
            (fX+rX)/weight,
            (fY+rY)/weight,
            (fO+rO)/weight,
        )
        (aX, aY, aO) = self.acceleration
        # Update speed
        (old_dX, old_dY, old_dO) = self.actualSpeed
        self.actualSpeed = (old_dX+aX*dt, old_dY+aY*dt, old_dO+aO*dt)
        (dX, dY, dO) = self.actualSpeed       
        # Update coord
        (old_x, old_y, old_o) = self.coord
        self.coord = (old_x+dX*dt, old_y+dY*dt, old_o+dO*dt) 
        # Colision checking : after all mooves
        
    
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
        
    def get_new_coord(self, x1, y1, x2, y2, correctDist):
        d = dist( [x1, y1], [x2, y2])
        if d >= correctDist:
            return x1, y1, x2, y2
        #COLLISION : Thales theorem with the small distance and good one
        x, y = abs(x1-x2), abs(y1-y2)
        if x == 0:
            dx = 0
            dy = (correctDist - y)/2
        else:
            angle = atan(y/x)
            dx = (cos(angle) * correctDist - x)/2
            dy = (sin(angle) * correctDist - y)/2
            s = -1
        if(x1<x2):
            s = 1
        x1 -= dx * s
        x2 += dx * s
        s = -1
        if(y1<y2):
            s = 1
        y1 -= dy * s
        y2 += dy * s
        return x1, y1, x2, y2
    
    def step(self, actions, team):
        # Execute one time step within the environment
        (dx1, dy1, do1, kick1, dx2, dy2, do2, kick2) = actions
        
        # update directive
        if team == 'blue':
            self.robots[0].move(dx1, dy1, do1)
            self.robots[1].move(dx2, dy2, do2)
        else:
            self.robots[2].move(dx1, dy1, do1)
            self.robots[3].move(dx2, dy2, do2)
        self.ball.move()
        # collision here...
        collision = 0
        for robot in self.robots:
            for robot_bis in self.robots:
                if robot == robot_bis:
                    continue
                (x1, y1, o1) = robot.coord
                (x2, y2, o2) = robot_bis.coord
                d = dist( [x1, y1], [x2, y2])
                if d < ROBOT_SIZE:
                    x1,y1, x2,y2 = self.get_new_coord(x1, y1, x2, y2, ROBOT_SIZE)
                    robot.coord = (x1, y1, o1)
                    robot_bis.coord = (x2, y2, o2)
                    
                    (dX, dY, dO) = robot.actualSpeed
                    robot.actualSpeed = (0, 0, dO)
                    (dX, dY, dO) = robot_bis.actualSpeed
                    robot_bis.actualSpeed = (0, 0, dO)
                    if robot.color == team or robot_bis.color == team:
                        collision += 1
        # Ball collision 
        (x, y, o) = self.ball.coord
        for robot in self.robots:
            (x1, y1, o1) = robot.coord
            d = dist([x,y], [x1, y1])
            correctDist = ROBOT_SIZE/2 + BALL_SIZE/2 
            if d < correctDist:
                # If the ball reach the front part of the robot it will be pushed by it
                # So we have to determine where the ball hit the robot.
                # Lets moove on the robot base
                (_x1, _y1, _o1) = 0, 0, 0
                (_x, _y, _o) = (x-x1, y-y1, o-o1)
                angle = degrees(atan(_y/_x))
                if angle < KICKER_O1 and angle > - KICKER_O1: 
                    # FRONT
                    _dx, _dy = abs(x-x1), abs(y-y1)
                    if _dx == 0:
                        dx = 0
                        dy = (correctDist - y)/2
                    else:
                        angle = atan(_dy/_dx)
                        dx = (cos(angle) * correctDist - _dx)
                        dy = (sin(angle) * correctDist - _dy)
                    self.ball.coord = (x+dx, y+dy, o)
                    self.ball.actualSpeed = robot.actualSpeed
                else: 
                    
                    # Boing
                    (dX, dY, dO) = self.ball.actualSpeed # direction
                
                break
                    
        #return obv...
        
class Robot(Movable):
    def __init__(self, x, y, o, color, number):
        super().__init__(x, y, o, 0, 0, 0, 0, 0, 0, 250)
        self.color = color
        self.number = number
        
    def move(self, obj_dX, obj_dY, obj_dO):
        self.generic_move(obj_dX, obj_dY, obj_dO, ROBOT_WEIGTH, True)
    

class Ball(Movable):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 0, 0, 0, 0, 0, 10)
        
    def move(self):
        self.generic_move(0, 0, 0, BALL_WEIGTH, False)
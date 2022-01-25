from socker_render import SockerRender
from socker_constants import *
from math import dist, atan, degrees, cos, sin, pi
import numpy as np

def get_red_pos(x, y, o):
    return FIELD_WIDTH/2-x, FIELD_HEIGHT/2-y, -o
    
def get_red_speed(dX, dY, dO):
    return -dX, -dY, -dO
    
def get_red_acceleration(aX, aY, aO):
    return -aX, -aY, -aO
    
class Movable:
    def __init__(self, x, y, o, dX, dY, dO, aX, aY, aO, weight):
        self.coord = (x, y, o)
        self.actualSpeed = (dX, dY, dO)
        self.acceleration = (aX, aY, aO)
        self.weight = weight
    
    def obs(self, team):
        (x, y, o) = self.coord
        (dX, dY, dO) = self.actualSpeed
        (aX, aY, aO) = self.acceleration
        if team == 'red':
            (x, y, o) = get_red_pos(x, y, o)
            (dX, dY, dO) = get_red_speed(dX, dY, dO)
            (aX, aY, aO) = get_red_acceleration(aX, aY, aO)
        return [x, y, o, dX, dY, dO, aX, aY, aO]
    
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
        self.last_robot_touch_ball = None
    
    def __str__(self):
        text = "FIELD DESCRIPTION (Blue team ref) \n"
        text += "Ball: \n" + self.ball.obs()
        text += "Blue team : \n"
        text += "Robot 1: \n " + self.robots[0].obs()
        text += "Robot 2: \n " + self.robots[1].obs()
        text += "Red team : \n"
        text += "Robot 1: \n " + self.robots[2].obs()
        text += "Robot 2: \n " + self.robots[3].obs()
        
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
            dX = 0
            dY = (correctDist - y)/2
        else:
            angle = atan(y/x)
            dX = (cos(angle) * correctDist - x)/2
            dY = (sin(angle) * correctDist - y)/2
        s = -1
        if(x1<x2):
            s = 1
        x1 -= dX * s
        x2 += dX * s
        s = -1
        if(y1<y2):
            s = 1
        y1 -= dY * s
        y2 += dY * s
        return x1, y1, x2, y2
    
    def is_ball_out(self):
        (x, y, o) = self.ball.coord
        return (x < -FIELD_WIDTH/2
                or x > FIELD_WIDTH/2
                or y < -FIELD_HEIGHT/2
                or y > FIELD_HEIGHT/2)
    
    def is_finished(self):
        (x, y, o) = self.ball.coord
        return (
            (x < -FIELD_WIDTH/2 or x > FIELD_WIDTH/2)
                and y > Y_BUT-FIELD_HEIGHT/2  and y < FIELD_HEIGHT/2-Y_BUT ) # ball out of the field in one cage
            
    def obs(self, team):
        if team == 'blue':    
            return [self.ball.obs(team),
                    self.robots[0].obs(team),
                    self.robots[1].obs(team),
                    self.robots[2].obs(team),
                    self.robots[3].obs(team)]
        return [self.ball.obs(team),
                self.robots[2].obs(team),
                self.robots[3].obs(team),
                self.robots[0].obs(team),
                self.robots[1].obs(team)]
            
    def get_winner(self):
        if not self.is_finished():
            return None
        # blue team have to mark on bot size x < 0 and red on top size x > 0
        if x < 0:
            return "blue"
        return "red"
        
    def step(self, actions, team):
        # Execute one time step within the environment
        (dX1, dY1, dO1, kick1, dX2, dY2, dO2, kick2) = actions
        if team == 'red':
            dX1, dY1, dO1 = get_red_speed(dX1, dY1, dO1)
            dX2, dY2, dO2 = get_red_speed(dX2, dY2, dO2)
            
        # update directive
        if team == 'blue':
            self.robots[0].move(dX1, dY1, dO1)
            self.robots[1].move(dX2, dY2, dO2)
        else:
            self.robots[2].move(dX1, dY1, dO1)
            self.robots[3].move(dX2, dY2, dO2)
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
                self.last_robot_touch_ball = robot
                #
                (_x1, _y1, _o1) = (0, 0, 0)
                (_x, _y, _o) = (x-x1, y-y1, o-o1)
                
                angle = 90 * np.sign(_y)
                if _x != 0:
                    if _x < 0:
                        angle = degrees( pi - atan(_y *1.0/_x) )
                    else:
                        angle = degrees( atan(_y *1.0/_x) )
                angle = angle % 360
                if 360-KICKER_O1 < angle or angle < KICKER_O1:
                    # FRONT
                    _dX, _dY = abs(x-x1), abs(y-y1)
                    if _dX == 0:
                        dX = 0
                        dY = (correctDist - y)/2
                    else:
                        angle = atan(_dY/_dX)
                        dX = (cos(angle) * correctDist - _dX)
                        dY = (sin(angle) * correctDist - _dY)
                    self.ball.coord = (x+dX, y+dY, o)
                    self.ball.actualSpeed = robot.actualSpeed
                else: 
                    # Boing
                    # Angle between vect ball, robot & speed
                    # Speed --> cos(a) dx + sin(a) dy
                    #       --> sin(a) dx + cos(a) dy et dO
                    vect_ballrobot = [x1-x, y1-y]
                    (dX, dY, dO) = self.ball.actualSpeed
                    vect_speed = [dX, dY]

                    vect_ballrobot = vect_ballrobot / np.linalg.norm(vect_ballrobot)
                    vect_speed = vect_speed / np.linalg.norm(vect_speed)
                    dot_product = np.dot(vect_ballrobot, vect_speed)
                    angle = np.arccos(dot_product)
                    cosa = cos(angle)
                    sina = sin(angle)
                    self.ball.actualSpeed = (-dX, -dY, dO)
                    # TODO
                    #self.ball.actualSpeed = ( -cosa * dX + sina * dY,  - cosa * dX + sina * dY, dO)
                
                break
        # Is the ball out of field ?
        out = 0
        if self.is_ball_out():
            # RESET
            if self.last_robot_touch_ball.color == team:
                out = 1
            self.reset('classic')
        # Results
        observation = self.obs(team)
        reward = STEP_REWARD + collision * COLLISION_REWARD + out * TROUGHT_BALL_OUT_REWARD 
        done = self.is_finished()
        return observation, reward, done, self
        
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
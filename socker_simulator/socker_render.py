import pygame
from math import cos, sin, radians
from socker_constants import *

RATIO_MM_PIXEL = FIELD_HEIGHT/(SCREEN_WIDTH-BORDER)
def fromMMtoPixel_coord(x, y):  
    return -y / RATIO_MM_PIXEL + SCREEN_WIDTH/2, -x/ RATIO_MM_PIXEL + SCREEN_HEIGHT/2 
def fromMMtoPixel_dist(d):
    return d / RATIO_MM_PIXEL 

class SockerRender:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self._screen = None
        # Load field image
        self.field_image = pygame.image.load(FIELD_IMAGE_PATH)
        self.field_image = pygame.transform.rotate(self.field_image, 90)
        self.field_image = pygame.transform.scale(self.field_image, 
                                                  (SCREEN_WIDTH-BORDER,
                                                   SCREEN_HEIGHT-BORDER))
        # Load robot images 
        def loadImage(imageName, size):
            image = pygame.image.load("assets\\images\\" + imageName)
            return pygame.transform.scale(image, (size, size))
        #
        new_size = fromMMtoPixel_dist(ROBOT_MARK)
        self.colorImageDic = {
            ('red', 1) : ((255, 0, 0), loadImage(ROBOT_RED_1_MARKER_IMAGE,
                                                 new_size)),
            ('red', 2) : ((255, 0, 0), loadImage(ROBOT_RED_2_MARKER_IMAGE, 
                                                 new_size)),
            ('blue', 1) : ((0, 0, 255), loadImage(ROBOT_BLUE_1_MARKER_IMAGE,
                                                  new_size)),
            ('blue', 2) : ((0, 0, 255), loadImage(ROBOT_BLUE_2_MARKER_IMAGE,
                                                  new_size)),
        }
        
    def render(self, field):
        # Background
        self.screen.fill( FIELD_COLOR )
        self.screen.blit(self.field_image, (BORDER/2, BORDER/2))
        #Elements
        (x, y, o) = field.ball.coord
        self.display_ball(x, y)
        #
        for robot in field.robots:
            (x, y, o) = robot.coord
            color = robot.color
            number = robot.number
            self.display_robot(x, y, o, color, number)
        pygame.display.update()

    def display_ball(self, x, y):
        x_render, y_render = fromMMtoPixel_coord(x,y)
        pygame.draw.circle(self.screen, (255, 255, 0), (x_render, y_render), BALL_SIZE/2)
    
    def display_robot(self, x, y, o, color, number):
        x_render, y_render = fromMMtoPixel_coord(x,y) # coordonate
        (color, image) = self.colorImageDic.get((color, number))
        #
        image = pygame.transform.rotate(image, o)
        w, h = image.get_size()
        radius = fromMMtoPixel_dist(ROBOT_SIZE)/2
        # Robot Circle
        pygame.draw.circle(self.screen, color, (x_render, y_render), radius) 
        
        # Direction indication robot circle
        angle = radians(-o-90)
        (x_ind, y_ind) = (x_render + cos(angle) * radius * 0.6 , 
                          y_render + sin(angle) * radius * 0.6 )
        pygame.draw.circle(self.screen, (255, 255, 255), (x_ind, y_ind), 4)
        
        # Draw the kicker of robots 
        # --> TODO : Kicker movement
        angle = o-180
        o1 = radians(KICKER_O1 - angle)
        o2 = radians(KICKER_O2 - angle)
        radius_kicker = ROBOT_KICK_RADIUS/2
        (x1, y1) = (x_render + cos(o1) * radius_kicker , 
                          y_render + sin(o1) * radius_kicker )
        (x2, y2) = (x_render + cos(o2) * radius_kicker , 
                          y_render + sin(o2) * radius_kicker )
        #                
        pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 3)
        self.screen.blit(image, (x_render-w/2, y_render-h/2))
        
        
    @property
    def screen(self):
        if self._screen is None:
            self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        return self._screen


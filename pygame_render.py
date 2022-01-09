import pygame
import math
#from socker_environment import Robot, Ball

# Constants

# Mesured done on PDF
FIELD_WIDTH, FIELD_HEIGHT = 1200 , 1800 #mm
X_POS, Y_POS = 300, 440                 #mm 
BUT = 160                               #mm to 1200-160
RATIO = FIELD_HEIGHT / FIELD_WIDTH
# 
FIELD_COLOR = (68, 170, 0)
#
# ROBOT
ROBOT_MARK = 100 #mm
ROBOT_SIZE = 180 #mm



BORDER = 100
SCREEN_WIDTH = 450 + BORDER
SCREEN_HEIGHT = (SCREEN_WIDTH-BORDER) * RATIO + BORDER

BALL_SIZE = 14 # to define
ROBOT_SIZE = 30 # to define
        
RATIO_MM_PIXEL = FIELD_WIDTH/(SCREEN_WIDTH-BORDER)
def fromMMtoPixel(x, y):  
    return x / RATIO_MM_PIXEL + SCREEN_WIDTH/2, y / RATIO_MM_PIXEL + SCREEN_HEIGHT/2

def fromMMtoPixel_dist(d):
    return d * RATIO_MM_PIXEL 
class PygameRender:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self._screen = None
        # Load field image
        self.field_image = pygame.image.load("assets\\images\\croped_field.png")
        self.field_image = pygame.transform.rotate(self.field_image, 90)
        self.field_image = pygame.transform.scale(self.field_image, (SCREEN_WIDTH-BORDER, SCREEN_HEIGHT-BORDER))
        # Load robot images 
        self.blue_marker_1 = pygame.image.load("assets\\images\\blue-markers1.png")
        
    def render(self, field):
        width, height = 1500, 800 #field.width, field.height # in cm  
        self.screen.fill( FIELD_COLOR )    
        self.screen.blit(self.field_image, (BORDER/2, BORDER/2))
        #pygame.draw.rect(self.screen, (20, 180, 20), (0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT, 0.90*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT))

        self.display_ball(0,0)
        self.display_ball(X_POS, -Y_POS)
        self.display_robot(244, -20, 34, 'blue', 1)
        
        pygame.display.update()
        pygame.time.delay(3000)

    def display_ball(self, x, y):
        x_render, y_render = fromMMtoPixel(x,y)
        pygame.draw.circle(self.screen, (255, 255, 0), (x_render, y_render), BALL_SIZE/2)
    
    def display_robot(self, x, y, o, color, number):
        x_render, y_render = fromMMtoPixel(x,y)
        if color == 'red':
            c = (255, 0, 0)
        else:
            c = (0, 0, 255)
            if number == 1:
                image = self.blue_marker_1
        image = pygame.transform.scale(image, (50, 50))
        image = pygame.transform.rotate(image, o)
        pygame.draw.circle(self.screen, c, (x_render, y_render), fromMMtoPixel_dist(ROBOT_SIZE)/2)
        self.screen.blit(image, (x_render-25, y_render-25))
        
        
    @property
    def screen(self):
        if self._screen is None:
            self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        return self._screen
    
test = PygameRender()
test.render("")


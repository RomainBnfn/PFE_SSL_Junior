import pygame
import math
#from socker_environment import Robot, Ball

# Constants

#
FIELD_WIDTH = 1800  #mm
FIELD_HEIGHT = 1200 #mm
A = 300             #mm
B = 460             #mm (from left corner)
RATIO = FIELD_HEIGHT / FIELD_WIDTH 
FIELD_COLOR = (68, 170, 0)
#
BORDER = 50
SCREEN_WIDTH = 1000 + BORDER
SCREEN_HEIGHT = (SCREEN_WIDTH-BORDER) * RATIO + BORDER

class IRenderable:
    def display(self):
        pass

class Robot(IRenderable):
    def __init__(self):
        pass
    def display(self):
        pass

class Ball(IRenderable):
    def __init__(self):
        pass
    def display(self):
        pass
    
class PygameRender:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self._screen = None
        self.background = pygame.image.load("assets\\images\\croped_field.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH-BORDER, SCREEN_HEIGHT-BORDER))
    
    def render(self, field):
        width, height = 1500, 800 #field.width, field.height # in cm  
        self.screen.fill((40, 40, 40))    
        self.screen.blit(self.background, (BORDER/2, BORDER/2))
        #pygame.draw.rect(self.screen, (20, 180, 20), (0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT, 0.90*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT))

        pygame.display.update()
        pygame.time.delay(3000)

    @property
    def screen(self):
        if self._screen is None:
            self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        return self._screen
    
test = PygameRender()
test.render("")
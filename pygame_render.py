import pygame
import math
#from socker_environment import Robot, Ball

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

#
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
    
    def render(self, field):
        width, height = 1500, 800 #field.width, field.height # in cm
        self.screen.fill( (40, 40, 40) )
        
        pygame.draw.rect(self.screen, (20, 180, 20), (0.05*SCREEN_WIDTH, 0.05*SCREEN_HEIGHT, 0.90*SCREEN_WIDTH, 0.90*SCREEN_HEIGHT))

        pygame.display.update()
        pygame.time.delay(3000)

    @property
    def screen(self):
        if self._screen is None:
            self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        return self._screen
    
test = PygameRender()
test.render("")
from math import atan, degrees

# Constants
# Mesures done on PDF
FIELD_WIDTH, FIELD_HEIGHT = 1800 , 1200 #mm
X_POS, Y_POS = 440, 300                 #mm 
Y_BUT = 160                             #mm 
    #Robot
ROBOT_MARK = 100                        #mm
ROBOT_SIZE = 180                        #mm
ROBOT_KICK_SIZE = 69                    #mm
ROBOT_KICK_RADIUS = 71                  #mm
KICKER_O1 = degrees(atan(ROBOT_KICK_RADIUS/ROBOT_KICK_SIZE)) #deg
KICKER_O2 = 180 - KICKER_O1                                  #deg
    #Ball
BALL_SIZE = 14                          # to define
# Display mesures
# Screen size : the screen width correspond to the field height
RATIO = FIELD_WIDTH/FIELD_HEIGHT
BORDER = 50
SCREEN_WIDTH = 500 + BORDER
SCREEN_HEIGHT = (SCREEN_WIDTH-BORDER) * RATIO + BORDER
# Miscellaneous
FIELD_COLOR = (68, 170, 0)
MAX_SPEED = 180                         #mm.s-1
MAX_ANGULAR_SPEED = 40                  # °.s-1
MAX_BALL_SPEED = 900                    #mm.s-1

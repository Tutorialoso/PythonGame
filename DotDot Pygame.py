import random, pygame, sys
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DOT_SIZE = 8
GAP_SIZE = 40
TOLERANCE = 15

#         R    G    B
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
GREY  = (200, 200, 200)

BACKGROUND_COLOUR = GREY
DOT_COLOUR = BLACK

def main():
    global FPS_CLOCK, DISPLAYSURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DotDot')

    mouse_x = 0
    mouse_y = 0
    firstSelection = None

    DISPLAYSURF.fill(BACKGROUND_COLOUR)
    draw_grid()
    
    while True:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                pygame.display.update()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        
def draw_grid():
    for x in range(0, WINDOW_WIDTH, GAP_SIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, 480), 1)
    for y in range(0, WINDOW_HEIGHT, GAP_SIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (640, y), 1)

def pixel_to_grid(mouse_x, mouse_y):
    if ((mouse_x % GAP_SIZE) > (TOLERANCE) + 10):
        grid_x = (mouse_x / GAP_SIZE) + 1
    elif ((mouse_x % GAP_SIZE) < TOLERANCE):
        grid_x = mouse_x / GAP_SIZE
    else:
        grid_x = None
    if ((mouse_y % GAP_SIZE) > (TOLERANCE) + 10):
        grid_y = (mouse_y / GAP_SIZE) + 1
    elif ((mouse_y % GAP_SIZE) < TOLERANCE):
        grid_y = mouse_y / GAP_SIZE
    else:
        grid_y = None
    return grid_x, grid_y

if __name__ == '__main__':
    main()

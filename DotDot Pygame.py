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
PLAYER_ONE_COLOUR = BLUE
PLAYER_TWO_COLOUR = RED

PLAYER_ONE = "1"
PLAYER_TWO = "2"

def main():
    global FPS_CLOCK, DISPLAYSURF, grid_array
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DotDot')

    mouse_x = 0
    mouse_y = 0
    mouseClicked = None

    current_player = PLAYER_ONE
    last_colour = PLAYER_ONE_COLOUR

    DISPLAYSURF.fill(BACKGROUND_COLOUR)
    grid_array = init_grid()
    
    while True:
        mouseCliked = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True
                grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
                if (grid_x != None) and (grid_y != None):
                    if (grid_x > 0) and (grid_y > 0) and (grid_x < 16) and (grid_y < 12):
                        valid = is_click_valid(grid_x, grid_y)
                        if valid == True:
                            draw_dot(grid_x, grid_y, current_player)
                    if current_player == PLAYER_ONE:
                        current_player = PLAYER_TWO
                    else:
                        current_player = PLAYER_ONE
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                pygame.display.update()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        
def init_grid():
    grid_array = []
    for i in range(0, (int(WINDOW_HEIGHT / GAP_SIZE) - 1)):
        grid_sub_array = []
        for j in range(0, (int(WINDOW_WIDTH / GAP_SIZE) - 1)):
            grid_sub_array.append(True)
        grid_array.append(grid_sub_array)
    for l in range (0, len(grid_array)):
        print(grid_array[l])
    for x in range(GAP_SIZE, (WINDOW_WIDTH), GAP_SIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (x, GAP_SIZE), (x, (WINDOW_HEIGHT - GAP_SIZE)), 1)
    for y in range(GAP_SIZE, (WINDOW_HEIGHT), GAP_SIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (GAP_SIZE, y), ((WINDOW_WIDTH - GAP_SIZE), y), 1)
    return grid_array

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
    if (grid_x != None) and (grid_y != None):
        grid_x = int(grid_x)
        grid_y = int(grid_y)
        print("grid_x =", grid_x, "grid_y =", grid_y)
    return grid_x, grid_y

def grid_to_pixel(grid_x, grid_y):
    pixel_x = (grid_x * GAP_SIZE)
    pixel_y = (grid_y * GAP_SIZE)
    return pixel_x, pixel_y

def is_click_valid(grid_x, grid_y):
    array_x = grid_x - 1
    array_y = grid_y - 1
    print("array_x =", array_x, "array_y =", array_y)
    valid = grid_array[array_y][array_x]
    print(valid)
    if grid_array[array_y][array_x] == True:
        grid_array[array_y][array_x] = False
    return valid

def draw_dot(grid_x, grid_y, player):
    if player == PLAYER_ONE:
        player_colour = PLAYER_ONE_COLOUR
    else:
        player_colour = PLAYER_TWO_COLOUR
    pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
    pygame.draw.circle(DISPLAYSURF, player_colour, (pixel_x, pixel_y), 4, 0)

if __name__ == '__main__':
    main()

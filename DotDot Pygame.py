import random, pygame, sys
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DOT_SIZE = 8
GAP_SIZE = 40
TOLERANCE = 15

assert WINDOW_WIDTH % GAP_SIZE == 0, "Window width must be a multiple of gap size"
assert WINDOW_HEIGHT % GAP_SIZE == 0, "Window height must be a multiple of gap size"

#          R    G    B
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
ORANGE = (255, 140,   0)
GREY   = (200, 200, 200)

BACKGROUND_COLOUR = GREY
PLAYER_ONE_COLOUR = BLUE
PLAYER_TWO_COLOUR = RED

PLAYER_ONE = "1"
PLAYER_TWO = "2"

class Dot():
    coord = (None, None)
    player = None
    colour = None
    def __init__(self, player, grid_x, grid_y):
        array_x = grid_x - 1
        array_y = grid_y - 1
        Dot.player = player
        Dot.coord = (array_x, array_y)
        if player == PLAYER_ONE:
            Dot.colour = PLAYER_ONE_COLOUR
        else:
            Dot.colour = PLAYER_TWO_COLOUR
        connected = False
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        pygame.draw.circle(DISPLAYSURF, Dot.colour, (pixel_x, pixel_y), 4, 0)

class Land():
    total_area = 0
    player = None
    colour = None
    def __init__(self, player, dots_array):
        if player == PLAYER_ONE:
            Land.colour = PLAYER_ONE_COLOUR
        else:
            Land.colour = PLAYER_TWO_COLOUR
        for current in range (len(dots_array), 0, -1):
            first_dot_coord = dots_array[current].coord
            second_dot_coord = dots_array[current - 1].coord
            pygame.draw.line(DISPLAYSURF, Land.colour, first_dot_coord, second_dot_coord, 4)

def main():
    global FPS_CLOCK, DISPLAYSURF, grid_array
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DotDot')
    title_font_obj = pygame.font.Font('freesansbold.ttf', 22)
    title_surface_obj = title_font_obj.render('DotDot', True, ORANGE)
    title_rect_obj = title_surface_obj.get_rect()
    title_rect_obj.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / GAP_SIZE))

    mouse_x = 0
    mouse_y = 0
    mouseClicked = None

    current_player = PLAYER_ONE
    last_colour = PLAYER_ONE_COLOUR

    DISPLAYSURF.fill(BACKGROUND_COLOUR)
    DISPLAYSURF.blit(title_surface_obj, title_rect_obj)
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
                            init_dot(grid_x, grid_y, current_player)
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
            grid_sub_array.append(None)
        grid_array.append(grid_sub_array)
#    for l in range (0, len(grid_array)):
#        print(grid_array[l])
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
#        print("grid_x =", grid_x, "grid_y =", grid_y)
    return grid_x, grid_y

def grid_to_pixel(grid_x, grid_y):
    pixel_x = (grid_x * GAP_SIZE)
    pixel_y = (grid_y * GAP_SIZE)
    return pixel_x, pixel_y

def is_click_valid(grid_x, grid_y):
    array_x = grid_x - 1
    array_y = grid_y - 1
    valid = False
#    print("array_x =", array_x, "array_y =", array_y)
    if grid_array[array_y][array_x] == None:
        valid = True
    return valid

def init_dot(grid_x, grid_y, player):
    new_dot = Dot(player, grid_x, grid_y)
    array_x, array_y = new_dot.coord[0], new_dot.coord[1]
#    print("array_x =", array_x, "array_y =", array_y)
    grid_array[array_y][array_x] = new_dot

def is_connection_valid():
    valid = False

def connect_dots():
    dots_array = []

if __name__ == '__main__':
    main()

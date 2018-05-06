import random, pygame, sys
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DOT_SIZE = 4
GAP_SIZE = 40
TOLERANCE = 15

assert WINDOW_WIDTH % GAP_SIZE == 0, "Window width must be a multiple of gap size"
assert WINDOW_HEIGHT % GAP_SIZE == 0, "Window height must be a multiple of gap size"

#          R    G    B    A
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

TITLE_IMG = pygame.image.load('dotdot.jpg')
#ERROR_SOUND = pygame.mixer.Sound('beeps.wav')

class Dot():
    def __init__(self, player, grid_x, grid_y):
        array_x = grid_x - 1
        array_y = grid_y - 1
        self.player = player
        self.coord = (array_x, array_y)
        if player == PLAYER_ONE:
            self.colour = PLAYER_ONE_COLOUR
        else:
            self.colour = PLAYER_TWO_COLOUR
        connected = False
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        pygame.draw.circle(DISPLAYSURF, self.colour, (pixel_x, pixel_y), DOT_SIZE, 0)

class Land():
    def __init__(self, player, dots_array):
        self.pixel_array = []
        self.dots_obj_array = dots_array
        self.enemy_dots = 0
        if player == PLAYER_ONE:
            self.colour = PLAYER_ONE_COLOUR
        else:
            self.colour = PLAYER_TWO_COLOUR
        for current in range (0, len(dots_array)):
            dot_coord = grid_to_pixel(dots_array[current].coord[0] + 1, dots_array[current].coord[1] + 1)
            self.pixel_array.append(dot_coord)
        self.enemy_dots = dot_counter(dots_array)
        if self.enemy_dots > 0:
            pygame.draw.polygon(DISPLAYSURF, self.colour, self.pixel_array)

def main():
    global FPS_CLOCK, DISPLAYSURF, grid_array, player_one_score, player_two_score
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DotDot')

    current_player = PLAYER_ONE
    last_colour = PLAYER_ONE_COLOUR
    
    title_font_obj = pygame.font.Font('freesansbold.ttf', 34)
    title_surface_obj = title_font_obj.render('DotDot', True, ORANGE)
    title_rect_obj = title_surface_obj.get_rect()
    title_rect_obj.center = ((WINDOW_WIDTH / 2), ((WINDOW_HEIGHT / GAP_SIZE) + 5))

    mouse_x = 0
    mouse_y = 0
    mouseClicked = None
    dot_placed = False
    connecting = False
    status_changed = False
    score_changed = False

    DISPLAYSURF.fill(BACKGROUND_COLOUR)
    DISPLAYSURF.blit(title_surface_obj, title_rect_obj)
    grid_array = init_grid()
    
    connect_top_left = ((WINDOW_WIDTH / 2) + (3 * GAP_SIZE), WINDOW_HEIGHT - (GAP_SIZE - 10))
    connect_button_coord = init_button("Connect", connect_top_left)
    next_player_top_left = (GAP_SIZE, WINDOW_HEIGHT - (GAP_SIZE - 10))
    next_player_button_coord = init_button("Next Player", next_player_top_left)

    player_status = "Player " + current_player + "'s turn"
    connecting_status = "Connecting"
    game_status = player_status
    status_colour = BLACK
    update_game_status(game_status, status_colour)

    player_one_score = 0
    player_two_score = 0
    update_player_score(PLAYER_ONE, player_one_score)
    update_player_score(PLAYER_TWO, player_two_score)
    
    while True:
        mouseCliked = False
        if status_changed == True:
            update_game_status(game_status, status_colour)
            status_changed = False
        if score_changed == True:
            update_player_score(PLAYER_ONE, player_one_score)
            update_player_score(PLAYER_TWO, player_two_score)
            score_changed = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True
                grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
                if (dot_placed == False) and (connecting == False):
                    if (grid_x != None) and (grid_y != None):
                        if (grid_x > 0) and (grid_y > 0) and (grid_x < 16) and (grid_y < 12):
                            valid = is_click_valid(grid_x, grid_y)
                            if valid == True:
                                init_dot(grid_x, grid_y, current_player)
                                dot_placed = True
                elif connecting == True:
                    if (grid_x != None) and (grid_y != None):
                        if (grid_x > 0) and (grid_y > 0) and (grid_x < 16) and (grid_y < 12):
                            valid = is_click_valid(grid_x, grid_y)
                            if valid == False:
                                array_x = grid_x - 1
                                array_y = grid_y - 1
                                chosen_dot = grid_array[array_y][array_x]
                                if len(dots_array) > 0:
                                    if chosen_dot != dots_array[0]:
                                        connection_valid = is_connection_valid(dots_array[len(dots_array) - 1], chosen_dot)
                                        if connection_valid == True:
                                            dots_array.append(chosen_dot)
                                    else:
                                        connecting = False
                                        land_player = chosen_dot.player
                                        new_land = Land(land_player, dots_array)
                                        to_add_score = new_land.enemy_dots
                                        if current_player == PLAYER_ONE:
                                            player_one_score += to_add_score
                                        else:
                                            player_two_score += to_add_score
                                        score_changed = True
                                else:
                                    dots_array.append(chosen_dot)
                    elif (mouse_x >= connect_button_coord[0][0]) and (mouse_x <= connect_button_coord[1][0]) and \
                       (mouse_y >= connect_button_coord[0][1]) and (mouse_y <= connect_button_coord[1][1]):
                        connecting = False
                        game_status = player_status
                        status_colour = BLACK
                        status_changed = True
                else:
                    if (mouse_x >= next_player_button_coord[0][0]) and (mouse_x <= next_player_button_coord[1][0]) and \
                       (mouse_y >= next_player_button_coord[0][1]) and (mouse_y <= next_player_button_coord[1][1]):
                        if current_player == PLAYER_ONE:
                            current_player = PLAYER_TWO
                        else:
                            current_player = PLAYER_ONE
                        dot_placed = False
                        status_changed = True
                        player_status = "Player " + current_player + "'s turn"
                        game_status  = player_status
                        status_colour = BLACK
                    elif (mouse_x >= connect_button_coord[0][0]) and (mouse_x <= connect_button_coord[1][0]) and \
                       (mouse_y >= connect_button_coord[0][1]) and (mouse_y <= connect_button_coord[1][1]):
                        dots_array = []
                        connecting = True
                        game_status = connecting_status
                        if current_player == PLAYER_ONE:
                            status_colour = PLAYER_ONE_COLOUR
                        else:
                            status_colour = PLAYER_TWO_COLOUR
                        status_changed = True
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

def init_button(text, top_left):
    button_width = (GAP_SIZE * 4)
    button_height = 25
    bottom_right = (top_left[0] + button_width, top_left[1] + button_height)
    button_coord = (top_left, bottom_right)
    pygame.draw.rect(DISPLAYSURF, BLACK, (top_left[0], top_left[1], button_width, button_height))
    button_font_obj = pygame.font.Font('freesansbold.ttf', 18)
    button_surface_obj = button_font_obj.render(text, True, WHITE)
    button_rect_obj = button_surface_obj.get_rect()
    button_rect_obj.center = (top_left[0] + (2 * GAP_SIZE), top_left[1] + 10)
    DISPLAYSURF.blit(button_surface_obj, button_rect_obj)
    return button_coord

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

def update_game_status(status, colour):
    x_coord = (WINDOW_WIDTH / 2) - (2 * GAP_SIZE)
    y_coord = (WINDOW_HEIGHT - (GAP_SIZE - 10))
    width = (GAP_SIZE * 4)
    height = 25
    status_centre = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT - (GAP_SIZE / 2)))
    pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOUR, (x_coord, y_coord, width, height))
    turn_font_obj = pygame.font.Font('freesansbold.ttf', 18)
    turn_surface_obj = turn_font_obj.render(status, True, colour)
    turn_rect_obj = turn_surface_obj.get_rect()
    turn_rect_obj.center = status_centre
    DISPLAYSURF.blit(turn_surface_obj, turn_rect_obj)

def is_connection_valid(first_dot, second_dot):
    valid = False
    first_dot_coord = first_dot.coord
    second_dot_coord = second_dot.coord
    if ((first_dot_coord[0] - second_dot_coord[0]) == 1) or ((first_dot_coord[0] - second_dot_coord[0]) == -1) or \
       ((first_dot_coord[1] - second_dot_coord[1]) == 1) or ((first_dot_coord[1] - second_dot_coord[1]) == -1):
        valid = True
    return valid

def dot_counter(dots_array):
    dots_counted = 0
    smallest_x = WINDOW_WIDTH / GAP_SIZE
    biggest_x = 0
    for current in range (0, len(dots_array)):
        dot_x_coord = dots_array[current].coord[0]
        if dot_x_coord < smallest_x:
            smallest_x = dot_x_coord
        if dot_x_coord > biggest_x:
            biggest_x = dot_x_coord
    #print("smallest_x =", smallest_x, "biggest_x =", biggest_x)
    for x_coordinate in range ((smallest_x + 1), biggest_x):
        #print("\nx_coordinate =", x_coordinate)
        current_x_dots_array = []
        for current in range (0, len(dots_array)):
            dot_x_coord = dots_array[current].coord[0]
            if dot_x_coord == x_coordinate:
                current_x_dots_array.append(dots_array[current])
        for current_dot in range (1, len(current_x_dots_array)):
            first_dot_y = current_x_dots_array[current_dot - 1].coord[1]
            second_dot_y = current_x_dots_array[current_dot].coord[1]
            if ((first_dot_y - second_dot_y) != 1) or ((first_dot_y - second_dot_y) != -1):
                if first_dot_y > second_dot_y:
                    to_check_y = first_dot_y - 1
                    finish_y = second_dot_y
                else:
                    to_check_y = second_dot_y - 1
                    finish_y = first_dot_y
                while to_check_y > finish_y:
                    #print("to_check_y =", to_check_y, "finish_y =", finish_y)
                    if grid_array[to_check_y][x_coordinate] != None:
                        grid_array[to_check_y][x_coordinate].player
                        if grid_array[to_check_y][x_coordinate].player != current_x_dots_array[current_dot].player:
                            dots_counted += 1
                            #print("enemy dot found")
                    to_check_y -= 1
    return dots_counted

def update_player_score(player, score):
    str_score = str(score)
    if player == PLAYER_ONE:
        colour =  PLAYER_ONE_COLOUR
        x_coord = GAP_SIZE
        score_txt = "Player 1 Score: " + str_score
    else:
        colour = PLAYER_TWO_COLOUR
        x_coord = WINDOW_WIDTH - (GAP_SIZE * 6)
        score_txt = "Player 2 Score: " + str_score
    y_coord = 5
    width = GAP_SIZE * 5
    height = 25
    score_centre = ((x_coord + (width / 2)), (GAP_SIZE / 2))
    pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOUR, (x_coord, y_coord, width, height))
    score_font_obj = pygame.font.Font('freesansbold.ttf', 18)
    score_surface_obj = score_font_obj.render(score_txt, True, colour)
    score_rect_obj = score_surface_obj.get_rect()
    score_rect_obj.center = score_centre
    DISPLAYSURF.blit(score_surface_obj, score_rect_obj)

if __name__ == '__main__':
    main()

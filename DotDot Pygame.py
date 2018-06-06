import random, pygame, sys
from pygame.locals import *

global WINDOW_WIDTH, WINDOW_HEIGHT, COLOURS, NAME_COLOURS, COLOURS_NAME

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DOT_SIZE = 4
GAP_SIZE = 40
TOLERANCE = 15
BIG_BUTTON_WIDTH = (GAP_SIZE * 4)
SMALL_BUTTON_WIDTH = ((GAP_SIZE / 5) * 3)

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

NAME_COLOURS = {"RED" : RED, "BLUE" : BLUE, "GREEN" : GREEN, "YELLOW" : YELLOW, "ORANGE" : ORANGE}
COLOURS_NAME = {RED : "RED", BLUE : "BLUE", GREEN : "GREEN", YELLOW : "YELLOW", ORANGE : "ORANGE"}
COLOURS = {"background" : GREY, "1" : BLUE, "2" : RED, "status" : BLACK}

PLAYER_ONE = "1"
PLAYER_TWO = "2"

DOT_DOT = pygame.image.load('menu dotdot.png')
BACK_ARROW = pygame.image.load('back arrow.png')
#ERROR_SOUND = pygame.mixer.Sound('beeps.wav')

def init_window():
    global FPS_CLOCK, DISPLAYSURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DotDot')
    DISPLAYSURF.fill(COLOURS["background"])

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

def terminate():
    pygame.quit()
    sys.exit()
    pygame.display.update()

class Dot():
    def __init__(self, player, grid_x, grid_y):
        array_x = grid_x - 1
        array_y = grid_y - 1
        self.player = player
        self.coord = (array_x, array_y)
        self.colour = COLOURS[player]
        connected = False
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        pygame.draw.circle(DISPLAYSURF, self.colour, (pixel_x, pixel_y), DOT_SIZE, 0)

class Land():
    def __init__(self, player, dots_array):
        self.pixel_array = []
        self.dots_obj_array = dots_array
        self.enemy_dots = 0
        self.colour = COLOURS[player]
        for current in range (0, len(dots_array)):
            dot_coord = grid_to_pixel(dots_array[current].coord[0] + 1, dots_array[current].coord[1] + 1)
            self.pixel_array.append(dot_coord)
        self.enemy_dots = game.dot_counter(dots_array)
        if self.enemy_dots > 0:
            pygame.draw.polygon(DISPLAYSURF, self.colour, self.pixel_array)

class Button():
    def __init__(self, text, top_left, button_width):
        button_height = 25
        bottom_right = (top_left[0] + button_width, top_left[1] + button_height)
        self.button_coord = (top_left, bottom_right)
        pygame.draw.rect(DISPLAYSURF, BLACK, (top_left[0], top_left[1], button_width, button_height))
        button_font_obj = pygame.font.Font('freesansbold.ttf', 18)
        button_surface_obj = button_font_obj.render(text, True, WHITE)
        button_rect_obj = button_surface_obj.get_rect()
        button_rect_obj.center = (top_left[0] + (button_width / 2), top_left[1] + 10)
        DISPLAYSURF.blit(button_surface_obj, button_rect_obj)
    def is_clicked(self, mouse_x, mouse_y):
        clicked = False
        if (mouse_x >= self.button_coord[0][0]) and (mouse_x <= self.button_coord[1][0]) and \
            (mouse_y >= self.button_coord[0][1]) and (mouse_y <= self.button_coord[1][1]):
            clicked = True
        return clicked

class Game():
    def main(self):
        init_window()

        global grid_array, player_one_score, player_two_score
        
        title_font_obj = pygame.font.Font('freesansbold.ttf', 34)
        title_surface_obj = title_font_obj.render('DotDot', True, ORANGE)
        title_rect_obj = title_surface_obj.get_rect()
        title_rect_obj.center = ((WINDOW_WIDTH / 2), ((WINDOW_HEIGHT / GAP_SIZE) + 5))

        mouse_x = 0
        mouse_y = 0
        dot_placed = False
        connecting = False
        status_changed = False
        score_changed = False
        game_finished = False
        current_player = PLAYER_ONE

        DISPLAYSURF.blit(title_surface_obj, title_rect_obj)
        grid_array = self.init_grid()
        
        connect_top_left = (WINDOW_WIDTH - (5 * GAP_SIZE), WINDOW_HEIGHT - (GAP_SIZE - 10))
        connect_button = Button("Connect", connect_top_left, BIG_BUTTON_WIDTH)
        next_player_top_left = (GAP_SIZE, WINDOW_HEIGHT - (GAP_SIZE - 10))
        next_player_button = Button("Next Player", next_player_top_left, BIG_BUTTON_WIDTH)
        quit_top_left = (WINDOW_WIDTH - ((GAP_SIZE / 5) * 4), WINDOW_HEIGHT - (GAP_SIZE - 10))
        quit_button = Button("", quit_top_left, SMALL_BUTTON_WIDTH)

        DISPLAYSURF.blit(BACK_ARROW, quit_top_left)

        player_status = "Player " + current_player + "'s turn"
        connecting_status = "Connecting"
        game_status = player_status
        self.update_game_status(game_status, COLOURS["status"])

        player_one_score = 0
        player_two_score = 0
        self.update_player_score(PLAYER_ONE, player_one_score)
        self.update_player_score(PLAYER_TWO, player_two_score)
        
        while game_finished != True:
            if status_changed == True:
                self.update_game_status(game_status, COLOURS["status"])
                status_changed = False
            if score_changed == True:
                self.update_player_score(PLAYER_ONE, player_one_score)
                self.update_player_score(PLAYER_TWO, player_two_score)
                score_changed = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
                    if (dot_placed == False) and (connecting == False) and (grid_x != None) and (grid_y != None) and \
                        (grid_x > 0) and (grid_y > 0) and (grid_x < (WINDOW_WIDTH / GAP_SIZE)) and (grid_y < (WINDOW_HEIGHT / GAP_SIZE)):
                        valid = self.is_click_valid(grid_x, grid_y)
                        if valid == True:
                            self.init_dot(grid_x, grid_y, current_player)
                            dot_placed = True
                    elif connecting == True:
                        if (grid_x != None) and (grid_y != None):
                            if (grid_x > 0) and (grid_y > 0) and (grid_x < (WINDOW_WIDTH / GAP_SIZE)) and (grid_y < (WINDOW_HEIGHT / GAP_SIZE)):
                                valid = self.is_click_valid(grid_x, grid_y)
                                if valid == False:
                                    array_x = grid_x - 1
                                    array_y = grid_y - 1
                                    chosen_dot = grid_array[array_y][array_x]
                                    if len(dots_array) > 0:
                                        if chosen_dot != dots_array[0]:
                                            connection_valid = self.is_connection_valid(dots_array[len(dots_array) - 1], chosen_dot)
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
                        elif connect_button.is_clicked(mouse_x, mouse_y):
                            connecting = False
                            game_status = player_status
                            status_colour = COLOURS["status"]
                            status_changed = True
                    else:
                        if next_player_button.is_clicked(mouse_x, mouse_y):
                            if current_player == PLAYER_ONE:
                                current_player = PLAYER_TWO
                            else:
                                current_player = PLAYER_ONE
                            dot_placed = False
                            status_changed = True
                            player_status = "Player " + current_player + "'s turn"
                            game_status  = player_status
                            status_colour = COLOURS["status"]
                        elif connect_button.is_clicked(mouse_x, mouse_y):
                            dots_array = []
                            connecting = True
                            game_status = connecting_status
                            status_colour = COLOURS[current_player]
                            status_changed = True
                        elif quit_button.is_clicked(mouse_x, mouse_y):
                            game_finished = True
                elif event.type == QUIT:
                    terminate()
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
            
    def init_grid(self):
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

    def is_click_valid(self, grid_x, grid_y):
        array_x = grid_x - 1
        array_y = grid_y - 1
        valid = False
    #    print("array_x =", array_x, "array_y =", array_y)
        if grid_array[array_y][array_x] == None:
            valid = True
        return valid

    def init_dot(self, grid_x, grid_y, player):
        new_dot = Dot(player, grid_x, grid_y)
        array_x, array_y = new_dot.coord[0], new_dot.coord[1]
    #    print("array_x =", array_x, "array_y =", array_y)
        grid_array[array_y][array_x] = new_dot

    def update_game_status(self, status, colour):
        x_coord = (WINDOW_WIDTH / 2) - (2 * GAP_SIZE)
        y_coord = (WINDOW_HEIGHT - (GAP_SIZE - 10))
        width = (GAP_SIZE * 4)
        height = 25
        status_centre = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT - (GAP_SIZE / 2)))
        pygame.draw.rect(DISPLAYSURF, COLOURS["background"], (x_coord, y_coord, width, height))
        turn_font_obj = pygame.font.Font('freesansbold.ttf', 18)
        turn_surface_obj = turn_font_obj.render(status, True, colour)
        turn_rect_obj = turn_surface_obj.get_rect()
        turn_rect_obj.center = status_centre
        DISPLAYSURF.blit(turn_surface_obj, turn_rect_obj)

    def is_connection_valid(self, first_dot, second_dot):
        valid = False
        first_dot_coord = first_dot.coord
        second_dot_coord = second_dot.coord
        if ((first_dot_coord[0] - second_dot_coord[0]) == 1) or ((first_dot_coord[0] - second_dot_coord[0]) == -1) or \
           ((first_dot_coord[1] - second_dot_coord[1]) == 1) or ((first_dot_coord[1] - second_dot_coord[1]) == -1):
            valid = True
        return valid

    def dot_counter(self, dots_array):
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

    def update_player_score(self, player, score):
        str_score = str(score)
        score_txt = "Player " + player + " Score: " + str_score
        colour =  COLOURS[player]
        if player == PLAYER_ONE:
            x_coord = GAP_SIZE
        else:
            x_coord = WINDOW_WIDTH - (GAP_SIZE * 6)
        y_coord = 5
        width = GAP_SIZE * 5
        height = 25
        score_centre = ((x_coord + (width / 2)), (GAP_SIZE / 2))
        pygame.draw.rect(DISPLAYSURF, COLOURS["background"], (x_coord, y_coord, width, height))
        score_font_obj = pygame.font.Font('freesansbold.ttf', 18)
        score_surface_obj = score_font_obj.render(score_txt, True, colour)
        score_rect_obj = score_surface_obj.get_rect()
        score_rect_obj.center = score_centre
        DISPLAYSURF.blit(score_surface_obj, score_rect_obj)

class MainMenu():
    def main(self):
        init_window()

        DISPLAYSURF.blit(DOT_DOT, ((WINDOW_WIDTH / 2) - (484 / 2), 0))
        
        settings_top_left = (WINDOW_WIDTH - (5 * GAP_SIZE), WINDOW_HEIGHT - (GAP_SIZE - 10))
        settings_button = Button("Settings", settings_top_left, BIG_BUTTON_WIDTH)
        start_game_top_left = (GAP_SIZE, WINDOW_HEIGHT - (GAP_SIZE - 10))
        start_game_button = Button("Start Game", start_game_top_left, BIG_BUTTON_WIDTH)

        mouse_x = 0
        mouse_y = 0
        button_clicked = False
        button_type = None

        while button_clicked != True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if start_game_button.is_clicked(mouse_x, mouse_y):
                        button_clicked = True
                        button_type = "Game"
                    elif settings_button.is_clicked(mouse_x, mouse_y):
                        button_clicked = True
                        button_type = "Settings"
                elif event.type == QUIT:
                    terminate()
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

        return button_type

class Settings():
    def main(self):
        init_window()

        back_top_left = (WINDOW_WIDTH - (5 * GAP_SIZE), WINDOW_HEIGHT - (GAP_SIZE - 10))
        back_button = Button("Back to menu", back_top_left, BIG_BUTTON_WIDTH)
        
        previous_res_top_left = ((GAP_SIZE / 5), (GAP_SIZE / 4) + GAP_SIZE)
        previous_res_button = Button("<", previous_res_top_left, SMALL_BUTTON_WIDTH)
        next_res_top_left = ((GAP_SIZE * 4) + (GAP_SIZE / 2), (GAP_SIZE / 4) + GAP_SIZE)
        next_res_button = Button(">", next_res_top_left, SMALL_BUTTON_WIDTH)
        
        previous_col_one_top_left = ((GAP_SIZE / 5), (GAP_SIZE / 4) + (GAP_SIZE * 3.5))
        previous_col_one_button = Button("<", previous_col_one_top_left, SMALL_BUTTON_WIDTH)
        next_col_one_top_left = ((GAP_SIZE * 4) + (GAP_SIZE / 2), (GAP_SIZE / 4) + (GAP_SIZE * 3.5))
        next_col_one_button = Button(">", next_col_one_top_left, SMALL_BUTTON_WIDTH)
        previous_col_two_top_left = ((GAP_SIZE / 5), (GAP_SIZE / 4) + (GAP_SIZE * 6))
        previous_col_two_button = Button("<", previous_col_two_top_left, SMALL_BUTTON_WIDTH)
        next_col_two_top_left = ((GAP_SIZE * 4) + (GAP_SIZE / 2), (GAP_SIZE / 4) + (GAP_SIZE * 6))
        next_col_two_button = Button(">", next_col_two_top_left, SMALL_BUTTON_WIDTH)
        
        save_top_left = (GAP_SIZE, WINDOW_HEIGHT - (GAP_SIZE - 10))
        save_button = Button("Save and Apply", save_top_left, BIG_BUTTON_WIDTH)

        header_font_obj = pygame.font.Font('freesansbold.ttf', 18)
        to_display_res = (str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        to_display_colour_one = COLOURS_NAME[COLOURS["1"]]
        to_display_colour_two = COLOURS_NAME[COLOURS["2"]]
        to_display_colours = [to_display_colour_one, to_display_colour_two]
        new_width, new_height, new_player_one_colour, new_player_two_colour = WINDOW_WIDTH, WINDOW_HEIGHT, COLOURS["1"], COLOURS["2"]

        resolution_header_centre = (((GAP_SIZE * 7) / 2) - ((GAP_SIZE / 4) * 3), (GAP_SIZE / 2))
        resolution_header_surface_obj = header_font_obj.render("Resolution", True, BLACK)
        resolution_header_rect_obj = resolution_header_surface_obj.get_rect()
        resolution_header_rect_obj.center = resolution_header_centre
        
        resolution_centre = (((GAP_SIZE * 7) / 2) - ((GAP_SIZE / 4) * 3), (GAP_SIZE * 1.5))
        resolution_surface_obj = header_font_obj.render(to_display_res, True, BLACK)
        resolution_rect_obj = resolution_surface_obj.get_rect()
        resolution_rect_obj.center = resolution_centre

        player_one_centre = (((GAP_SIZE * 7) / 2) - ((GAP_SIZE / 4) * 3), (GAP_SIZE * 3))
        player_one_surface_obj = header_font_obj.render("Player 1 Colour", True, BLACK)
        player_one_rect_obj = player_one_surface_obj.get_rect()
        player_one_rect_obj.center = player_one_centre

        player_two_centre = (((GAP_SIZE * 7) / 2) - ((GAP_SIZE / 4) * 3), (GAP_SIZE * 5.5))
        player_two_surface_obj = header_font_obj.render("Player 2 Colour", True, BLACK)
        player_two_rect_obj = player_two_surface_obj.get_rect()
        player_two_rect_obj.center = player_two_centre

        self.update_player_colour_selector(to_display_colours[0], PLAYER_ONE)
        self.update_player_colour_selector(to_display_colours[1], PLAYER_TWO)
        DISPLAYSURF.blit(resolution_header_surface_obj, resolution_header_rect_obj)
        DISPLAYSURF.blit(resolution_surface_obj, resolution_rect_obj)
        DISPLAYSURF.blit(player_one_surface_obj, player_one_rect_obj)
        DISPLAYSURF.blit(player_two_surface_obj, player_two_rect_obj)

        mouse_x = 0
        mouse_y = 0
        button_type = None
        resolutions = ["640x480", "800x600", "1280x720"]
        colours = []
        for key in NAME_COLOURS:
            colours.append(key)

        while button_type != "Back":
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if back_button.is_clicked(mouse_x, mouse_y):
                        button_type = "Back"
                    elif previous_res_button.is_clicked(mouse_x, mouse_y):
                        for y in range(0, len(resolutions)):
                            if (to_display_res == resolutions[y]) and (y != 0):
                                to_display_res = resolutions[y - 1]
                                self.update_display_resolution_selector(to_display_res)
                    elif next_res_button.is_clicked(mouse_x, mouse_y):
                        y = 0
                        changed = False
                        while (y < len(resolutions)) and (changed == False):
                            if (to_display_res == resolutions[y]) and (y != (len(resolutions) - 1)):
                                to_display_res = resolutions[y + 1]
                                self.update_display_resolution_selector(to_display_res)
                                changed = True
                            y += 1
                    elif previous_col_one_button.is_clicked(mouse_x, mouse_y):
                        for y in range(0, len(colours)):
                            if (to_display_colours[0] == colours[y]) and (y != 0):
                                if colours[y - 1] != to_display_colours[1]:
                                    to_display_colours[0] = colours[y - 1]
                                    self.update_player_colour_selector(to_display_colours[0], PLAYER_ONE)
                                elif (colours[y - 1] != to_display_colours[1]) and ((y - 1) != 0):
                                    to_display_colours[0] = colours[y - 2]
                                    self.update_player_colour_selector(to_display_colours[0], PLAYER_ONE)
                    elif next_col_one_button.is_clicked(mouse_x, mouse_y):
                        y = 0
                        changed = False
                        while (y < len(colours)) and (changed == False):
                            if (to_display_colours[0] == colours[y]) and (y != (len(colours) - 1)):
                                if colours[y + 1] != to_display_colours[1]:
                                    to_display_colours[0] = colours[y + 1]
                                    self.update_player_colour_selector(to_display_colours[0], PLAYER_ONE)
                                    changed = True
                                elif (colours[y + 1] == to_display_colours[1]) and ((y + 1) != (len(colours) - 1)):
                                    to_display_colours[1] = colours[y + 2]
                                    self.update_player_colour_selector(to_display_colours[1], PLAYER_ONE)
                                    changed = True
                            y += 1
                    elif previous_col_two_button.is_clicked(mouse_x, mouse_y):
                        for y in range(0, len(colours)):
                            if (to_display_colours[1] == colours[y]) and (y != 0):
                                if colours[y - 1] != to_display_colours[0]:
                                    to_display_colours[1] = colours[y - 1]
                                    self.update_player_colour_selector(to_display_colours[1], PLAYER_TWO)
                                elif (colours[y - 1] != to_display_colours[0]) and ((y - 1) != 0):
                                    to_display_colours[1] = colours[y - 2]
                                    self.update_player_colour_selector(to_display_colours[0], PLAYER_ONE)
                    elif next_col_two_button.is_clicked(mouse_x, mouse_y):
                        y = 0
                        changed = False
                        while (y < len(colours)) and (changed == False):
                            if (to_display_colours[1] == colours[y]) and (y != (len(colours) - 1)):
                                if colours[y + 1] != to_display_colours[0]:
                                    to_display_colours[1] = colours[y + 1]
                                    self.update_player_colour_selector(to_display_colours[1], PLAYER_TWO)
                                    changed = True
                                elif (colours[y + 1] == to_display_colours[0]) and ((y + 1) != (len(colours) - 1)):
                                    to_display_colours[1] = colours[y + 2]
                                    self.update_player_colour_selector(to_display_colours[1], PLAYER_TWO)
                                    changed = True
                            y += 1
                    elif save_button.is_clicked(mouse_x, mouse_y):
                        self.save_settings(to_display_res, to_display_colours)
                        new_width, new_height, new_player_one_colour, new_player_two_colour = self.load_settings()
                        button_type = "Back"
                elif event.type == QUIT:
                    terminate()
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

        return new_width, new_height, new_player_one_colour, new_player_two_colour

    def load_settings(self):
        message = "Settings Loaded"
        values_array = []
        try:
            settings_file = open("settings.txt")
            settings_string_array = settings_file.readlines()
            settings_file.close()
            for setting in range(0, len(settings_string_array)):
                setting_string = settings_string_array[setting].split("=")
                value = setting_string[1].strip()
                try:
                    value_int = int(value)
                    values_array.append(value_int)
                except ValueError:
                    values_array.append(value)
            width = values_array[0]
            height = values_array[1]
            player_one_colour = NAME_COLOURS[values_array[2]]
            player_two_colour = NAME_COLOURS[values_array[3]]
        except FileNotFoundError:
            message = "File Not Found"
        return width, height, player_one_colour, player_two_colour

    def save_settings(self, resolution, colours):
        settings_file = open("settings.txt", "w")
        resolution_array = resolution.split("x")
        width = "WINDOW_WIDTH=" + resolution_array[0] + "\n"
        height = "WINDOW_HEIGHT=" + resolution_array[1] + "\n"
        player_one_colour = "PLAYER_ONE=" + colours[0] + "\n"
        player_two_colour = "PLAYER_TWO=" + colours[1] + "\n"
        to_write_array = [width, height, player_one_colour, player_two_colour]
        for element in to_write_array:
            settings_file.write(element)
        settings_file.close()

    def update_display_resolution_selector(self, to_display_res):
        resolution_font_obj = pygame.font.Font('freesansbold.ttf', 18)
        x_coord = GAP_SIZE
        y_coord = (GAP_SIZE / 4) + GAP_SIZE
        width = GAP_SIZE * 3
        height = GAP_SIZE
        pygame.draw.rect(DISPLAYSURF, COLOURS["background"], (x_coord, y_coord, width, height))
        resolution_centre = (((GAP_SIZE * 7) / 2) - ((GAP_SIZE / 4) * 3), (GAP_SIZE * 1.5))
        resolution_surface_obj = resolution_font_obj.render(to_display_res, True, BLACK)
        resolution_rect_obj = resolution_surface_obj.get_rect()
        resolution_rect_obj.center = resolution_centre
        DISPLAYSURF.blit(resolution_surface_obj, resolution_rect_obj)

    def update_player_colour_selector(self, to_display_colour, player):
        x_coord = GAP_SIZE + (GAP_SIZE / 8)
        if player == "1":
            y_coord = (GAP_SIZE / 4) + (GAP_SIZE * 3.5)
        else:
            y_coord = (GAP_SIZE / 4) + (GAP_SIZE * 6)
        width = GAP_SIZE * 3
        height = (GAP_SIZE / 5) * 3
        pygame.draw.rect(DISPLAYSURF, NAME_COLOURS[to_display_colour], (x_coord, y_coord, width, height))

game = Game()
settings = Settings()
menu = MainMenu()
end = False
options = {"Game" : game.main, "Settings" : settings.main}
WINDOW_WIDTH, WINDOW_HEIGHT, COLOURS["1"], COLOURS["2"] = settings.load_settings()

while end != True:
    go_to = menu.main()
    if go_to == "Game":
        options[go_to]()
    elif go_to == "Settings":
        WINDOW_WIDTH, WINDOW_HEIGHT, COLOURS["1"], COLOURS["2"] = options[go_to]()
    elif go_to == "Quit":
        end = True

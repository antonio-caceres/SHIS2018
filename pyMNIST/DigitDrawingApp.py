"""
An extremely simple image editor for 28x28 black-and-white images, created by Mr. V for Antonio.
Much of the code used in this project is from https://inventwithpython.com/pygameHelloWorld.py
Install pygame using the Terminal:
    sudo pip install pygame
Install pip using the Terminal:
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
"""
import pygame
import os
import random
from pygame.locals import *  # for QUIT and other state/type info
import numpy as np

class DigitDrawing:
    # Drawing Area Constants
    HEIGHT, WIDTH = 28, 28
    X_SIZE, Y_SIZE = 10, 10
    X_OFFSET, Y_OFFSET = 20, 20
    MAX_VALUES = 30  # will determine how quickly the brush paints black
    BRUSH = [" XX ",
             "XXXX",
             " XX "]

    # Color Constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Instance Variables
    window_surface = None
    values = None
    clicking = False
    raster_must_redraw = True
    shift_is_pressed = False
    app_is_running = False

    def __init__(self):
        self.initialize_application()

    def init_values(self):
        self.width = 28
        self.height = 28
        self.values = np.array([[0.0]]*self.width*self.height)

    def get(self, x, y = None):
        return self.values[y*self.width+x][0]

    def set(self, x, y, value = None):
        self.values[y*self.width+x][0] = value

    def initialize_application(self):
        """
        Initializes the pygame window, text, and drawing space.
        """
        # Create drawing space by initializing a zero array of values.
        #self.values = [[0 for i in range(DigitDrawing.WIDTH)] for j in range(DigitDrawing.HEIGHT)]
        self.init_values()

        pygame.init()
        self.window_surface = pygame.display.set_mode((500, 400), 0, 24)
        pygame.display.set_caption("SHIS Digit Drawing")

        font_size = 48
        basic_font = pygame.font.SysFont(None, font_size)
        text = basic_font.render('esc to clear - enter to save', True, DigitDrawing.BLACK, DigitDrawing.WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = self.window_surface.get_rect().centerx
        text_rect.y = self.window_surface.get_rect().height - font_size

        self.window_surface.fill(DigitDrawing.WHITE)
        self.window_surface.blit(text, text_rect)

        # test code
        """
        DigitDrawing.brush_to_values_raster([
            "                            ",
            "      ######                ",
            "     ########               ",
            "    ###   ####              ",
            "   ##       ###             ",
            "   #         ###            ",
            " ##           ##            ",
            "              ##            ",
            "              #             ",
            "              #             ",
            "              #             ",
            "             #              ",
            "            #               ",
            "           #                ",
            "          #                 ",
            "         #                  ",
            "         #                  ",
            "        ##                  ",
            "        ##                  ",
            "       ###                  ",
            "       ##                   ",
            "      ####              #   ",
            "      #####             ##  ",
            "     ###############   ###  ",
            "     ####################   ",
            "                  ######    ",
            "                            ",
        ],self.values, self.width, self.height, 0.1)
        positions = DigitDrawing.range_of_shiftable_positions(self.values, self.width, self.height)
        for delta in positions:
            print(delta)
            DigitDrawing.shift_all_values(self.values, self.width, self.height, delta)
            DigitDrawing.terminal_print(self.values, self.width, self.height)
        """

        pygame.display.update()
        self.game_loop()

    def game_loop(self):
        """
        Runs the game loop and processes inputs using decomposition.
        """
        app_is_running = True
        while app_is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    app_is_running = False
                elif event.type == KEYDOWN:
                    self.process_keyboard_input(event)
                elif event.type == KEYUP:
                    if event.key == 304:
                        self.shift_is_pressed = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.clicking = (1, -1)[event.button == 3]
                    raster_pos = DigitDrawing.get_raster_position(event.pos)
                    self.add_brush_to_values_at(raster_pos)
                    self.clamp_values()
                    self.raster_must_redraw = True
                elif event.type == MOUSEBUTTONUP:
                    self.clicking = False
                elif event.type == MOUSEMOTION:
                    if self.clicking:
                        raster_pos = DigitDrawing.get_raster_position(event.pos)
                        self.add_brush_to_values_at(raster_pos)
                        self.clamp_values()
                        self.raster_must_redraw = True
            if self.raster_must_redraw:
                self.draw_raster()
                pygame.display.update()  # draw the window onto the screen
                raster_must_redraw = False
        pygame.quit()

    def process_keyboard_input(self, event):
        self.raster_must_redraw = True
        # Save the currently drawn image on space or return.
        if event.key == 13 or event.key == 32:
            self.create_and_save_image("Image ")
        # Reset the drawing space on escape or backspace.
        elif event.key == 27 or event.key == 8:
            self.init_values()
        elif event.key == 304:
            self.shift_is_pressed = True
        # Deals with the 'w', 'a', 's', 'd', and 'r' inputs.
        elif 32 <= event.key < 128 and chr(event.key) in "wasdr":
            x_range, y_range = DigitDrawing.calculate_shift_ranges(self.values, self.width, self.height)
            shift_delta = (0,0)
            if event.key == ord('w') and (self.shift_is_pressed or y_range[0] < 0):
                shift_delta = (0, -1)
            elif event.key == ord('a') and (self.shift_is_pressed or x_range[0] < 0):
                shift_delta = (-1, 0)
            elif event.key == ord('s') and (self.shift_is_pressed or y_range[1] > 0):
                shift_delta = (0, +1)
            elif event.key == ord('d') and (self.shift_is_pressed or x_range[1] > 0):
                shift_delta = (+1, 0)
            elif event.key == ord('r'):
                rnd_x = random.randint(x_range[0], x_range[1])
                rnd_y = random.randint(y_range[0], y_range[1])
                shift_delta = (rnd_x,rnd_y)
            if shift_delta != (0,0):
                self.shift_all_values(self.values, self.width, self.height, shift_delta)

    def draw_raster(self):
        height, width = self.height, self.width
        rect_border = 1
        pygame.draw.rect(self.window_surface, DigitDrawing.BLACK,
                         (DigitDrawing.X_OFFSET - rect_border,
                          DigitDrawing.Y_OFFSET - rect_border,
                          width * DigitDrawing.X_SIZE + rect_border * 2,
                          height * DigitDrawing.Y_SIZE + rect_border * 2),
                         rect_border)
        for r in range(height):
            for c in range(width):
                x = DigitDrawing.X_OFFSET + DigitDrawing.X_SIZE * c
                y = DigitDrawing.Y_OFFSET + DigitDrawing.Y_SIZE * r
                color = DigitDrawing.get_color_from_value(self.get(c,r))
                pygame.draw.rect(self.window_surface, color,
                                 (x, y, DigitDrawing.X_SIZE, DigitDrawing.Y_SIZE))

    def create_and_save_image(self, base_name):
        """
        Creates a bitmap of the currently drawn image and saves it to a file in the data/user directory.
        :param base_name: the beginning of the file name for the image to be saved.
        """
        image_name = DigitDrawing.get_complete_title(base_name)
        height, width = self.height, self.width
        surf = pygame.Surface((width, height))
        surf.fill(DigitDrawing.WHITE)
        pix_array = pygame.PixelArray(surf)
        for r in range(height):
            for c in range(width):
                # note: pygame pixel maps are x/y not row/col
                pix_array[c][r] = DigitDrawing.get_color_from_value(self.get(c,r))
        del pix_array
        pygame.image.save(surf, image_name)

    def add_to_values_at(self, pos):
        ink = self.clicking
        ink *= 1.0/self.MAX_VALUES
        DigitDrawing.add_to_values_at_static(pos, ink, self.get, self.set,self.width, self.height)

    def add_brush_to_values_at(self, xy_pos):
        for r in range(len(self.BRUSH)):
            for c in range(len(self.BRUSH[r])):
                if self.BRUSH[r][c] != ' ':
                    self.add_to_values_at((xy_pos[0] + c, xy_pos[1] + r))

    def clamp_values(self):

        for i in range(len(self.values)):
            self.values[i][0] = np.clip(self.values[i][0],0,1)

    @staticmethod
    def terminal_print(values, width, height):
        import sys
        for row in range(height):
            for col in range(width):
                v = ('.','#')[values[row*28+col][0]!=0]
                sys.stdout.write(v)
            sys.stdout.write('\n')

    @staticmethod
    def add_to_values_at_static(pos, ink, get, set, width, height):
        """
        'draws' pixels at the target location using set, and possibly in surrounding pixels
        :param pos: where
        :param ink: how much to add, as a fraction of 1. should be less than 1, because it is multiplied by up to 5. can be negative!
        :param get: callback. how to get a value: get(x, y)
        :param set: callback. how to set a value: set(x, y, value)
        :param width: boundary limit for width (0 is assumed as min)
        :param height: boundary limit for height (0 is assumed as min)
        """
        if 0 <= pos[0] < width and 0 <= pos[1] < height:
            r, c = int(pos[1]), int(pos[0])
            up, dn, lf, rt = pos[1] - r <= .5, pos[1] - r >= .5, pos[0] - c <= .5, pos[0] - c >= .5
            set(c,r, get(c,r)+ink * 5)
            if r > 0 and up:
                set(c,r-1, get(c,r-1) + ink * 2)
                if c > 0 and lf: set(c-1,r-1, get(c-1,r-1) + ink * 1)
                if c > width - 1 and rt: set(c+1,r-1, get(c+1,r-1) + ink * 1)
            if c > 0 and lf:
                set(c-1,r,get(c-1,r) + ink * 2)
            if r < height - 1 and dn:
                set(c,r+1, get(c,r+1) + ink * 2)
                if c > 0 and lf: set(c-1,r+1, get(c-1,r+1) + ink * 1)
                if c > width - 1 and rt: set(c+1,r+1, get(c+1,r+1) + ink * 1)
            if c > width - 1 and rt:
                set(c+1,r, get(c+1,r)+ ink * 2)

    @staticmethod
    def brush_to_values_raster(brush, values, width, height, intensity):
        """
        :param values: if None, will create a new values raster that is width x height sized
        :return: values
        """
        index = 0
        if type(values) != np.ndarray and values == None:
            values = np.array([[0.0]]*width*height)
        def get(x,y):
            return values[y*width+x][0]
        def set(x,y,value):
            values[y*width+x][0] = value
        for r in range(len(brush)):
            for c in range(len(brush[r])):
                if brush[r][c] != ' ':
                    DigitDrawing.add_to_values_at_static((c+0.5,r+0.5), intensity, get, set, width, height)
        return values


    @staticmethod
    def range_of_shiftable_positions(values, width, height):
        bounds = DigitDrawing.bound_box_of_values(values, width, height)
        result = []
        dx, dy = bounds[1][0] - bounds[0][0], bounds[1][1] - bounds[0][1]
        result.append((-bounds[0][0], -bounds[0][1]))
        for r in range(height-dy):
            if dx > 0:
                for c in range(width-dx-1):
                    result.append((+1,0))
            if r < height-dy-1:
                result.append((-(width-dx-1),+1))
        return result

    @staticmethod
    def shift_all_values(values, width, height, xy_delta):
        # create a 2D array version of the 1D array
        twoDcopy = []
        for r in range(height):
            twoDcopy.append([])
            for c in range(width):
                twoDcopy[r].append(values[r*width+c][0])
        for r in range(len(twoDcopy)):
            DigitDrawing.shift_list(twoDcopy[r], xy_delta[0], 0)
        DigitDrawing.shift_list(twoDcopy, xy_delta[1], [0] * len(twoDcopy[0]))
        # copy it back now
        for r in range(height):
            for c in range(width):
                values[r*width+c][0] = twoDcopy[r][c]


    @staticmethod
    def calculate_shift_ranges(values, width, height):
        """
        Calculates the maximum range by which to shift the image to reach the boundary
        :return: ((max_left, max_right),(max_up, max_down))
        """
        bounds = DigitDrawing.bound_box_of_values(values, width, height)
        x_range = (-bounds[0][0], width - bounds[1][0] - 1)
        y_range = (-bounds[0][1], height - bounds[1][1] - 1)
        return x_range, y_range

    @staticmethod
    def bound_box_of_values(values, width, height):
        """
        Calculates the box of values surrounding the image in question.
        :return: ((min_x,min_y),(max_x,max_y))
        """
        minimum, maximum = [width, height], [-1, -1]
        for r in range(height):
            for c in range(width):
                v = values[r*width+c][0]
                if v != 0:
                    if c < minimum[0]: minimum[0] = c
                    if r < minimum[1]: minimum[1] = r
                    if c > maximum[0]: maximum[0] = c
                    if r > maximum[1]: maximum[1] = r
        return (minimum[0], minimum[1]), (maximum[0], maximum[1])

    @staticmethod
    def shift_list(values, delta, fill_extra_with=None):
        import copy
        if delta < 0:  # go backwards, losing values at the front
            for i in range(0, len(values) + delta):
                values[i] = values[i - delta]
            if fill_extra_with is not None:
                for i in range(len(values) + delta, len(values)):
                    values[i] = copy.copy(fill_extra_with)
        if delta > 0:
            for i in range(len(values) - 1, -1, -1):
                values[i] = values[i - delta]
            if fill_extra_with is not None:
                for i in range(delta - 1, -1, -1):
                    values[i] = copy.copy(fill_extra_with)

    @staticmethod
    def get_complete_title(base_title):
        title = base_title
        counter = 0
        unique = False
        while not unique:
            title = base_title + str(counter)
            unique = True
            for item in os.listdir(os.getcwd() + "/data/user"):
                if item == title + ".bmp":
                    unique = False
            counter += 1
        complete_title = "data/user/" + title + ".bmp"
        return complete_title

    @staticmethod
    def get_raster_position(mouse):
        x_raster_pos = float(mouse[0] - DigitDrawing.X_OFFSET) / DigitDrawing.X_SIZE
        y_raster_pos = float(mouse[1] - DigitDrawing.Y_OFFSET) / DigitDrawing.Y_SIZE
        return x_raster_pos, y_raster_pos

    @staticmethod
    def get_color_from_value(v):
        """
        Returns a shade of grey in RGB from a single value between 0 and MAX_VALUES.
        The higher the value, the darker the shade, based off of the proportion of the value versus MAX_VALUES.
        :param v: a value between 0 and MAX_VALUES.
        :return: a tuple of three of the same integers between 0 and 255, representing a shade of grey.
        """
        if v <= 0: return DigitDrawing.WHITE
        if v > 1: v = 1
        v = 255 - int(255 * v)
        return v, v, v

    @staticmethod
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


if __name__ == "__main__":
    drawing_app = DigitDrawing()

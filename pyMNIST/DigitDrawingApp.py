"""
An image editor for 28x28 gray-scale images, created by Mr. V for Antonio.
Much of the code used in this project is from https://inventwithpython.com/pygameHelloWorld.py
Install pygame using the Terminal with: sudo pip install pygame
Install pip using the Terminal with: curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
"""
import random
import numpy as np
import pygame
from pygame.locals import *  # for QUIT and other state/type info
import FileProcessor

# Drawing Area Constants
WIDTH, HEIGHT = 28, 28  # dimensions for the drawing space in pixels
X_SIZE, Y_SIZE = 10, 10  # used for raster position
X_OFFSET, Y_OFFSET = 20, 20  # used for raster position
MAX_VALUES = 30  # determines how 'quickly' the brush paints black
BRUSH = [" XX ",
         "XXXX",
         " XX "]

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global Variables
values = np.array([[0.0]] * WIDTH*HEIGHT)
clicking = False
raster_must_redraw = True
shift_is_pressed = False
app_is_running = False


# Changing the Value Array
def get_val(x, y=None):
    """
    :param x: if y is None, the index of the position in the value array;
        else, the column (x) of the pixel from the drawing
    :param y: the row (y) of the pixel from the drawing
    :return: the value of that pixel (drawing) or that index (array)
    """
    global values
    return values[y * WIDTH + x][0]


def set_val(x, y=None, value=0):
    """
    :param x: if y is None, the index of the position in the value array;
        else, the column (x) of the pixel from the drawing
    :param y: the row (y) of the pixel from the drawing
    :param value: the value to set that pixel (drawing) or index (array) to.
    """
    global values
    values[y * WIDTH + x][0] = value


def clamp_values():
    global values
    for i in range(len(values)):
        values[i][0] = np.clip(values[i][0], 0, 1)  # restricts the values to floats between 0 and 1.


# Handling User Inputs
def process_input(user_event):
    """
    Processes a user input from pygame.
    :param user_event: pygame event
    """
    global clicking, raster_must_redraw, shift_is_pressed, app_is_running
    if user_event.type == QUIT:
        app_is_running = False
    elif user_event.type == KEYDOWN:
        process_keyboard_input(user_event)
    elif user_event.type == KEYUP:
        if user_event.key == 304:
            shift_is_pressed = False
    elif user_event.type == MOUSEBUTTONDOWN:
        clicking = (1, -1)[user_event.button == 3]
        raster_pos = get_raster_position(user_event.pos)
        add_brush_to_values_at(raster_pos)
        clamp_values()
        raster_must_redraw = True
    elif user_event.type == MOUSEBUTTONUP:
        clicking = False
    elif user_event.type == MOUSEMOTION:
        if clicking:
            raster_pos = get_raster_position(user_event.pos)
            add_brush_to_values_at(raster_pos)
            clamp_values()
            raster_must_redraw = True


def get_raster_position(mouse):
    """
    :param mouse: the position of the event (the mouse)
    :return: the position of the mouse with respect to the drawing space
    """
    x_raster_pos = float(mouse[0] - X_OFFSET) / X_SIZE
    y_raster_pos = float(mouse[1] - Y_OFFSET) / Y_SIZE
    return x_raster_pos, y_raster_pos


def process_keyboard_input(user_event):
    global values, raster_must_redraw, shift_is_pressed
    raster_must_redraw = True
    # Save the currently drawn image on space or return.
    if user_event.key == 13 or user_event.key == 32:
        save_bitmap_image()
    # Reset the drawing space on escape or backspace.
    elif user_event.key == 27 or user_event.key == 8:
        values = np.array([[0.0]] * WIDTH * HEIGHT)
    elif user_event.key == 304:
        shift_is_pressed = True

    # Deals with the 'w', 'a', 's', 'd', and 'r' inputs.
    elif 32 <= user_event.key < 128 and chr(user_event.key) in "wasdr":
        x_range, y_range = FileProcessor.calculate_shift_ranges(values)
        shift_delta = (0, 0)
        if user_event.key == ord('w') and (shift_is_pressed or y_range[0] < 0):
            shift_delta = (0, -1)
        elif user_event.key == ord('a') and (shift_is_pressed or x_range[0] < 0):
            shift_delta = (-1, 0)
        elif user_event.key == ord('s') and (shift_is_pressed or y_range[1] > 0):
            shift_delta = (0, +1)
        elif user_event.key == ord('d') and (shift_is_pressed or x_range[1] > 0):
            shift_delta = (+1, 0)
        elif user_event.key == ord('r'):
            rnd_x = random.randint(x_range[0], x_range[1])
            rnd_y = random.randint(y_range[0], y_range[1])
            shift_delta = (rnd_x, rnd_y)
        if shift_delta != (0, 0):
            values = FileProcessor.shift_all_values(values, shift_delta)


# Adjusting the Drawing and the Values
def add_brush_to_values_at(xy_pos):
    global clicking
    for r in range(len(BRUSH)):
        for c in range(len(BRUSH[r])):
            if BRUSH[r][c] != ' ':
                ink = clicking * 1.0 / MAX_VALUES
                add_to_values_at_static((xy_pos[0] + c, xy_pos[1] + r), ink)


def add_to_values_at_static(pos, ink):
    """
    'draws' pixels at the target location using set_val, and possibly in surrounding pixels
    :param pos: x and y values dictating where to draw the pixel.
    :param ink: how much to add, as a fraction of 1.
        ink must be less than 1, because it is multiplied by up to 5. ink can be negative!
    """
    if 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT:
        r, c = int(pos[1]), int(pos[0])
        up, dn, lf, rt = pos[1] - r <= .5, pos[1] - r >= .5, pos[0] - c <= .5, pos[0] - c >= .5
        set_val(c, r, get_val(c, r) + ink * 5)
        if r > 0 and up:
            set_val(c, r - 1, get_val(c, r - 1) + ink * 2)
            if c > 0 and lf:
                set_val(c - 1, r - 1, get_val(c - 1, r - 1) + ink * 1)
            if c > WIDTH - 1 and rt:
                set_val(c + 1, r - 1, get_val(c + 1, r - 1) + ink * 1)
        if c > 0 and lf:
            set_val(c - 1, r, get_val(c - 1, r) + ink * 2)
        if r < HEIGHT - 1 and dn:
            set_val(c, r + 1, get_val(c, r + 1) + ink * 2)
            if c > 0 and lf:
                set_val(c - 1, r + 1, get_val(c - 1, r + 1) + ink * 1)
            if c > WIDTH - 1 and rt:
                set_val(c + 1, r + 1, get_val(c + 1, r + 1) + ink * 1)
        if c > WIDTH - 1 and rt:
            set_val(c + 1, r, get_val(c + 1, r) + ink * 2)


def draw_raster(window):
    """
    Draws the current array of values on the pygame window.
    :param window: the pygame window surface in which to draw the values.
    """
    rect_border = 1
    pygame.draw.rect(window, BLACK,
                     (X_OFFSET - rect_border,
                      Y_OFFSET - rect_border,
                      WIDTH * X_SIZE + rect_border * 2,
                      HEIGHT * Y_SIZE + rect_border * 2),
                     rect_border)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            x = X_OFFSET + X_SIZE * c
            y = Y_OFFSET + Y_SIZE * r
            pygame.draw.rect(window, get_color_from_value(get_val(c, r)),
                             (x, y, X_SIZE, Y_SIZE))


def brush_to_values_raster(brush, intensity):
    """
    :param brush: the thing to draw.
    :param intensity: how much to add, as a fraction of 1. to be passed to add_to_values_at_static.
    """
    for r in range(len(brush)):
        for c in range(len(brush[r])):
            if brush[r][c] != ' ':
                add_to_values_at_static((c + 0.5, r + 0.5), intensity)


# Miscellaneous
def save_bitmap_image():
    image_name = FileProcessor.get_complete_title('Image', 'bitmap_images', '.bmp')
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(WHITE)
    pix_array = pygame.PixelArray(surf)
    for r in range(HEIGHT):
        for c in range(WIDTH):
            # note: pygame pixel maps are x/y not row/col
            pix_array[c][r] = get_color_from_value(get_val(c, r))
    del pix_array
    pygame.image.save(surf, image_name)


def get_color_from_value(v):
    """
    Returns a shade of grey in RGB from a single value between 0 and MAX_VALUES.
    The higher the value, the darker the shade, based off of the proportion of the value versus MAX_VALUES.
    :param v: a value between 0 and MAX_VALUES.
    :return: a tuple of three of the same integers between 0 and 255, representing a shade of grey.
    """
    if v <= 0:
        return WHITE
    if v > 1:
        v = 1
    v = 255 - int(255 * v)
    return v, v, v


def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


if __name__ == "__main__":
    pygame.init()
    window_surface = pygame.display.set_mode((500, 400), 0, 24)
    pygame.display.set_caption("SHIS Digit Drawing")

    font_size = 48
    basic_font = pygame.font.SysFont(None, font_size)
    text = basic_font.render('esc to clear - enter to save', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = window_surface.get_rect().centerx
    text_rect.y = window_surface.get_rect().height - font_size

    window_surface.fill(WHITE)
    window_surface.blit(text, text_rect)

    pygame.display.update()

    app_is_running = True
    while app_is_running:
        for event in pygame.event.get():
            process_input(event)
        if raster_must_redraw:
            draw_raster(window_surface)
            pygame.display.update()
            raster_must_redraw = False
    pygame.quit()

    brush_to_values_raster([
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
        "                            "], 0.1)
    positions = FileProcessor.range_of_shiftable_positions(values)
    for delta in positions:
        print(delta)
        FileProcessor.shift_all_values(values, delta)
        FileProcessor.draw_input_to_ascii(values)

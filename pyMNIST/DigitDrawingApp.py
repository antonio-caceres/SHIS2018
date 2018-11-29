"""
An extremely simple image editor for 28x28 blackk-and-white images, created by Mr. V for Antonio.
Much of the code used in this project is from https://inventwithpython.com/pygameHelloWorld.py
Install pygame using the Terminal:
    sudo pip install pygame
Install pip using the Terminal:
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
"""
import pygame, sys, os, random
from pygame.locals import *  # for QUIT and other state/type info

# Drawing Area Constants
HEIGHT, WIDTH = 28, 28
SIZE = (10, 10)
OFFSET = (20, 20)
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


def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def new_2d_values(height, width):
    values = []
    for r in range(height):
        values.append([])
        for c in range(width):
            values[r].append(0)
    return values


def value_to_color(v):
    if v <= 0:
        return WHITE
    if v > MAX_VALUES:
        v = MAX_VALUES
    v = int(float(MAX_VALUES - v) / MAX_VALUES * 255)
    return v, v, v


def draw_raster(values, offset, size, window_surface):
    height, width = len(values), len(values[0])
    rect_border = 1
    pygame.draw.rect(window_surface, BLACK,
                     (offset[0] - rect_border,
                      offset[1] - rect_border,
                      width * size[0] + rect_border * 2,
                      height * size[1] + rect_border * 2),
                     rect_border)
    for r in range(height):
        for c in range(width):
            x, y = offset[0] + size[0] * c, offset[1] + size[1] * r
            color = value_to_color(values[r][c])
            pygame.draw.rect(window_surface, color, (x, y, size[0], size[1]))


def get_raster_position(mouse, offset, size):
    return float(mouse[0] - offset[0]) / size[0], float(mouse[1] - offset[1]) / size[1]


def create_and_save_image(values, image_name):
    height, width = len(values), len(values[0])
    surf = pygame.Surface((width, height))
    surf.fill(WHITE)
    pix_array = pygame.PixelArray(surf)
    for r in range(height):
        for c in range(width):
            pix_array[c][r] = value_to_color(values[r][c])  # note: pygame pixel maps are x/y not row/col
    del pix_array
    pygame.image.save(surf, image_name)


def get_complete_title(base_title):
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


def add_to_values_at(values, p, add=1):
    if 0 <= p[0] < WIDTH and 0 <= p[1] < HEIGHT:
        r,c = int(p[1]),int(p[0])
        up,dn,lf,rt = p[1]-r < .5, p[1]-r > .5,p[0]-c < .5,p[0]-c > .5
        values[r][c] += add*5
        if r > 0 and up:
            values[r-1][c] += add*2
            if c > 0 and lf: values[r-1][c-1] += add*1
            if c > WIDTH-1 and rt:values[r-1][c+1] += add*1
        if c > 0 and lf:
            values[r][c-1] += add*2
        if r < HEIGHT-1 and dn:
            values[r+1][c] += add*2
            if c > 0 and lf: values[r+1][c-1] += add*1
            if c > WIDTH-1 and rt:values[r+1][c+1] += add*1
        if c > WIDTH-1 and rt:
            values[r][c+1] += add*2


def add_brush_to_values_at(values, posxy, brush, add=1):
    for r in range(len(brush)):
        for c in range(len(brush[r])):
            if brush[r][c] != ' ':
                add_to_values_at(values, (posxy[0] + c, posxy[1] + r), add)


def bound_box_of_values(values):
    """returns ((minx,miny),(maxx,maxy))"""
    height, width = len(values), len(values[0])
    min, max = [width,height], [-1,-1]
    for r in range(height):
        for c in range(width):
            if values[r][c] != 0:
                if c < min[0]: min[0] = c
                if r < min[1]: min[1] = r
                if c > max[0]: max[0] = c
                if r > max[1]: max[1] = r
    return ((min[0],min[1]), (max[0],max[1]))


def shift_list(list, delta, fill_extra_with=None):
    import copy
    if delta < 0: # go backwards, losing values at the front
        for i in range(0, len(list)+delta):
            list[i] = list[i-delta]
        if fill_extra_with != None:
            for i in range(len(list)+delta, len(list)):
                list[i] = copy.copy(fill_extra_with)
    if delta > 0:
        for i in range(len(list)-1, -1, -1):
            list[i] = list[i-delta]
        if fill_extra_with != None:
            for i in range(delta-1, -1, -1):
                list[i] = copy.copy(fill_extra_with)

def shift_all_values(values, deltaxy):
    for r in range(len(values)):
        shift_list(values[r], deltaxy[0], 0)
    shift_list(values, deltaxy[1], [0]*len(values[0]))


def calculate_shift_ranges(values):
    """return ((max_left, max_right),(max_up, max_down))"""
    bounds = bound_box_of_values(values)
    rangex = (-bounds[0][0], WIDTH-bounds[1][0]-1)
    rangey = (-bounds[0][1], HEIGHT-bounds[1][1]-1)
    return (rangex, rangey)


def create_and_run_app():
    pygame.init()  # set up pygame
    window_surface = pygame.display.set_mode((500, 400), 0, 24)  # set up the window
    pygame.display.set_caption("SHIS Digit Drawing")

    # set up fonts
    font_size = 48
    basic_font = pygame.font.SysFont(None, font_size)

    # set up the text
    text = basic_font.render('esc to clear - enter to save', True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = window_surface.get_rect().centerx
    text_rect.y = window_surface.get_rect().height - font_size;

    window_surface.fill(WHITE)  # draw the white background onto the surface
    window_surface.blit(text, text_rect)  # draw the text onto the surface

    values = new_2d_values(HEIGHT, WIDTH)

    pygame.display.update()

    clicking = False
    raster_must_redraw = True
    shift_is_pressed = False
    app_is_running = True
    while app_is_running:
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                app_is_running = False
            elif event.type == KEYDOWN:
                raster_must_redraw = True
                if event.key == 13 or event.key == 32:  # save on space or return
                    create_and_save_image(values, get_complete_title("Image "))
                elif event.key == 27 or event.key == 8:  # reset on escape or backspace
                    values = new_2d_values(HEIGHT, WIDTH)
                elif event.key == 304:
                    shift_is_pressed = True
                elif event.key >= 32 and event.key < 128 and chr(event.key) in "wasdr":
                    rangex, rangey = calculate_shift_ranges(values)
                    if event.key == ord('w') and (shift_is_pressed or rangey[0] < 0):
                        shift_all_values(values, (0,-1))
                    elif event.key == ord('a') and (shift_is_pressed or rangex[0] < 0):
                        shift_all_values(values, (-1,0))
                    elif event.key == ord('s') and (shift_is_pressed or rangey[1] > 0):
                        shift_all_values(values, (0,1))
                    elif event.key == ord('d') and (shift_is_pressed or rangex[1] > 0):
                        shift_all_values(values, (1,0))
                    elif event.key == ord('r'):
                        import random
                        rndx = random.randint(rangex[0],rangex[1])
                        rndy = random.randint(rangey[0],rangey[1])
                        shift_all_values(values, (rndx, rndy))
            elif event.type == KEYUP:
                if event.key == 304:
                    shift_is_pressed = False
            elif event.type == MOUSEBUTTONDOWN:
                clicking = (1,-1)[event.button==3]
                rasterPos = get_raster_position(event.pos, OFFSET, SIZE)
                add_brush_to_values_at(values, rasterPos, BRUSH, clicking)
                raster_must_redraw = True
            elif event.type == MOUSEBUTTONUP:
                clicking = False
            elif event.type == MOUSEMOTION:
                if clicking:
                    rasterPos = get_raster_position(event.pos, OFFSET, SIZE)
                    add_brush_to_values_at(values, rasterPos, BRUSH, clicking)
                    raster_must_redraw = True
        if raster_must_redraw:
            draw_raster(values, OFFSET, SIZE, window_surface)
            pygame.display.update()  # draw the window onto the screen
            raster_must_redraw = False
    pygame.quit()

if __name__ == "__main__":
    create_and_run_app()
    sys.exit()

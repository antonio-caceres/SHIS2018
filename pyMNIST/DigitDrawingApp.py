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


def draw_raster(values, offset, size):
    height, width = len(values), len(values[0])
    rect_border = 1
    pygame.draw.rect(windowSurface, BLACK,
                     (offset[0] - rect_border,
                      offset[1] - rect_border,
                      width * size[0] + rect_border * 2,
                      height * size[1] + rect_border * 2),
                     rect_border)
    for r in range(height):
        for c in range(width):
            x, y = offset[0] + size[0] * c, offset[1] + size[1] * r
            color = value_to_color(values[r][c])
            pygame.draw.rect(windowSurface, color, (x, y, size[0], size[1]))


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


def add_to_values_at(values, p):
    if 0 <= p[0] < WIDTH and 0 <= p[1] < HEIGHT:
        r,c = int(p[1]),int(p[0])
        up,dn,lf,rt = p[1]-r < .5, p[1]-r > .5,p[0]-c < .5,p[0]-c > .5
        values[r][c] += 5
        if r > 0 and up:
            values[r-1][c] += 2
            if c > 0 and lf: values[r-1][c-1] += 1
            if c > WIDTH-1 and rt:values[r-1][c+1] += 1
        if c > 0 and lf:
            values[r][c-1] += 2
        if r < HEIGHT-1 and dn:
            values[r+1][c] += 2
            if c > 0 and lf: values[r+1][c-1] += 1
            if c > WIDTH-1 and rt:values[r+1][c+1] += 1
        if c > WIDTH-1 and rt:
            values[r][c+1] += 2


def add_brush_to_values_at(values, rasterPos, brush):
    for r in range(len(brush)):
        for c in range(len(brush[r])):
            if brush[r][c] != ' ':
                add_to_values_at(values, (rasterPos[0] + c, rasterPos[1] + r))


pygame.init()  # set up pygame
windowSurface = pygame.display.set_mode((500, 400), 0, 24)  # set up the window
pygame.display.set_caption("SHIS Digit Drawing")

# set up fonts
font_size = 48
basic_font = pygame.font.SysFont(None, font_size)

# set up the text
text = basic_font.render('esc to clear - enter to save', True, BLACK, WHITE)
text_rect = text.get_rect()
text_rect.centerx = windowSurface.get_rect().centerx
text_rect.y = windowSurface.get_rect().height - font_size;

windowSurface.fill(WHITE)  # draw the white background onto the surface
windowSurface.blit(text, text_rect)  # draw the text onto the surface

values = new_2d_values(HEIGHT, WIDTH)

pygame.display.update()

clicking = False
raster_must_redraw = True

while True:
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == 13 or event.key == 32:  # save on space or return
                create_and_save_image(values, get_complete_title("Image "))
            if event.key == 27 or event.key == 8:  # reset on escape or backspace
                values = new_2d_values(HEIGHT, WIDTH)
                raster_must_redraw = True
        elif event.type == MOUSEBUTTONDOWN:
            clicking = True
            rasterPos = get_raster_position(event.pos, OFFSET, SIZE)
            add_brush_to_values_at(values, rasterPos, BRUSH)
            raster_must_redraw = True
        elif event.type == MOUSEBUTTONUP:
            clicking = False
        elif event.type == MOUSEMOTION:
            if clicking:
                rasterPos = get_raster_position(event.pos, OFFSET, SIZE)
                add_brush_to_values_at(values, rasterPos, BRUSH)
                raster_must_redraw = True
        if raster_must_redraw:
            draw_raster(values, OFFSET, SIZE)
            pygame.display.update()  # draw the window onto the screen
    raster_must_redraw = False

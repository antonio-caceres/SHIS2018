# created by Mr. V, for Antonio, as a quick-and-sort-of-dirty image editor
# extremely simple image editor for 28x28 black-and-white images
# to install pygame:
#   sudo pip install pygame
# if you need pip: curl https://bootstrap.pypa.io/get-pip.py > get-pip.py

# much of this code is from https://inventwithpython.com/pygameHelloWorld.py
import os
import pygame, sys
from pygame.locals import * # for QUIT, and other state/type info

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 24)
pygame.display.set_caption('Hello world!')

# pygame.mouse.set_cursor(*pygame.cursors.arrow)

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up fonts
font_size = 48
basicFont = pygame.font.SysFont(None, font_size)

# set up the text
text = basicFont.render('esc to clear - enter to save', True, BLACK, WHITE)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.y = windowSurface.get_rect().height - font_size;

# draw the white background onto the surface
windowSurface.fill(WHITE)

# draw a green polygon onto the surface
# pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# draw some blue lines onto the surface
# pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
# pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120))
# pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)

# draw a blue circle onto the surface
# pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

# draw a red ellipse onto the surface
# pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)

# draw the text's background rectangle onto the surface
# pygame.draw.rect(windowSurface, RED, (textRect.left-20, textRect.top-20, textRect.width+40, textRect.height+40))

# get a pixel array of the surface
# pixArray = pygame.PixelArray(windowSurface)
# pixArray[480][380] = BLACK
# del pixArray

# draw the text onto the surface
windowSurface.blit(text, textRect)


def rc():  # random color
    import random
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


height, width = 28, 28
size = (10,10)
offset = (20,20)
MAX_VALUES = 12
values = None # will be an array of integers, from 0 to MAXVALUES


def new_2d_values(height, width):
    values = []
    for r in range(height):
        values.append([])
        for c in range(width):
            values[r].append(0)
    return values


values = new_2d_values(height, width)


def value_to_color(v):
    if v <= 0: return WHITE
    if v > MAX_VALUES: v = MAX_VALUES
    v = int(float(MAX_VALUES - v) / MAX_VALUES * 255)
    return v, v, v


def draw_raster(values, offset, size):
    height, width = len(values), len(values[0])
    rect_border = 1
    pygame.draw.rect(windowSurface, BLACK, (
        offset[0]-rect_border,
        offset[1]-rect_border,
        width*size[0]+rect_border*2,
        height*size[1]+rect_border*2), rect_border)
    for r in range(height):
        for c in range(width):
            x, y = offset[0]+size[0]*c, offset[1]+size[1]*r
            color = value_to_color(values[r][c])
            pygame.draw.rect(windowSurface, color,
                #(textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40)
                (x, y, size[0], size[1])
            )


def get_raster_position(mouse, offset, size):
    return (float(mouse[0]-offset[0])/size[0], float(mouse[1]-offset[1])/size[1])


def create_and_save_image(values, imageName):
    height, width = len(values), len(values[0])
    surf = pygame.Surface((width, height))
    surf.fill(WHITE)
    pixArray = pygame.PixelArray(surf)
    for r in range(height):
        for c in range(width):
            pixArray[c][r] = value_to_color(values[r][c]) # note: pygame pixel maps are x/y not row/col
    del pixArray
    pygame.image.save(surf, imageName)


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


# draw the window onto the screen
pygame.display.update()

clicking = False
rasterMustRedraw = True
# run the game loop
while True:
    for event in pygame.event.get():
        # print(event)
        if event.type == QUIT:
            create_and_save_image(values, get_complete_title("Image"))
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == 13 or event.key == 32: # save on space or return
                create_and_save_image(values, get_complete_title("Image"))
            if event.key == 27 or event.key == 8: # reset on escape or backspace
                values = new_2d_values(height, width)
                rasterMustRedraw = True
        elif event.type == MOUSEBUTTONDOWN:
            clicking = True
        elif event.type == MOUSEBUTTONUP:
            clicking = False
        elif event.type == MOUSEMOTION:
            if clicking:
                rasterPos = get_raster_position(event.pos, offset, size)
                if (rasterPos[0] >= 0 and rasterPos[0] < width 
                and rasterPos[1] >= 0 and rasterPos[1] < height):
                    r,c = int(rasterPos[1]),int(rasterPos[0])
                    up,dn,lf,rt = rasterPos[1]-r < .5, rasterPos[1]-r > .5,rasterPos[0]-c < .5,rasterPos[0]-c > .5
                    values[r][c] += 5
                    if r > 0 and up:
                        values[r-1][c] += 2
                        if c > 0 and lf: values[r-1][c-1] += 1
                        if c > width-1 and rt:values[r-1][c+1] += 1
                    if c > 0 and lf:
                        values[r][c-1] += 2
                    if r < height-1 and dn:
                        values[r+1][c] += 2
                        if c > 0 and lf: values[r+1][c-1] += 1
                        if c > width-1 and rt:values[r+1][c+1] += 1
                    if c > width-1 and rt:
                        values[r][c+1] += 2
                    rasterMustRedraw = True
        if rasterMustRedraw:
            draw_raster(values, offset, size)
            # draw the window onto the screen
            pygame.display.update()
    rasterMustRedraw = False


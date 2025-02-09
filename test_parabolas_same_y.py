# this is not a unit test but a graphical test
# to stop mistakes early!
import pygame
import random
import math
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE
from pygame import gfxdraw
from parabola import Parabola,intersect_parabolas
from globals import *

import sys


# GLOBAL_FONT = pygame.font.SysFont("monospace", 30)



# pretty high threshold tbh
TOLERANCE = 0.01
def find_intersection(first_points, second_points):
    # find intersection in O(n^2)
    # this remains here for comparison purposes
    for element in first_points:
        for second_element in second_points:
            if math.isclose(element[0], second_element[0],rel_tol=TOLERANCE) and math.isclose(element[1], second_element[1],rel_tol=TOLERANCE):
                return element


def find_intersection_parabola(x_f_1, y_f_1, y_d_1, x_f_2, y_f_2, y_d_2):
    # lets try a math approach instead of bruteforcing both circles
    pass

def draw_circle_alpha(color, center, radius, alpha):
    global SCREEN

    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    shape_surf.set_alpha(alpha)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    SCREEN.blit(shape_surf, target_rect)


def update():
    global POINTS
    for x, y in POINTS:
        draw_circle_alpha(COLOR_BLACK, (x, y), 10, 255)


def generate_random_points():
    global POINTS
    for _ in range(10):
        x = random.randint(0, WINDOW_HEIGHT)
        y = random.randint(0, WINDOW_WIDTH)
        POINTS.append((x, y))


def draw_line(height):
    global SCREEN
    pygame.draw.line(SCREEN, COLOR_RED, (0, height), (WINDOW_WIDTH, height), 2)


def derive_parabola(COLOR, x_f, y_f, y_d):
    global SCREEN
    # a parabola can be considered as a combination of a directrix and focus
    # for the time being, our directix is the cursor position
    local_points = []
    for x in range(0, WINDOW_WIDTH):
        y = ((x - x_f)**2)/(2*(y_f - y_d)) + ((y_f + y_d)/2)
        if x > 0 and y > 0:
            local_points.append((int(x), int(y)))

    return local_points


def main():
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, POINTS
    pygame.init()
    # pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    # CLOCK = pygame.tick.Clock()

    step = 0

    i = 0
    POINTS = []

    FOCUS = (200, 300)
    SECOND_FOCUS = (400, 300)
    POINTS.append(FOCUS)
    POINTS.append(SECOND_FOCUS)


    # generate_random_points()

    current_position = 400
    first_parabola = Parabola(FOCUS[0], FOCUS[1], current_position)
    second_parabola = Parabola(SECOND_FOCUS[0], SECOND_FOCUS[1], current_position)
    intersection = intersect_parabolas(first_parabola, second_parabola)
    print(intersection)

    while True:
        SCREEN.fill(COLOR_WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_r:
                    POINTS = []
                    # generate_random_points()
                elif event.key == K_s:

                    i += 1
                elif event.key == K_ESCAPE:
                    sys.exit()

        draw_circle_alpha(COLOR_BLACK, FOCUS, 3, 240)
        draw_circle_alpha(COLOR_BLACK, SECOND_FOCUS, 3, 240)
        # cursor_position = pygame.mouse.get_pos()[1]
        # visualiation basic code
        first_parabola.draw(SCREEN)
        second_parabola.draw(SCREEN)

        draw_circle_alpha(COLOR_RED, intersection, 3, 255)
        # actual working of the main part



        pygame.display.update()


if __name__ == "__main__":
    main()

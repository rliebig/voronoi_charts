import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE

import sys


# GLOBAL_FONT = pygame.font.SysFont("monospace", 30)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


COLOR_RED = (125, 0, 1)
COLOR_GREEN = (5, 125, 6)
COLOR_BLUE = (4, 57, 115)
COLOR_YELLOW = (128, 128, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (90, 90, 90)
COLOR_WHITE = (255, 255, 255)

def draw_circle_alpha(color, center, radius, alpha):
    global SCREEN

    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    shape_surf.set_alpha(alpha)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    SCREEN.blit(shape_surf, target_rect)


def update():
    global POINTS
    for x,y in POINTS:
        draw_circle_alpha(COLOR_BLACK, (x,y), 10, 255)


def generate_random_points():
    global POINTS
    for _ in range(10):
        x = random.randint(0, WINDOW_HEIGHT)
        y = random.randint(0, WINDOW_WIDTH)
        POINTS.append((x, y))

def draw_line(height):
    global SCREEN
    pygame.draw.line(SCREEN, COLOR_RED, (0, height), (WINDOW_WIDTH, height), 2)


def main():
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, POINTS
    pygame.init()
    # pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    # CLOCK = pygame.tick.Clock()

    step = 0

    i = 0
    POINTS = []
    
    # generate_random_points()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_r:
                    POINTS = []
                    # generate_random_points()
                # elif event.key == K_s:
                elif event.key == K_ESCAPE:
                    sys.exit()

            SCREEN.fill(COLOR_WHITE)
            update()

            cursor_position = pygame.mouse.get_pos()
            draw_line(cursor_position[1])

            pygame.display.update()

if __name__ == "__main__":
    main()

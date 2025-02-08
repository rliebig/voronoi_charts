import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE
from enum import Enum
from utilities import COLOR_OFFWHITE, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_GREY, COLOR_BLACK, COLOR_WHITE
# make local imports verbose
from .Ort import Ort

import sys


# I apologize about the denglish notation. Denglish means
# a combiniation of english and german words ( Deutsch + Englisch = denglisch)
# i wrote this to study for a exam about algorihtmic geometry
# and needed to memorize the terms 
# GLOBAL_FONT = pygame.font.SysFont("monospace", 30)

MOUSE_MODE = False

WINDOW_HEIGHT = 800 
WINDOW_WIDTH = 800

def generate_random_points():
    global POINTS
    for i in range(100):
        x = random.randint(1, WINDOW_HEIGHT)
        y = random.randint(1, WINDOW_WIDTH)
        # we should reject points in two close 
        # proximity to each other
        POINTS.append(Ort(x, y, i))

def draw_line(height):
    global SCREEN
    pygame.draw.line(SCREEN, COLOR_RED, (0, height), (WINDOW_WIDTH, height), 2)


def derive_parabola(x_f, y_f, y_d):
    # a parabola can be considered as a combination of a directrix and focus
    local_points = []
    for x in range(0, WINDOW_WIDTH):
        y = ((x - x_f)**2)/(2*(y_f - y_d)) + ((y_f + y_d)/2) 
        local_points.append((int(x), int(y)))


    return local_points
    # pygame.draw.lines(SCREEN, COLOR_GREEN, False, local_points)


class Beachline():
    items = []
    collisions = []
    def __init__(self, size=WINDOW_WIDTH):
        # initialize empty array
        self.items = [[0, 0] for x in range(WINDOW_WIDTH+1)] 
        self.collisions = list()
        self.collided_wellenstuecke = list()

    def reset_collisions(self):
        self.collision = list()
        self.collided_wellenstuecke = list()

    def add(self, L, x, y): 
        # always forwards - never backwards!

        if not x > 0:
            return

        if self.items[y][0] < x and x < WINDOW_HEIGHT:
            self.items[y][0] = x
            self.items[y][1] = L
            return True

        return False


    def collect(self):
        return [(x, y[0]) for x,y in enumerate(self.items)]

    def get_collisions(self):
        return self.collisions

def main():
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, POINTS, GLOBAL_SET
    pygame.init()
    # pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    # CLOCK = pygame.tick.Clock()

    POINTS = []
    generate_random_points()

    BEACH_LINE = Beachline()
    WATCHED_ENDPOINTS = []

    permanent_points = []
    cursor_position = 0
    

    while True:
        SCREEN.fill(COLOR_OFFWHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_r:
                    POINTS = []
                    cursor_position = 0
                    WATCHED_ENDPOINTS = []
                    generate_random_points() 
                    permanent_points = []
                    BEACH_LINE = Beachline()
                    GLOBAL_SET.clear()
                    # GLOBAL_SET = set() 
                elif event.key == K_s:
                    if not MOUSE_MODE:
                        cursor_position += 1
                    i += 1
                elif event.key == K_ESCAPE:
                    sys.exit()

        if MOUSE_MODE:
            cursor_position = pygame.mouse.get_pos()[1]
        else:
            cursor_position = cursor_position + 1
        # visualiation basic code
        draw_line(cursor_position)
        # actual working of the main part
        for point in POINTS:
            if cursor_position == point.y:
                WATCHED_ENDPOINTS.append(point)
                point.state = ORT_STATE.ACTIVE
                global_toggle = True

            point.draw()
                

        # lets introduce logic for the spike line 
        rejection_candidates = []
        wellen_stuecke = []
        BEACH_LINE.reset_collisions()
        for point in WATCHED_ENDPOINTS:
            position = point.position
            if cursor_position == point.y:
                # object becomes interesting in a different time frame
                continue

            wellen_stueck = derive_parabola(point.x, point.y, cursor_position)
            wellen_stuecke.append(wellen_stueck)

            # we should check for collision right here
            only_rejections = True
            for x in wellen_stueck:
                not_rejection = BEACH_LINE.add(position, x[1], x[0])
                if not_rejection:
                    only_rejections = False 

            # if no points are accepted, we have a spike event
            if only_rejections:
                rejection_candidates.append(point)

        collisions = BEACH_LINE.get_collisions()
        new_beachline = BEACH_LINE.collect()
        # well, that did not work out.
        # so, how do we fix this
        # now find all intersections for each pair of wellen_stuecke
                 
        for candidate in rejection_candidates:
            print(f"REJECTION {candidate}")
            WATCHED_ENDPOINTS.remove(candidate)
            for point in POINTS:
                # update main point state for better visualisation
                if candidate.x == point.x and candidate.y == point.y:
                    point.state = ORT_STATE.DEAD
            

        # copy to plain points list
        new_beachline = BEACH_LINE.collect()
        BEACH_LINE.reset_collisions()

        # we should probably remember to which edge
        # a endpoint is connected if I'm being honest
        
        # thesurface second important path of this equation is probably
        

        if len(new_beachline) > 2: 
            pygame.draw.lines(SCREEN, COLOR_GREEN, False, new_beachline)
        
        # this branch is really not great for performance
        # but anyways, sometimes you have to do stupid
        # things
        
        pygame.display.update()

if __name__ == "__main__":
    main()

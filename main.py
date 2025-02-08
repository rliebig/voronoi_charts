import pygame
import math
import random
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE, K_t
from enum import Enum
from copy import deepcopy

import sys

# I apologize about the denglish notation. Denglish means
# a combiniation of english and german words ( Deutsch + Englisch = denglisch)
# i wrote this to study for a exam about algorihtmic geometry
# and needed to memorize the terms 
# GLOBAL_FONT = pygame.font.SysFont("monospace", 30)

MOUSE_MODE = False

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

def generate_random_points():
    global POINTS
    for i in range(10):
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
        local_points.append((x, y))


    return local_points
    # pygame.draw.lines(SCREEN, COLOR_GREEN, False, local_points)

class ORT_STATE(Enum):
    SLEEPING = 0
    ACTIVE = 1
    DEAD = 2
class Ort():
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.state = ORT_STATE.SLEEPING
        self.position = pos

    def draw(self):
        x = self.x
        y = self.y

        if self.state == ORT_STATE.SLEEPING:
            draw_circle_alpha(COLOR_BLACK, (x,y), 10, 255)
        elif self.state == ORT_STATE.ACTIVE:
            draw_circle_alpha(COLOR_RED, (x,y), 10, 255)
        elif self.state == ORT_STATE.DEAD:
            draw_circle_alpha(COLOR_BLUE, (x,y), 10, 255)

GLOBAL_SET = {}

# lets memorize round, when something was added.
# it is only a true intersection, if it has been
# added in the same round!
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
        global GLOBAL_SET
        # always forwards - never backwards!

        if not x > 0:
            return

        toggle = False 
        if self.items[y][0] < x and x < WINDOW_HEIGHT:
            self.items[y][0] = x
            self.items[y][1] = L
            toggle = True
            try:
                # lets try finding local minima
                if (self.items[y+2][0] > x and self.items[y-2][0] > x) or (self.items[y-2][0] < x and self.items[y-2][0] > x):
                    global GLOBAL_SET, SCREEN
                    draw_circle_alpha(COLOR_RED, (y,x ), 7, 255)
                    self.collisions.append([y,x])
            except Exception as e:
                print(e)

        # elif self.items[y][1] != L and math.isclose(self.items[y][0], x, rel_tol=1e-05) and y == y: # true intersection
        # elif self.items[y][0] == x and y == y : # true intersection
        # ensure only one collision per round! 
        #for collided in self.collided_wellenstuecke:

        #    if  self.items[y][1] == collided[1]:
            # if L == collided[0] and self.items[y][1] == collided[1]:
        #        return False

            #values = GLOBAL_SET[target_string]
            #for val in values:
            #    if val[0] == y:
            #        return False
          

        print(len(self.collisions))
        return toggle


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

    step = 0

    i = 0
    POINTS = []
    POINTS.append(Ort(200, 100, 0))
    POINTS.append(Ort(700, 100, 1))
    POINTS.append(Ort(400, 50, 2))

    BEACH_LINE = Beachline()
    WATCHED_ENDPOINTS = []
    permanent_points = []
    cursor_position = 0
    
    # generate_random_points()
    global_toggle = False

    while True:
        SCREEN.fill(COLOR_WHITE)
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
                elif event.key == K_t:
                    cursor_position = 0
                    WATCHED_ENDPOINTS = []
                    permanent_points = []
                    BEACH_LINE = Beachline()
                    GLOBAL_SET.clear()
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
                BEACH_LINE.add(cursor_position, point.y, point.x) # special sauce?
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
        for x in collisions:
            permanent_points.append(x)

        for x in permanent_points:
            SCREEN.set_at((int(x[0]), int(x[1])), COLOR_RED)

        BEACH_LINE.reset_collisions()

        # we should probably remember to which edge
        # a endpoint is connected if I'm being honest
        
        # thesurface second important path of this equation is probably

        
        if global_toggle:
            for elem in GLOBAL_SET.values():
                #indices_to_remove = []
                #for second_elem in elem:
                #    if elem[0] == second_elem[0]:
                #        indices_to_remove.append(second_elem)

                #actual_ones = deepcopy(elem)
                #for second_elem in indices_to_remove:
                #    print("removing duplicate y coordinate")
                #    actual_one.remove(second_elem)
                
                if len(elem) > 2:
                    pygame.draw.lines(SCREEN, COLOR_BLACK, False, elem, width=2)

        if len(new_beachline) > 2: 
            pygame.draw.lines(SCREEN, COLOR_GREEN, False, new_beachline)
        
        # this branch is really not great for performance
        # but anyways, sometimes you have to do stupid
        # things
        
        pygame.display.update()

if __name__ == "__main__":
    main()

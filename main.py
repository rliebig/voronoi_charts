import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE
from enum import Enum

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
    for _ in range(10):
        x = random.randint(0, WINDOW_HEIGHT)
        y = random.randint(0, WINDOW_WIDTH)
        POINTS.append(Ort(x, y))

def draw_line(height):
    global SCREEN
    pygame.draw.line(SCREEN, COLOR_RED, (0, height), (WINDOW_WIDTH, height), 2)


def derive_parabola(x_f, y_f, y_d):
    global SCREEN
    # a parabola can be considered as a combination of a directrix and focus
    local_points = []
    for x in range(0, WINDOW_WIDTH):
        y = ((x - x_f)**2)/(2*(y_f - y_d)) + ((y_f + y_d)/2) 
        if y > 0:
            local_points.append((int(x), int(y)))


    return local_points
    # pygame.draw.lines(SCREEN, COLOR_GREEN, False, local_points)

class ORT_STATE(Enum):
    SLEEPING = 0
    ACTIVE = 1
    DEAD = 2
class Ort():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = ORT_STATE.SLEEPING

    def draw(self):
        x = self.x
        y = self.y

        if self.state == ORT_STATE.SLEEPING:
            draw_circle_alpha(COLOR_BLACK, (x,y), 10, 255)
        elif self.state == ORT_STATE.ACTIVE:
            draw_circle_alpha(COLOR_RED, (x,y), 10, 255)
        elif self.state == ORT_STATE.DEAD:
            draw_circle_alpha(COLOR_BLUE, (x,y), 10, 255)

class Beachline():
    items = []
    collisions = []
    def __init__(self, size=WINDOW_WIDTH):
        # initialize empty array
        self.items = [0 for x in range(WINDOW_WIDTH+1)] 
        self.collisions = list()

    def reset_collisions(self):
        self.collision = list()

    def add(self, x, y): 
        # always forwards - never backwards!
        if self.items[y] < x and x < WINDOW_HEIGHT:
            if x > 0:
                self.items[y] = x
                return True

        # elif self.items[y] == x:
        #    self.collisions.append([y,x])
        return False


    def collect(self):
        return [(x, y) for x,y in enumerate(self.items)]

    # def get_collisions(self):
    #     return self.collisions

def main():
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, POINTS
    pygame.init()
    # pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    # CLOCK = pygame.tick.Clock()

    step = 0

    i = 0
    POINTS = []
    POINTS.append(Ort(200, 100))
    POINTS.append(Ort(700, 100))
    POINTS.append(Ort(400, 50))

    BEACH_LINE = Beachline()
    WATCHED_ENDPOINTS = []
    permanent_points = []
    cursor_position = 0
    
    # generate_random_points()

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

            point.draw()
                

        # lets introduce logic for the spike line 
        rejection_candidates = []
        wellen_stuecke = []
        for point in WATCHED_ENDPOINTS:
            if cursor_position == point.y:
                # object becomes interesting in a different time frame
                continue

            wellen_stueck = derive_parabola(point.x, point.y, cursor_position)
            wellen_stuecke.append(wellen_stueck)

            # we should check for collision right here
            only_rejections = True
            for x in wellen_stueck:
                not_rejection = BEACH_LINE.add(x[1], x[0])
                if not_rejection:
                    only_rejections = False 

            # if no points are accepted, we have a spike event
            if only_rejections:
                rejection_candidates.append(point)

        collisions = []
        new_beachline = BEACH_LINE.collect()
        # well, that did not work out.
        # so, how do we fix this
        # now find all intersections for each pair of wellen_stuecke
        for index, element in enumerate(wellen_stuecke):
            # now get all other points
            other_candidates = list()

            if index == 0:
                other_candidates = wellen_stuecke[1:]
            elif index == len(wellen_stuecke) - 1:
                other_candidates = wellen_stuecke[:-1]
            else:
                other_candidates = wellen_stuecke[0:index]
                for j in wellen_stuecke[index+1:]:
                 
                    other_candidates.append(j)
            # print(f"index = {index}")
            # print(f"len = {len(other_candidates)}")

            # find intersection!
            for x in element:
                for j in other_candidates:
                    toggle = False
                    for k in j:
                        # find only _first_ intersection
                        if x[0] == k[0] and x[1] == k[1] and x[0] > 0 and x[1] > 0:
                            # select for intersections on the 
                            # beachline!
                            for l,y in new_beachline:
                                if x[0] == l and x[1] == y:
                                    collisions.append([x[0], x[1]])
                            toggle = True
                            continue

                    if toggle:
                        continue

                 
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

        BEACH_LINE.reset_collisions()

        # we should probably remember to which edge
        # a endpoint is connected if I'm being honest
        
        # the second important path of this equation is probably
        for point in permanent_points:
            print(point)
            x_0 = point[0]
            y_0 = point[1]

            rect = pygame.Rect(x_0, y_0, 1, 1)

            # hack to draw a pixel
            pygame.draw.rect(SCREEN, COLOR_RED, rect)

        

        if len(new_beachline) > 2: 
            pygame.draw.lines(SCREEN, COLOR_GREEN, False, new_beachline)
        
        # this branch is really not great for performance
        # but anyways, sometimes you have to do stupid
        # things
        
        pygame.display.update()

if __name__ == "__main__":
    main()

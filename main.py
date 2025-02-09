import pygame
import math
import random
from pygame.locals import QUIT, KEYDOWN, K_r, K_s, K_ESCAPE, K_t
from utilities import COLOR_OFFWHITE, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_GREY, COLOR_BLACK, COLOR_WHITE
from parabola import Parabola, intersect_parabolas
from enum import Enum
# make local imports verbose
from Ort import Ort, ORT_STATE

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
    for i in range(20):
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
    #
class PointedBeachline():
    def __init__(self, size=WINDOW_WIDTH):
        self.items = [[0,0] for x in range(WINDOW_WIDTH + 1)]

    def add(self, L, x, y):
        if not x > 0 or not y > 0 or y > 799:
            return

        toggle = False
        if self.items[y][0] < x and x < WINDOW_HEIGHT and self.items[y][1] < L:
            self.items[y][0] = x
            self.items[y][1] = L
            toggle = True

        return toggle

    def collect(self):
        return [(x, y[0]) for x,y in enumerate(self.items)]
     
class Beachline():
    wave_pieces = []
    def __init__(self, size=WINDOW_WIDTH):
        # initialize empty array
        self.size = size
        self.wave_pieces = []

    def add(self, current_position, ort):
        # insert so that x coordinates are aligned
        #
        #
        new_parabola = Parabola(ort.x, ort.y, current_position)
        self.wave_pieces.append(new_parabola)
        self.wave_pieces.sort(key=lambda x: x.x_f)

    def draw(self, SCREEN, pointed_beachline, current_position):
        points = []

        for wave_piece in self.wave_pieces:
            wave_piece.y_d = current_position

        # if len(self.wave_pieces) > 1:
            # self.wave_pieces[-1].boundary_right = WINDOW_WIDTH

        # if len(self.wave_pieces) == 1:
            # self.wave_pieces[0].boundary_left = 0
            # self.wave_pieces[0].boundary_right = WINDOW_WIDTH
        print("===============================")
        for i in range(0, len(self.wave_pieces) - 1):
            # find current intersections
            current = self.wave_pieces[i]
            print(f"current i = {i}")
            print(current)
            # we could extract this from loop
            # for even better performance!
            print(f"next wavepice i = {i+1}")
            next_wavepiece = self.wave_pieces[i+1]
            print(next_wavepiece)
            intersection, intersection_two = intersect_parabolas(next_wavepiece, current)
            # only values inside the grpah
            if intersection_two[0] > 0 and intersection_two[0] < WINDOW_WIDTH and intersection_two[1] > 0 and intersection_two[1] < WINDOW_WIDTH:
                points.append(intersection_two)
            if intersection[0] > 0 and intersection[0] < WINDOW_WIDTH and intersection[1] > 0 and intersection[1] < WINDOW_WIDTH:
                points.append(intersection)
            # points.append(intersection)
            # 
        values_to_remove = []
        rejection_candidates = []

        for i in range(len(self.wave_pieces)):
            current = self.wave_pieces[i]
            sec_points = current.draw(SCREEN)
            toggle = False
            for point in sec_points:
                value = pointed_beachline.add(current_position, point[1], point[0])
                if value:
                    toggle = True
            if not toggle:
                values_to_remove.append(current)
                rejection_candidates.append(Ort(current.x_f, current.y_f, 1))

        # implement logic for marking points!
        for value in values_to_remove:
            self.wave_pieces.remove(value)
        if len(values_to_remove) > 0:
            self.wave_pieces.sort(key=lambda x: x.x_f)

        return points, rejection_candidates



# literal names from course text
class EVENT_ENUM(Enum):
    POINT_EVENT = 1
    SPIKE_EVENT = 2

class Event():
    def __init__(self, event_type, time, point, old_wave_piece=None):
        if event_type not in EVENT_ENUM:
            raise Error("Invalid Argument!")

        self.event_type = event_type
        self.time = time
        self.point = point
        if old_wave_piece:
            self.old_wave_piece = old_wave_piece

class SweepStatusStructure():
    def __init__(self):
        self.events = [] # would correctly be a different structure, but oh well

    def add_event(self, event):
        self.events.append(event)

    def process_events(self):
        pass


def main():
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, POINTS
    pygame.init()
    # pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    # CLOCK = pygame.tick.Clock()

    POINTS = []
    POINTS.append(Ort(100, 200, 0))
    # POINTS.append(Ort(200, 204, 0))
    POINTS.append(Ort(300, 200, 0))
    # POINTS.append(Ort(400, 200, 0))
    # POINTS.append(Ort(201, 100, 0))
    POINTS.append(Ort(200, 205, 0))
    POINTS.append(Ort(400, 400, 0))
    #generate_random_points()

    BEACH_LINE = Beachline()
    pointed_beachline = PointedBeachline()
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
                    generate_random_points()
                    cursor_position = 0
                    WATCHED_ENDPOINTS = []
                    permanent_points = []
                    BEACH_LINE = Beachline()
                    pointed_beachline = PointedBeachline()
                    # GLOBAL_SET.clear()
                elif event.key == K_t:
                    cursor_position = 0
                    WATCHED_ENDPOINTS = []
                    permanent_points = []
                    BEACH_LINE = Beachline()
                    pointed_beachline = PointedBeachline()
                    for point in POINTS:
                        point.state = ORT_STATE.SLEEPING

                    # GLOBAL_SET.clear()
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
            if cursor_position - 1 == point.y: # 

                WATCHED_ENDPOINTS.append(point)
                point.state = ORT_STATE.ACTIVE
                BEACH_LINE.add(cursor_position, point)

            point.draw(SCREEN)
                

        # lets introduce logic for the spike line 
        rejection_candidates = []
        wellen_stuecke = []
        # well, that did not work out.
        # so, how do we fix this
        # now find all intersections for each pair of wellen_stuecke
                 
        result, rejection_candidates = BEACH_LINE.draw(SCREEN, pointed_beachline, cursor_position)
        for candidate in rejection_candidates:
            # WATCHED_ENDPOINTS.remove(candidate)
            for point in POINTS:
                # update main point state for better visualisation
                if candidate.x == point.x and candidate.y == point.y:
                    point.state = ORT_STATE.DEAD
            

        # copy to plain points list
        for point in result:
            permanent_points.append(point)

        curr = pointed_beachline.collect()
        if len(curr) > 0:
            pygame.draw.lines(SCREEN, COLOR_GREEN, False, curr, width=2)

        # for x in permanent_points:
        if len(permanent_points) > 2:
            for point in permanent_points:
                SCREEN.set_at(point, COLOR_RED)
            # pygame.draw.lines(SCREEN, COLOR_RED, False, permanent_points, width=2)
            # SCREEN.set_at(x[0], COLOR_RED)
      
        pygame.display.update()

if __name__ == "__main__":
    main()

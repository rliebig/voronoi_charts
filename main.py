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
    for i in range(2):
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
        self.wave_pieces.sort(key=lambda x: new_parabola.x_f)

        
    def draw(self, SCREEN, current_position):
        points = []

        for wave_piece in self.wave_pieces:
            wave_piece.y_d = current_position

        if len(self.wave_pieces) > 1:
            self.wave_pieces[-1].boundary_right = WINDOW_WIDTH

        if len(self.wave_pieces) == 1:
            self.wave_pieces[0].boundary_left = 0
            self.wave_pieces[0].boundary_right = WINDOW_WIDTH
        else:
            for i in range(len(self.wave_pieces)- 1):
                # find current intersections
                current = self.wave_pieces[i]
                # we could extract this from loop
                # for even better performance!
                next_wavepiece = self.wave_pieces[i+1]
                print(current)
                print(next_wavepiece)
                intersection, intersection_two = intersect_parabolas(next_wavepiece, current)
                # current.boundary_left = 0
                # LINKS-Rechts test?
                current.boundary_right = intersection_two[0]
                next_wavepiece.boundary_left = intersection_two[0]

                points.append(intersection_two)
                points.append(intersection)

        for i in range(len(self.wave_pieces)):
            current = self.wave_pieces[i]
            current.draw(SCREEN)

        return points



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
    POINTS.append(Ort(200, 100, 0))
    POINTS.append(Ort(200, 200, 0))
    #generate_random_points()

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
                    # GLOBAL_SET.clear()
                elif event.key == K_t:
                    cursor_position = 0
                    WATCHED_ENDPOINTS = []
                    permanent_points = []
                    BEACH_LINE = Beachline()
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
        print(POINTS)
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
                 
        for candidate in rejection_candidates:
            print(f"REJECTION {candidate}")
            WATCHED_ENDPOINTS.remove(candidate)
            for point in POINTS:
                # update main point state for better visualisation
                if candidate.x == point.x and candidate.y == point.y:
                    point.state = ORT_STATE.DEAD
            

        # copy to plain points list
        result = BEACH_LINE.draw(SCREEN, cursor_position)
        for point in result:
            print(point)
            permanent_points.append(result)

        for x in permanent_points:
            print(x)
            print(len(x))
            SCREEN.set_at(x[0], COLOR_RED)
      
        pygame.display.update()

if __name__ == "__main__":
    main()

from utilities import draw_circle_alpha, COLOR_BLACK, COLOR_RED, COLOR_BLUE
from enum import Enum
from pygame import gfxdraw

CIRCLE_RADIUS = 5



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

    def _draw_circle(self, SCREEN, color, coordinates):
        gfxdraw.aacircle(SCREEN, coordinates[0], coordinates[1], CIRCLE_RADIUS, color)
        gfxdraw.filled_circle(SCREEN, coordinates[0], coordinates[1], CIRCLE_RADIUS, color)

    def draw(self, SCREEN):
        x = self.x
        y = self.y

        if self.state == ORT_STATE.SLEEPING:
            self._draw_circle(SCREEN, COLOR_BLACK, (x,y))
        elif self.state == ORT_STATE.ACTIVE:
            self._draw_circle(SCREEN, COLOR_RED, (x,y))
        elif self.state == ORT_STATE.DEAD:
            self._draw_circle(SCREEN, COLOR_BLUE, (x,y))

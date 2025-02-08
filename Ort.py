from utilities import draw_circle_alpha

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

    def draw(self, SCREEN):
        x = self.x
        y = self.y

        if self.state == ORT_STATE.SLEEPING:
            draw_circle_alpha(SCREEN, COLOR_BLACK, (x,y), CIRCLE_RADIUS, 230)
        elif self.state == ORT_STATE.ACTIVE:
            draw_circle_alpha(SCREEN, COLOR_RED, (x,y), CIRCLE_RADIUS, 230)
        elif self.state == ORT_STATE.DEAD:
            draw_circle_alpha(SCREEN, COLOR_BLUE, (x,y), CIRCLE_RADIUS, 230)

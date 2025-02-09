from globals import *
import math
import pygame

class Parabola():
    """
        This class implements a parabola in
        focal/directrix format
    """
    def __init__(self, x_f, y_f, y_d):
        self.x_f = float(x_f)
        self.y_f = float(y_f)
        self.y_d = float(y_d)

        self.boundary_left = 0
        self.boundary_right = WINDOW_WIDTH

    def __str__(self):
        return f"WAVEPIECE x_f = {self.x_f} x_y = {self.y_f} y_d = {self.y_d}"

    def draw(self, SCREEN):
        local_points = []
        for x in range(self.boundary_left, self.boundary_right):
            y = ((x - self.x_f)**2)/(2*(self.y_f - self.y_d)) + ((self.y_f + self.y_d)/2)
            if x > 0 and y > 0: # sometimes points are generated outside the plain...
                local_points.append((int(x), int(y))) # 

        # if len(local_points) > 2:
            # pygame.draw.lines(SCREEN, COLOR_GREEN, False, local_points, width=2)    

        return local_points

    def convert_to_vertex_focal_length(self):
        """
           This returns the necessary parameters
           for a vertex/focal-length parabola.
           This is being used for the intersection.
           You know this representation form math class!
        """
        p = float(self.x_f)
        q = (float(self.y_f) + float(self.y_d)) / 2
        a = (float(self.y_f) - float(self.y_d)) / 2
        return (p, q), a

        
def _coeffs(vertex, a):
    return 1/(4*a), (-2*vertex[0])/(4*a), vertex[1] + (vertex[0]*vertex[0]/(4*a))

def solve_quadratics(a,b,c):
    d = math.sqrt((b*b)-(4*a*c))
    return (-b+d)/(2*a), (-b-d)/(2*a)

def intersect_parabolas(first: Parabola, second: Parabola):
    first_vertex, first_a = first.convert_to_vertex_focal_length()
    second_vertex, second_a = second.convert_to_vertex_focal_length()

    # two vertices on the same point 
    if first_vertex[1] == second_vertex[1] and first_a == second_a:
        x_second_squared = second_vertex[0] ** 2
        x_first_squared = first_vertex[0] ** 2

        x = (x_second_squared - x_first_squared) / (2*(second_vertex[0] - first_vertex[0]))
        y = (((x - first_vertex[0])*(x - first_vertex[0])) / (4 * first_a)) +  second_vertex[1]

        return (x, y)

    m2, m1, m0 = _coeffs(first_vertex, first_a)
    n2, n1, n0 = _coeffs(second_vertex, second_a)

    x1, x2 = solve_quadratics(m2 - n2, m1 - n1, m0 - n0)
    y1 = (((x1 - first_vertex[0])**2)/(4 * first_a)) + first_vertex[1]
    y2 = (((x2 - first_vertex[0])**2)/(4 * first_a)) + first_vertex[1]

    return (int(x1), int(y1)), (int(x2), int(y2))

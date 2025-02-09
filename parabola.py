class Parabola():
    """
        This class implements a parabola in
        focal/directrix format
    """
    def __init__(self, x_f, y_f, y_d):
        self.x_f = x_f
        self.y_f = y_f
        self.y_d = y_d

    def draw(self, SCREEN, initial_x=0,final_x=WINDOW_WIDTH):
        local_points = []
        for x in range(initial_x, final_x):
            y = ((x - x_f)**2)/(2*(y_f - y_d)) + ((y_f + y_d)/2)
            if x > 0 and y > 0:
                local_points.append((int(x), int(y)))

        return local_points
    

    def convert_to_vertex_focal_length(self):
        """
           This returns the necessary parameters
           for a vertex/focal-length parabola.
           This is being used for the intersection.
           You know this representation form math class!
        """
        p = self.x_f
        q = (self.y_f + self.y_d) / 2
        a = (self.y_f - self.y_d) / 2
        return (p, q), a

        

def intersect_parabolas(first: Parabola, second: Parabola):
    first_vertex, first_a = first.convert_to_vertex_focal_length()
    second_vertex, second_a = second.convert_to_vertex_focal_length()

    # two vertices on the same point 
    if first_vertex[0] == second_vertex[0] and first_a == second_a:
        x_second_squared = second_vertex[1] ** 2
        x_first_squared = first_vertex[1] ** 2
        x = (x_second_squared - x_first_squared) / (2*(second_vertex[1] - first_vertex[1]))
        y = (((x - first_vertex[1])*(x - first_vertex[1])) / (4 * first_a)) +  
        return (x, y)

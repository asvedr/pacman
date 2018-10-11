
EMPTY_VECTOR = (0, 0)
PACMAN_SPEED = 0.3
RED_SPEED = 0.5
BLUE_SPEED = 0.5
PINK_SPEED = 0.5
YELLO_SPEEd = 0.5

class Pers(object):
    
    __slots__ = 'x', 'y', 'color', 'algorithm', 'speed', 'vector', 'is_pacman'
    
    @classmethod
    def pacman(cls, x, y):
        pacman = cls(x, y, pacman_algorithm, None)
        pacman.vector = (0, 0)
        pacman.is_pacman = True
        return pacman

    @classmethod
    def red(cls, x, y):
        return cls(x, y, red_algorithm, 'red')

    @classmethod
    def yello(cls, x, y):
        return cls(x, y, yello_algorithm, 'yello')

    @classmethod
    def pink(cls, x, y):
        return cls(x, y, pink_algorithm, 'pink')

    @classmethod
    def blue(cls, x, y):
        return cls(x, y, blue_algorithm, 'blue')
        
    def __init__(self, x, y, algorithm, color):
        self.x = x
        self.y = y
        self.algorithm = algorithm
        self.color = color
        self.vector = None
        self.is_pacman = False
    
    def move(self, logic):
        self.algorithm(self, logic)    

    def regular_move(self, logic, nx, ny):
        field = logic.field
        if not (0 <= nx < field.width or 0 <= ny < field.height):
            raise Exception('out of map')
        self.x = nx
        self.y = ny


def pacman_algorithm(pers, logic):
    has_turn = False
    if logic.user_vector != EMPTY_VECTOR:
        has_turn = True
        pers.vector = logic.user_vector
    x = pers.x + pers.vector[0] * PACMAN_SPEED * logic.diff_time
    y = pers.y + pers.vector[1] * PACMAN_SPEED * logic.diff_time
    pers.regular_move(logic, x, y)


def red_algorithm(pers, logic):
    # x = logic.pacman.x
    # y = logic.pacman.y
    x = pers.x
    y = pers.y
    pers.regular_move(logic, x, y)
    

blue_algorithm = red_algorithm
pink_algorithm = red_algorithm
yello_algorithm = red_algorithm
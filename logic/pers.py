from logic.path_finder import find_path
from math import floor
from logic.field import Cell
import logging
import enum

EMPTY_VECTOR = (0, 0)
PACMAN_SPEED = 0.2
RED_SPEED = 0.3
BLUE_SPEED = 0.5
PINK_SPEED = 0.5
YELLO_SPEED = 0.5
PREY_SPEED = 0.1
CELL_CENTER_DELTA = 0.2

RED = 'red'
BLUE = 'blue'
YELLO = 'yellow'
PINK = 'pink'

color_list = [RED, BLUE, YELLO, PINK]
color_dict = {color_list[i]:i for i in range(len(color_list))}

v_left = (-1, 0)
v_right = (1, 0)
v_up = (0, -1)
v_down = (0, 1)

turns_for = {v_left  : [v_down, v_up],
             v_right : [v_up, v_down],
             v_up    : [v_left, v_right],
             v_down  : [v_right, v_left],
             EMPTY_VECTOR : []}


class Mode(enum.Enum):
    HUNTER = 0
    PREY = 1


class Pers(object):
    
    __slots__ = ('x', 'y', 'color', 'algorithm',
                 'speed', 'vector', 'is_pacman', 'logger',
                 'start_point', 'mode',
                 'next_point', 'prev_dist')
    
    @classmethod
    def pacman(cls, x, y):
        pacman = cls(x, y, pacman_algorithm, None)
        pacman.vector = (0, 0)
        pacman.is_pacman = True
        return pacman

    @classmethod
    def red(cls, x, y):
        return cls(x, y, red_algorithm, color_dict[RED])

    @classmethod
    def yello(cls, x, y):
        return cls(x, y, yello_algorithm, color_dict[YELLO])

    @classmethod
    def pink(cls, x, y):
        return cls(x, y, pink_algorithm, color_dict[PINK])

    @classmethod
    def blue(cls, x, y):
        return cls(x, y, blue_algorithm, color_dict[BLUE])
        
    def __init__(self, x, y, algorithm, color):
        self.x = x
        self.y = y
        self.start_point = (x, y)
        self.algorithm = algorithm
        self.color = color
        self.vector = EMPTY_VECTOR
        self.is_pacman = False
        self.logger = logging.getLogger('pacman')
        self.mode = Mode.HUNTER
        self.next_point = None
        self.prev_dist = None

    def move(self, logic):
        self.algorithm(self, logic)    

    def regular_move(self, logic, nx, ny):
        field = logic.field
        if not (0 <= nx < field.width or 0 <= ny < field.height):
            raise Exception('out of map')
        self.x = nx
        self.y = ny

    def can_turn(self, field):
        turns = turns_for[self.vector]
        if len(turns) == 0:
            return True
        x = round(self.x) + turns[0][0]
        y = round(self.y) + turns[0][1]
        if field[y][x] != Cell.Wall:
            return True
        x = round(self.x) + turns[1][0]
        y = round(self.y) + turns[1][1]
        if field[y][x] != Cell.Wall:
            return True
        return False

    def point(self):
        return (round(self.x), round(self.y))

    def is_on_cell_center(self):
        x = self.x
        y = self.y
        return x - floor(x) < CELL_CENTER_DELTA and y - floor(y) < CELL_CENTER_DELTA


def pacman_algorithm(pers, logic):
    has_turn = False
    vector = logic.user_vector
    if vector != EMPTY_VECTOR and vector != pers.vector:
        point = pers.point()
        next_pt = (point[0] + vector[0], point[1] + vector[1])
        if logic.field.data[next_pt[0]][next_pt[1]] != Cell.Wall:
            pers.x = point[0]
            pers.y = point[1]
            has_turn = True
            pers.vector = logic.user_vector
    x = pers.x + pers.vector[0] * PACMAN_SPEED
    y = pers.y + pers.vector[1] * PACMAN_SPEED
    pers.regular_move(logic, x, y)


def normal_vector(point):
    x = point[0]
    y = point[1]
    if x != 0:
        x = round(x / abs(x))
    if y != 0:
        y = round(y / abs(y))
    return (x, y)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def ghost_move(pers, logic, fin_point, speed):
    color = pers.color
    if pers.next_point is not None:
        if dist((pers.x, pers.y), pers.next_point) > pers.prev_dist:
            point = pers.point()
            pers.x = point[0]
            pers.y = point[1]
    if pers.is_on_cell_center() and pers.can_turn(logic.field.data):
        if pers.mode == Mode.HUNTER:
            ghost_point = pers.point()
            if pers.vector == EMPTY_VECTOR:
                dont_use = []
            else:
                normal = normal_vector(pers.vector)
                back_x = ghost_point[0] - normal[0]
                back_y = ghost_point[1] - normal[1]
                dont_use = [(back_x, back_y)]
            path = find_path(logic.field.data, dont_use, fin_point, ghost_point)
            if len(path) <= 1:
                if ghost_point == fin_point:
                    logic.pacman_killed()
                return
            next_cell = path[1]
            vector = (next_cell[0] - ghost_point[0], next_cell[1] - ghost_point[1])
            if pers.vector != vector:
                pers.x = ghost_point[0]
                pers.y = ghost_point[1]
            pers.vector = normal_vector(vector)
            pers.next_point = next_cell
        else:
            ways = []
            normal = normal_vector(pers.vector)
            back_pt = None
            x = pers.x
            y = pers.y
            if normal[0] != normal[1]: # Not null vector
                back_pt = (x - normal, y - normal[1])
            for px, py in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pt = (x + px, y + py)
                if next_pt != back_pt:
                    ways.append(next_pt)
            way = random.choice(ways)
            pers.vector = normal_vector((way[0] - x, way[1] - y))
    nx = pers.x + (pers.vector[0] * speed)
    ny = pers.y + (pers.vector[1] * speed)
    pers.regular_move(logic, nx, ny)
    if pers.next_point is not None:
        pers.prev_dist = dist(pers.next_point, (pers.x, pers.y))


def red_algorithm(pers, logic):
    speed = RED_SPEED if pers.mode == Mode.HUNTER else PREY_SPEED
    ghost_move(pers, logic, logic.pacman.point(), speed)
    

blue_algorithm = red_algorithm
pink_algorithm = red_algorithm
yello_algorithm = red_algorithm

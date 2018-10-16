from logic.p_queue import PQueue
from logic.field import Cell

nearest = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Warning: algorithm works only with closed labyrinth
# On open labyrinth there will be exceptions
def find_path(field, dont_use, src_point, dst_point):

    ''' result of this function is list FROM dst_point TO src_point '''

    def volume(point):
        return abs(point[0] - dst_point[0]) + abs(point[1] - dst_point[1])

    queue = PQueue()
    queue.push((src_point, None), volume(src_point))
    used = set(dont_use)

    while len(queue) > 0:

        path = queue.pop()

        if path[0] == dst_point:
            result = []
            while path is not None:
                point, path = path
                result.append(point)

            return result

        x, y = path[0]
        for px, py in nearest:
            nx = x + px
            ny = y + py
            if field[ny][nx] != Cell.Wall:
                point = (nx, ny)
                if not (point in used):
                    queue.push((point, path), volume(point))
                    used.add(point)

    return []

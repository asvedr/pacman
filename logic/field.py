import enum
from functools import reduce

class Cell(enum.Enum):
    Empty = 0
    Wall = 1
    RGhost = 2
    BGhost = 3
    YGhost = 4
    PGhost = 5
    Pacman = 6
    Dot = 7

class Field(object):

    cell_map = {'#': Cell.Wall,
                ' ': Cell.Empty,
                'P': Cell.Pacman,
                'r': Cell.RGhost,
                'b': Cell.BGhost,
                'y': Cell.YGhost,
                'p': Cell.PGhost,
                '.': Cell.Dot}
                
    __slots__ = 'data', 'dot_count', 'width', 'height'
                
    def __init__(self, path):
        
        with open(path, 'rt') as handler:
            # creating
            lines = handler.read().split('\n')
    
        lines = list(filter(''.__ne__, lines))
        # checking
        assert len(lines) > 0
        ethalon = len(lines[0])
        assert all(map(lambda line: len(line) == ethalon, lines))

        cell_map = self.cell_map
        
        def make_line(line):
            return list(map(cell_map.get, line))

        self.data = list(map(make_line, lines))
        dot_count = 0
        for line in self.data:
            for cell in line:
                if cell == Cell.Dot:
                    dot_count += 1
        self.dot_count = dot_count
        self.height = len(self.data)
        self.width = len(self.data[0])

    def __repr__(self):

        back_map = {val:key for key, val in self.cell_map.items()}
    
        acc = '%s\n' % self.dot_count
        out = [''.join([back_map[cell] for cell in line]) for line in self.data]
        return acc + '\n'.join(out)

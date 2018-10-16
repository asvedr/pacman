import threading as th
import time
from logic.field import Field, Cell
from logic.pers import Pers, color_list
import multiprocessing as mp
from logic.logger import prepare_logger
import logging


SLEEP_TIME = 0.1

class _LogicProcess(object):
    
    __slots__ = ('ghosts', 'pacman', 'field',
                 'user_vector', '_stop_flag',
                 'previous_time', 'diff_time',
                 'eated_dots', 'namespace',
                 'logger')
    user_vector_none = (0, 0)

    def __init__(self, field, namespace):
        self.namespace = namespace
        self.field = field
        self.pacman = None
        self.ghosts = []
        self.user_vector = self.user_vector_none
        self._stop_flag = False
        self.eated_dots = []
        self.previous_time = None
        prepare_logger()
        self.logger = logging.getLogger('pacman')
        
        perses = {Cell.Pacman: Pers.pacman,
                  Cell.RGhost: Pers.red,
                  Cell.BGhost: Pers.blue,
                  Cell.YGhost: Pers.yello,
                  Cell.PGhost: Pers.pink}
        
        for y in range(field.height):
            for x in range(field.width):
                cell = field.data[y][x]
                if cell in perses:
                    pers = perses[cell](x, y)
                    if pers.is_pacman:
                        self.pacman = pers
                    else:
                        self.ghosts.append(pers)
                    field.data[y][x] = Cell.Empty

        # self._mainloop()
                    
    def stop(self):
        self._stop_flag = True
    
    # def run(self):
        # self.previous_time = time.time()
        # threading.Thread(target=self._mainloop).start()

    def tick(self):
        now = time.time()
        self.diff_time = now - self.previous_time if self.previous_time else 0
        self.previous_time = now
        uv = self.namespace.user_vector
        if uv is not None:
            self.user_vector = uv
        self.pacman.move(self)
        self.user_vector = self.user_vector_none
        ghosts_state = []
        for ghost in self.ghosts:
            ghost.move(self)
            ghosts_state.append((ghost.x, ghost.y, ghost.color))
        ns = self.namespace
        ns.pacman = (self.pacman.x, self.pacman.y)
        ns.ghosts = ghosts_state
        time.sleep(SLEEP_TIME)

    def pacman_killed(self):
        print('pacman killed')

    def mainloop_mp(self):
        while not self._stop_flag:
            self.tick()

    def mainloop_th(self):
        while not self._stop_flag:
            self.tick()
            time.sleep(0.001)


def _build_n_run_mp(field, namespace):
    _LogicProcess(field, namespace).mainloop_mp()

def _build_n_run_th(field, namespace):
    _LogicProcess(field, namespace).mainloop_th()

class _State(object):
    
    __slots__ = 'ghosts', 'pacman', 'eated_dots'

    def __init__(self, pacman, ghosts, eated_dots):
        self.pacman = pacman
        self.ghosts = ghosts
        self.eated_dots = eated_dots


class _NameSpacePlug:
    def __init__(self):
        self.ghosts = []
        self.pacman = None
        self.eated_dots = []
        self.user_vector = None


class Logic(object):

    __mode = 'MP'

    @classmethod
    def set_thread_mode(cls):
        cls.__mode = 'TH'

    @classmethod
    def set_multiprocess_mode(cls):
        cls.__mode = 'MP'

    @classmethod
    def load_file(cls, path):
        field = Field(path)
        if cls.__mode == 'MP':
            namespace, manager = cls._prepare_mp_manager()
            proc = mp.Process(target=_build_n_run_mp, args=(field, namespace))
            return cls(manager, namespace, proc, field)
        else:
            namespace = _NameSpacePlug()
            proc = th.Thread(target=_build_n_run_th, args=(field, namespace))
            return cls(None, namespace, proc, field)
    
    @classmethod
    def start_process(cls, field):
        if cls.__mode == 'MP':
            namespace, manager = cls._prepare_mp_manager()
            proc = mp.Process(target=_build_n_run_mp, args=(field, namespace))
            return cls(manager, namespace, proc, field)
        else:
            namespace = _NameSpacePlug()
            proc = th.Thread(target=_build_n_run_th, args=(field, namespace))
            return cls(None, namespace, proc, field)

    @staticmethod
    def _prepare_mp_manager():
        manager = mp.Manager()
        ns = manager.Namespace()
        ns.ghosts = []
        ns.pacman = None
        ns.eated_dots = []
        ns.user_vector = None
        return (ns, manager)

    def __init__(self, manager, namespace, proc, field):
        proc.start()
        self.manager = manager
        self.namespace = namespace
        self.proc = proc
        self.field = field

    def get_state(self):
        ns = self.namespace
        ghosts = ns.ghosts
        pacman = ns.pacman
        dots = ns.eated_dots
        ghosts = [(x,y,color_list[c]) for (x,y,c) in ghosts]
        return (pacman, ghosts, dots)

    def move_pacman(self, vector):
        print('MOVE PACMAN ', vector)
        self.namespace.user_vector = vector

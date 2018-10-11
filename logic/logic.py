import threading
import time
from logic.field import Field, Cell
from logic.pers import Pers

class Logic(object):
	
	__slots__ = 'ghosts', 'pacman', 'field', 'user_vector', '_stop_flag'
	user_vector_none = (0, 0)
	
	@classmethod
	def load_file(cls, path):
		return cls(Field(path))
	
	def __init__(self, field):
		self.field = field
		self.pacman = None
		self.ghosts = []
		self.user_vector = self.user_vector_none
		self._stop_flag = False
		
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
					
	def stop(self):
		self._stop_flag = True
	
	def run(self):
		threading.Thread(target=self._mainloop).start()

	def _mainloop(self):
		while not self._stop_flag:
			self.pacman.move(self)
			self.user_vector = self.user_vector_none
			for ghost in self.ghosts:
				ghost.move(self)
			time.sleep(1)
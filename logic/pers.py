
class Pers(object):
	
	@classmethod
	def pacman(cls, x, y):
		cls(x, y, pacman_algorithm)

	@classmethod
	def red(cls, x, y):
		cls(x, y, red_algorithm)

	@classmethod
	def yello(cls, x, y):
		cls(x, y, yello_algorithm)

	@classmethod
	def pink(cls, x, y):
		cls(x, y, pink_algorithm)

	@classmethod
	def blue(cls, x, y):
		cls(x, y, blue_algorithm)
		
	def __init__(self, x, y, algorithm):
		self.x = x
		self.y = y
		self.algorithm = algorithm
	
	def move(self, logic):
		self.algorithm(logic)
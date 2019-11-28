class BoardContainer:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.board = [['_'] * cols for i in range(rows)]
		self.openSpaces = rows*cols
		self.depthOfEachColumn = [rows] * cols
		self.AIcheckerLocations = []
		self.playerCheckerLocations =[]

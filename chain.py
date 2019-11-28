class Chain:
	def __init__(self, start, end, orientation, potential):
		self.start = start
		self.end = end
		self.orientation = orientation
		self.potential = potential	

	def getSize(self):
		return max(abs(self.start.row - self.end.row), abs(self.start.col - self.end.col)) + 1

	def __str__(self):
		s = "CHAIN AT: Start: " + str(self.start) + " End: " + str(self.end) + " Orientation: " + str(self.orientation) + " Size: " + str(self.getSize())
		return s

	def getID(self):
		return (str(self))

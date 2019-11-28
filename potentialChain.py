class PotentialChain:
	def __init__(self, start, end, orientation, emptySpaces, checkeredSpaces):
		self.start = start
		self.end = end
		self.orientation = orientation
		self.emptySpaces = 	emptySpaces
		self.checkeredSpaces = checkeredSpaces

	def getSize(self):
		return max(abs(self.start.row - self.end.row), abs(self.start.col - self.end.col)) + 1

	def __str__(self):
		s = "POTENTIAL CHAIN AT: Start: " + str(self.start) + " End: " + str(self.end) + " Orientation: " + str(self.orientation) + " emptySpaces " + str(self.emptySpaces) + " checkeredSpaces " + str(self.checkeredSpaces)
		return s

	def getID(self):
		return (str(self))

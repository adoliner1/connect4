class Node:
	def __init__(self, boardContainer, score, parent, children, move):
		self.boardContainer = boardContainer
		self.score = score
		self.parent = parent
		self.children = children
		self.move = move

	def __str__(self):
		s = "Node with score: " + str(self.score) + " Children: " + str(self.children) + " Parent: " + str(self.parent) + " Move: " + str(self.move)
		return s
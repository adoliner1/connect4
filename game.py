from coordinate import *
from boardContainer import *
from chain import *
from potentialChain import *
from node import *
import copy
import pdb

orientations = {'vertical': ("south", "north"), 'horizontal': ("west", "east"), 'NW-SE': ("southEast", "northWest"), 'NE-SW': ("southWest", "northEast")}
directions = {"northWest":(-1,-1), "southEast":(1,1), "southWest":(1,-1), "northEast":(-1,1), "north":(-1,0), "south":(1,0), "east":(0,1), "west":(0,-1)}

def playGame(cols, rows, chainSizeToWin):
	#buildBoard and initialize game variables
	boardContainer = BoardContainer(rows, cols)
	longestPlayerChain = 0
	longestAIChain = 0
	isPlayer = True
	printBoard(boardContainer.board, "")
	while (boardContainer.openSpaces != 0 and longestPlayerChain < chainSizeToWin and longestAIChain < chainSizeToWin):
		playersChecker = 'X' if isPlayer else 'O'
		if not isPlayer:
			root = Node(boardContainer, None, None, [], None)
			buildTree(root, isPlayer, 0, 4, chainSizeToWin)
			proprogateScores(root, isPlayer)
			bestChild = getMinScoreNodeFromChildren(root.children)
			move = bestChild.move
		else:
			print "Make a move by choosing a column number from 0 to " + str(cols-1)
			try:
				moveColumn = int(input())
			except Exception:
				print "Choose a column number from 0 to " + str(cols-1)
				continue
			if(moveColumn < 0 or moveColumn > (cols - 1)):
				print("Out of range, try again")
				continue
			moveRow = boardContainer.depthOfEachColumn[moveColumn] - 1
			move = Coordinate(moveRow, moveColumn)
			if(move.row == -1):
				print("Column full, try again")
				continue

		print("\n Placing in column " + str(move.col))
		boardContainer.board[move.row][move.col] = playersChecker
		boardContainer.playerCheckerLocations.append(move) if isPlayer else boardContainer.AIcheckerLocations.append(move)
		boardContainer.openSpaces -= 1	
		boardContainer.depthOfEachColumn[move.col] -= 1
		printBoard(boardContainer.board, "")
		allChains = getChainsFromBoard(boardContainer, isPlayer, chainSizeToWin)

		if isPlayer:
			longestPlayerChain = getMaxChainSize(allChains)
		else:
			longestAIChain = getMaxChainSize(allChains)
		isPlayer = not isPlayer

def evaluateBoard(boardContainer, chainSizeToWin):
	chains = getChainsFromBoard(boardContainer, True, chainSizeToWin)
	opponentChains = getChainsFromBoard(boardContainer, False, chainSizeToWin)
	score = 0
	score += getScoreFromChains(boardContainer, chains)
	score -= getScoreFromChains(boardContainer, opponentChains)
	return score

def getScoreFromChains(boardContainer, chains):
	score = 0
	for key in chains:
		chain = chains[key]
		if chain.potential or chain.getSize() >= 4:
			if chain.getSize() == 1:
				score += 1
			elif chain.getSize() == 2:
				score += 5
				if len(chain.potential.keys()) >= 2:
					score += 50
			elif chain.getSize() == 3:
				score += 200
				if len(chain.potential.keys()) == 2:
					#potentialEndsOnLowestRow = True
					#for key in chain.potential.keys():
					#	potentialChain = chain.potential[key]
					#	if potentialChain.start.row == boardContainer.depthOfEachColumn[potentialChain.start.col] and potentialChain.end.row == boardContainer.depthOfEachColumn[potentialChain.start.col]
					score += 300
			else:
				score += 9999

			for key in chain.potential.keys():	
				score += 3
	return score

def buildTree(node, isPlayer, currentDepth, maxDepth, chainSizeToWin):
	if currentDepth == maxDepth or node.boardContainer.openSpaces <= 0:
		node.score = evaluateBoard(node.boardContainer, chainSizeToWin)
	else:
		chains = getChainsFromBoard(node.boardContainer, not isPlayer, chainSizeToWin)
		maxChainSize = getMaxChainSize(chains)
		if (maxChainSize >= chainSizeToWin):
			node.score = evaluateBoard(node.boardContainer, chainSizeToWin)
		else:
			playersChecker = 'X' if isPlayer else 'O'
			for col in range(node.boardContainer.cols):
				newBoardContainer = copy.deepcopy(node.boardContainer)
				moveRow = newBoardContainer.depthOfEachColumn[col] - 1
				if moveRow != -1:
					move = Coordinate(moveRow, col)
					newBoardContainer.board[moveRow][col] = playersChecker
					newBoardContainer.playerCheckerLocations.append(move) if isPlayer else newBoardContainer.AIcheckerLocations.append(move)
					newBoardContainer.openSpaces -= 1
					newBoardContainer.depthOfEachColumn[move.col] -= 1
					child = Node(newBoardContainer, None, node, [], move)
					node.children.append(child)
					buildTree(child, not isPlayer, currentDepth+1, maxDepth, chainSizeToWin)

def proprogateScores(node, isPlayer):
	if node.score == None:
		for child in node.children:
			if child.score == None:
				proprogateScores(child, not isPlayer)
		if isPlayer:
			node.score = getMaxScoreNodeFromChildren(node.children).score
		else:
			node.score = getMinScoreNodeFromChildren(node.children).score

def getMaxScoreNodeFromChildren(children):
	maxChildNode = children[0]
	maxScore = maxChildNode.score
	for child in children:
		if child.score > maxScore:
			maxChildNode = child
			maxScore = child.score
	return maxChildNode

def getMinScoreNodeFromChildren(children):
	minChildNode = children[0]
	minScore = minChildNode.score
	for child in children:
		if child.score < minScore:
			minChildNode = child
			minScore = child.score
	return minChildNode

def getChainsFromBoard(boardContainer, isPlayer, chainSizeToWin):
	locations = boardContainer.playerCheckerLocations if isPlayer else boardContainer.AIcheckerLocations
	allChains = {}
	for checkerLocation in locations:
		for orientation in orientations:
			chain = getChainFromLocationInOrientation(boardContainer, isPlayer, orientation, checkerLocation)
			updatePotentialsForChain(boardContainer, isPlayer, chain, chainSizeToWin)
			chainID = chain.getID()
			if chainID not in allChains:
				allChains[chainID] = chain	
	return allChains

def getMaxChainSize(chains):
	size = 0
	for chainID in chains:
		size = max(size, chains[chainID].getSize())
	return size

def getChainFromLocationInOrientation(boardContainer, isPlayer, orientation, location):
	board = boardContainer.board	
	rows = len(board)
	cols = len(board[0])
	playersChecker = 'X' if isPlayer else 'O'
	opponentsChecker = 'O' if isPlayer else 'X'
	direction = orientations[orientation][0]
	rowMovement = directions[direction][0]
	colMovement = directions[direction][1]

	#run through twice to check both directions
	for i in range(2):
		if i == 1:
			#switch direction
			rowMovement = rowMovement*-1
			colMovement = colMovement*-1

		r = location.row + rowMovement
		c = location.col + colMovement
		while (r < rows and r >= 0 and c >= 0 and c < cols):
			if (board[r][c] == playersChecker):
				r += rowMovement
				c += colMovement		
			else:
				break
		if i == 0:
			start = Coordinate(r-rowMovement,c-colMovement)		
		else:
			end = Coordinate(r-rowMovement,c-colMovement)

	chain = Chain(start, end, orientation, {})
	return chain

def updatePotentialsForChain(boardContainer, isPlayer, chain, chainSizeToWin):
	board = boardContainer.board
	rows = len(board)
	cols = len(board[0])
	playersChecker = 'X' if isPlayer else 'O'
	opponentsChecker = 'O' if isPlayer else 'X'
	spacesToCheck = chainSizeToWin - chain.getSize()
	currentWindowSize = chain.getSize()

	startDirection = orientations[chain.orientation][0]
	rowMovement = directions[startDirection][0]
	colMovement = directions[startDirection][1]

	#sliding window of size chainSizeToWin starting at start of potential and going to end potential

	#if windowSize doesn't reach chainSizeToWin, we have no potential chains to make. So we need to go to as far as we can in start,
	#which if all the squares are free means our window will start at chain.start + row.movement*spacesToCheck, if not, we try to advance
	#from chain.end to get up to chainSizeToWin

	currentNumberOfEmptySpacesInWindow = 0
	currentNumberOfFriendlyCheckersInWindow = chain.getSize()

	r = chain.start.row + rowMovement
	c = chain.start.col + colMovement


	#travel in startDirection from the start of the chain, keeping track of window size as we go
	while (r < rows and r >= 0 and c >= 0 and c < cols and currentWindowSize < chainSizeToWin):
		if (board[r][c] == '_'):
			currentWindowSize += 1
			currentNumberOfEmptySpacesInWindow += 1
		elif (board[r][c] == playersChecker):
			currentWindowSize += 1
			currentNumberOfFriendlyCheckersInWindow += 1
		else:
			break
		r += rowMovement
		c += colMovement

	potentialChainStart = Coordinate(r-rowMovement,c-colMovement)

	#switch directions of our row/col movers
	rowMovement = rowMovement*-1
	colMovement = colMovement*-1

	#travel in the other direction to get our initial chain end
	r = chain.end.row + rowMovement
	c = chain.end.col + colMovement

	while (r < rows and r >= 0 and c >= 0 and c < cols and currentWindowSize < chainSizeToWin):
		if (board[r][c] == '_'):
			currentWindowSize += 1
			currentNumberOfEmptySpacesInWindow += 1
		elif (board[r][c] == playersChecker):
			currentWindowSize += 1
			currentNumberOfFriendlyCheckersInWindow += 1
		else:
			break
		r += rowMovement
		c += colMovement

	potentialChainEnd = Coordinate(r-rowMovement, c-colMovement)

	#check if theres enough space for a potential chain
	if currentWindowSize == chainSizeToWin:

		potentialChain = PotentialChain(copy.deepcopy(potentialChainStart), copy.deepcopy(potentialChainEnd), chain.orientation, currentNumberOfEmptySpacesInWindow, currentNumberOfFriendlyCheckersInWindow)
		chainID = potentialChain.getID()
		if chainID not in chain.potential:
			chain.potential[chainID] = potentialChain

		while not (potentialChainStart.row == chain.start.row and potentialChainStart.col == chain.start.col):
			if board[potentialChainStart.row][potentialChainStart.col] == '_':
				currentNumberOfEmptySpacesInWindow -= 1
			else:
				currentNumberOfFriendlyCheckersInWindow -= 1

			potentialChainStart.row += rowMovement
			potentialChainEnd.row += rowMovement
			potentialChainStart.col += colMovement
			potentialChainEnd.col += colMovement

			if not (potentialChainEnd.row < rows and potentialChainEnd.row >= 0 and potentialChainEnd.col < cols and potentialChainEnd.col >= 0):
				break
			if board[potentialChainEnd.row][potentialChainEnd.col] == '_':
				currentNumberOfEmptySpacesInWindow += 1
			elif board[potentialChainEnd.row][potentialChainEnd.col] == playersChecker:
				currentNumberOfFriendlyCheckersInWindow += 1
			else:
				break

			potentialChain = PotentialChain(copy.deepcopy(potentialChainStart), copy.deepcopy(potentialChainEnd), chain.orientation, currentNumberOfEmptySpacesInWindow, currentNumberOfFriendlyCheckersInWindow)
			chainID = potentialChain.getID()
			if chainID not in chain.potential:
				chain.potential[chainID] = potentialChain

def printBoard(board, indent):
	i = 0
	for row in board:
		print indent + (str(i) + "  " + '  '.join([str(elem) for elem in row]))
		i += 1
	print indent + "   0  1  2  3  4  5  6"
	print indent + "----------------------"

def printTree(node, indent):
	print indent + str(node.score)
	printBoard(node.boardContainer.board, indent)
	for child in node.children:
		printTree(child, indent + "    ")

playGame(7, 6, 4)
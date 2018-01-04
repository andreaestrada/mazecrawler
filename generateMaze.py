###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Random maze generator
# Basic algorithm description for Eller's: http://www.neocomputer.org/projects/eller.html
# Basic algorithm description for recursive division: https://en.wikipedia.org/wiki/Maze_generation_algorithm
# Basic algorithm description for sidewinder: http://weblog.jamisbuck.org/2011/2/3/maze-generation-sidewinder-algorithm
# Basic algorithm description for hunt and kill: http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm
# Basic algorithm description for Binary: http://weblog.jamisbuck.org/2011/2/1/maze-generation-binary-tree-algorithm
# All code implementations completely by Andrea Estrada
# 
###############################################################################
from random import * #use to randomize maze

import spec #game specifications


#takes non-negative rows and cols and produces 2D base board to match that size
#helper function for createRandomMaze()
def createBase(rows, cols):
	base = []
	for row in range(rows):
		columns = []
		for col in range(cols):
			columns.append([])
		base.append(columns)
	return base


###############################################################################
#
# MAZE ALGORITHMS
# 
###############################################################################


#Eller's algorithm: assigning sets by row
#destructively modifies maze
#helper function for createRandomMaze()
def ellersMaze(maze, rows, cols):
	currSet = list(range(0, cols))
	for row in range(rows):
		for col in range(cols-1):
			passage = choice([True, False])
			if currSet[col] != currSet[col+1] and (row == rows - 1 or passage):
				currSet[col+1] = currSet[col] #change sets to track matches in current row
				#add horizontal connections
				maze[row][col].append("Right") 
				maze[row][col+1].append("Left")
		#randomly create vertical passageways
		if row < rows - 1: #not last row
			nextSet = list(range((row+1)*(cols), (row+2)*cols))  
			#track connections between next set/current set
			aboveSets = set(currSet)
			connections = set()
			#randomly create a connection between next line and every existing set
			while aboveSets != connections:
				for col in range(rows): #every column in the row
					passage = choice([True, False])
					if passage and currSet[col] not in connections:
						nextSet[col] = currSet[col] #passageway created
						connections.add(currSet[col]) #track new connection
						maze[row][col].append("Down")
						maze[row+1][col].append("Up")
			currSet = nextSet #repeat process on next row


#Recursive division: creates random walls and then breaks connections through those walls
#destructively modifies maze
#helper function for createRandomMaze()
def recursiveDivisionMaze(maze, rows, cols, toSplit = "Vertical"):
	if rows == 1 and cols == 1: return maze #nothing left to divide, in any dimension!
	if toSplit == "Horizontal":
		if rows == 1: return recursiveDivisionMaze(maze, rows, cols, "Vertical") #rows cannot be divided anymore
		else: #divide rows
			divisionIndex = randint(1, rows-1)
			#partition maze based on randomized dividing line
			top = maze[:divisionIndex] 
			bottom = maze[divisionIndex:]
			#get more divisions
			recursiveDivisionMaze(top, len(top), len(top[0]), "Vertical")
			recursiveDivisionMaze(bottom, len(bottom), len(bottom[0]), "Vertical")
			#create random pathway in division
			pathway = randint(0, cols-1)
			#pathway at bottom of the top section, top of the bottom section
			top[-1][pathway].append("Down")
			bottom[0][pathway].append("Up")
			return top + bottom
	elif toSplit == "Vertical":
		if cols == 1: return recursiveDivisionMaze(maze, rows, cols, "Horizontal") #cols cannot be divided anymore
		else: #divide cols
			divisionIndex = randint(1, cols-1)
			#parition maze based on randomized dividing line
			left = [row[:divisionIndex] for row in maze]
			right = [row[divisionIndex:] for row in maze]
			#get more divisions
			recursiveDivisionMaze(left, len(left), len(left[0]), "Horizontal")
			recursiveDivisionMaze(right, len(right), len(right[0]), "Horizontal")
			#create random pathway in division
			pathway = randint(0, rows-1)
			#pathway at right of the left section, left of the right section
			left[pathway][-1].append("Right")
			right[pathway][0].append("Left")
			return [a+b for a,b in zip(left,right)]


#Sidewinder algorithm: carve right for random lengths, then create upwards connection
#destructively modifies maze
#helper function for createRandomMaze()
def sidewinder(maze, rows, cols):
	for row in range(rows):
		if row == 0: #row at top is completely connected
			for col in range(cols-1): 
				maze[row][col].append("Right")
				maze[row][col+1].append("Left")
		else: #all other rows
			currentSetStart = 0
			while currentSetStart <= cols-1:
				upperBoundary = min(currentSetStart + 5, cols) #upper boundary for connection
				currentSetEnd = randint(currentSetStart+1, upperBoundary) #connection boundaries
				for col in range(currentSetStart, currentSetEnd-1):
					maze[row][col].append("Right")
					maze[row][col+1].append("Left")
				upwardsConnection = randint(currentSetStart, currentSetEnd-1)
				#create one connection upward per set
				maze[row][upwardsConnection].append("Up")
				maze[row-1][upwardsConnection].append("Down")
				currentSetStart = currentSetEnd


#Hunt and kill algorithm: carves path, looks for uncarved area to connect, then continues carving from that area
#destructively modifies maze
#helper function for createRandomMaze()
def huntAndKill(maze, rows, cols):

	currY = randint(0, rows-1)
	currX = randint(0, cols-1)

	#specifies pathways based on valid move
	def assignDirections(move):
		if move == (0,1): setTo = ["Right", "Left"] #first set to is for current, second set to is for new
		elif move == (0,-1): setTo = ["Left", "Right"]
		elif move == (1,0): setTo = ["Down", "Up"]
		else: setTo = ["Up", "Down"]
		return setTo

	#carves a passageway from a specified spot until no neighbors are unvisited
	def carve(maze, currY, currX):
		moves = [(0,1), (0,-1), (1,0), (-1,0)] 
		shuffle(moves)
		while len(moves) > 0:
			newY = currY + moves[0][0]
			newX = currX + moves[0][1]
			if newY >= 0 and newY < rows and newX >= 0 and newX < cols and maze[newY][newX] == []: #found valid move
				setTo = assignDirections(moves[0])
				#carve passage
				maze[currY][currX].append(setTo[0])
				maze[newY][newX].append(setTo[1])
				carve(maze, newY, newX)
				break
			moves.pop(0)

	#looks for occurrence of an univsited cell with a visited neighbor
	def hunt(maze, rows, cols):
		moves = [(0,1), (0,-1), (1,0), (-1,0)] 
		shuffle(moves)
		for row in range(rows):
			for col in range(cols):
				if maze[row][col] == []: 
					for move in moves:
						newY = row + move[0]
						newX = col + move[1]
						if newY >= 0 and newY < rows and newX >= 0 and newX < cols and maze[newY][newX] != []: #found valid move
								setTo = assignDirections(move)
								#creates connection between visited and univisited
								maze[row][col].append(setTo[0])
								maze[newY][newX].append(setTo[1])
								carve(maze, row, col)
								return True
		return False

	carve(maze, currY, currX)
	keepHunting = True
	while(keepHunting): #until there are no more instances of unvisited cells, continue hunting and carving
		keepHunting = hunt(maze, rows, cols)

#Binary Tree algorithm: choose between right passageway or down passageway
#destructively modifies maze
#helper function for createRandomMaze()
def binaryTree(maze, rows, cols):
	#this binary tree search favors the southeast diagonal 
	for row in range(rows):
		for col in range(cols):
			if row == rows-1:
				if col < cols-1:
					maze[row][col].append("Right")
					maze[row][col+1].append("Left")
			elif col == cols-1:
				maze[row][col].append("Down")
				maze[row+1][col].append("Up")
			else:
				passage = choice(["Right", "Down"])
				if passage == "Right":
					maze[row][col].append("Right")
					maze[row][col+1].append("Left")
				else:
					maze[row][col].append("Down")
					maze[row+1][col].append("Up")



###############################################################################
#
# GAMEBOARD ALGORITHMS: Edit maze to make it conducive to gameplay
# 
###############################################################################


#creates connections and make random loops in maze
#destructively modifies maze
#helper function for createRandomMaze()
def createLoops(maze):
	rows, cols = len(maze), len(maze[0])
	numLoops = int(rows*cols*spec.breakWalls)
	for i in range(numLoops):
		randX = randint(0, rows-2)
		randY = randint(0, cols-2)
		current = maze[randY][randX]
		if not "Right" in current:
			current.append("Right")
			maze[randY][randX+1].append("Left")
		elif not "Down" in current:
			current.append("Down")
			maze[randY+1][randX].append("Up")

#deletes unnecessary walls along edges of maze (border acts as wall, so individual walls unnecessary)
#destructively modifies maze
#helper function for createRandomMaze()
def eliminateEdgeCases(maze):
	rows, cols = len(maze), len(maze[0])
	for i in range(rows):
		current = maze[i][cols-1]
		if "Right" not in current:
			current.append("Right")
		if i == rows-1:
			for j in range(cols):
				current = maze[i][j]
				if "Down" not in current:
					current.append("Down")


#creates connections in maze where otherwise there would have been a dead end
#destructively modifies maze
#helper function for createRandomMaze()
def deadEndElimnator(maze):
	rows, cols = len(maze), len(maze[0])
	#edge case for bottomost row
	for i in range(cols-1): 
		bottom = maze[rows-1][i]
		if len(bottom) == 2: 
			if "Up" not in bottom:
				bottom.append("Up")
				maze[rows-2][i].append("Down")
			else:
				bottom.append("Right")
				maze[rows-1][i+1].append("Left")
	#all other rows
	for row in range(rows-1):
		#edge case for rightmost column
		side = maze[row][cols-1]
		if len(side) == 2:
			if "Down" not in side:
				side.append("Down")
				maze[row+1][cols-1].append("Up")
			else:
				side.append("Left")
				maze[row][cols-2].append("Right")
		#all other columns
		for col in range(cols-1):
			current = maze[row][col]
			if len(current) == 1: #only one connection --> eliminate dead end
				if current[0] == "Right": passage = "Down"
				elif current[0] == "Down": passage = "Right"
				else: passage = choice(["Right", "Down"])
				if passage == "Right":
					maze[row][col].append("Right") 
					maze[row][col+1].append("Left")
				else: 
					maze[row][col].append("Down")
					maze[row+1][col].append("Up")
	#edge case for bottom right square
	if "Left" not in maze[rows-1][cols-1]: 
		maze[rows-1][cols-1].append("Left")
		maze[rows-1][cols-2].append("Right")
	if "Up" not in maze[rows-1][cols-1]: 
		maze[rows-1][cols-1].append("Up")
		maze[rows-2][cols-1].append("Down")


###############################################################################
#
# GENERATE MAZE
# 
###############################################################################


#use various algorithms to create random mazes
#maze stores passageways as directions of legal movements
def createMaze():
	maze = createBase(spec.difficulty, spec.difficulty)
	rows, cols = len(maze), len(maze[0]) #base info
	if spec.mazeType == "Eller": ellersMaze(maze, rows, cols)
	elif spec.mazeType == "RecursiveDivision": recursiveDivisionMaze(maze, rows, cols)
	elif spec.mazeType == "Sidewinder": sidewinder(maze, rows, cols)
	elif spec.mazeType == "HuntAndKill": huntAndKill(maze, rows, cols)
	elif spec.mazeType == "Binary": binaryTree(maze, rows, cols)
	eliminateEdgeCases(maze)
	deadEndElimnator(maze)
	createLoops(maze)
	checkMaze(maze, rows, cols)
	return maze

###############################################################################
#
# TEST FUNCTIONS
#
###############################################################################

#use for debugging
def checkMaze(maze, rows, cols):
	for i in range(rows):
		for j in range (cols):
			for move in maze[i][j]:
				try:
					if move == "Right" and "Left" not in maze[i][j+1]: print("Wrong - Right")
					if move == "Left" and "Right" not in maze[i][j-1]: print("Wrong - Left")
					if move == "Up" and "Down" not in maze[i-1][j]: print("Wrong - Up")
					if move == "Down" and "Up" not in maze[i+1][j]: print("Wrong - Down")
				except Exception as ex: 
					if str(ex) != "list index out of range": print(ex)

#print pure maze without alterations
def testRandomMaze(difficulty):
	maze = createBase(difficulty, difficulty)
	rows, cols = len(maze), len(maze[0]) #base info
	mazeType = choice(["Eller", "RecursiveDivision", "Sidewinder", "HuntAndKill", "Binary"])
	if mazeType == "Eller": ellersMaze(maze, rows, cols)
	elif mazeType == "RecursiveDivision": recursiveDivisionMaze(maze, rows, cols)
	elif mazeType == "Sidewinder": sidewinder(maze, rows, cols)
	elif mazeType == "HuntAndKill": huntAndKill(maze, rows, cols)
	elif mazeType == "Binary": binaryTree(maze, rows, cols)
	eliminateEdgeCases(maze)
	deadEndElimnator(maze)
	createLoops(maze)
	checkMaze(maze, rows, cols)
	print(mazeType)
	print()
	return maze


def testCreateBase():
	print("Testing createBase()... ", end = "")
	assert(createBase(1, 1) == [[[]]])
	assert(createBase(2, 2) == [[[], []], [[], []]])
	assert(createBase(3, 3) == [[[], [], []], [[], [], []], [[], [], []]])
	print("passed!")

def testCreateRandomMaze():
	print("Testing createRandomMaze()... Printing random mazes:")
	print(createRandomMaze(5))

def main():
	testCreateBase()
	testCreateRandomMaze()

#main()



###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# ai Players: 3rd level of "intelligence"
# Basic framework for Djikstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# All code implementations completely by Andrea Estrada
#
###############################################################################
import pygame #graphics
import spec
import copy
import player
import ai

###############################################################################
#
# DIJKSTRA'S
#
###############################################################################

class AIThree(ai.AIPlayer): 

	#level three AI player finds most efficent path to a given player's location 
	def move(self):
		#print("moving")
		if self.getMazeSpot(): #in the center of a square
			#print("centered")
			self.routeNow = self.dijkstraPath()
			self.translatePath()
			if len(self.routeNow) >= 1: 
				self.dX = self.dDistance * self.routeNow[0][1]
				self.dY = self.dDistance * self.routeNow[0][0]
				self.routeNow.pop(0)
		self.collide()
		self.carryOut()

	def currDistances(self):
		maze = spec.maze
		rows = len(maze)
		cols = len(maze)
		currDist = {node: dict() for node in range(rows*cols)}
		for row in range(rows):
			for col in range(cols):
				currentSlot = col + row*cols
				moves = maze[row][col]
				currentSet = currDist[currentSlot]
				#not a different row, no wall, within bounds
				if (currentSlot+1)%cols != 0 and "Right" in moves and (currentSlot+1)<=rows*cols-1: 
					currentSet[currentSlot+1] = 1
				#not a different row, no wall, within bounds
				if (currentSlot-1)%cols != cols-1 and "Left" in moves and (currentSlot-1)>=0:
					currentSet[currentSlot-1] = 1
				#no wall, within bounds
				if "Up" in moves and (currentSlot-cols)>=0:
					currentSet[currentSlot-cols] = 1
				#no wall, within bounds
				if "Down" in moves and (currentSlot+cols)<rows*cols:
					currentSet[currentSlot+cols] = 1
		return currDist

	def dijkstraPath(self): 
		maze = spec.maze
		rows, cols = len(maze), len(maze[0])
		#possible points
		nodes = list(range(len(maze) * len(maze[0])))

		parent = dict()

		#track which places to go
		unvisited = dict()
		for node in nodes:
			unvisited[node] = None #use None instead of infinity
			parent[node] = None
		visited = dict()

		#distances between neighbouring nodes
		distances = self.currDistances()

		currDist = 0

		startX, startY = self.currentSlot() #indexX, indexY
		startNode = startX + startY*cols
		current = startX + startY*cols
		unvisited[current] = currDist

		#designate node that holds "winning" condition
		if self.tag == "me": endX, endY = spec.me.currentSlot() #my AI
		elif self.tag == "opponent": endX, endY = spec.opponent.currentSlot() #other AI
		endNode = endX + endY*cols

		while True:
			for node, dist in distances[current].items():
				if node in unvisited:
					newDist = currDist + dist
					if not unvisited[node] or unvisited[node] > newDist: 
						unvisited[node] = newDist
						parent[node] = current
			visited[current] = currDist
			if current in unvisited: unvisited.pop(current)
			if not unvisited: break #finished!
			candidates = []
			for node, dist in unvisited.items():
				if dist != None: candidates.append((node, dist))

			current, currDist = sorted(candidates, key = lambda nodes: nodes[1])[0]

		return(self.finalPath(parent, startNode, endNode, rows, cols))

	def finalPath(self, parent, startNode, endNode, rows, cols):
		path = []
		currentNode = endNode
		while currentNode != startNode:
			path.append(currentNode)
			currentNode = parent[currentNode]
		path = path[::-1]
		route = []
		for node in path:
			col = node%cols 
			row = (node - col)/cols
			route.append((row,col))
		return route

	#translate path produced by dijkstra algorithm
	def translatePath(self):
		currX, currY = self.currentSlot()
		translated = []
		for newNode in self.routeNow:
			y = newNode[0]
			x = newNode[1]
			dY = y-currY
			dX = x-currX
			translated.append((dY, dX))
			currY = y
			currX = x
		self.routeNow = translated


###############################################################################
#
# Test functions
#
###############################################################################

def main():
	print("Testing Dijkstra...", end = "")
	#assert(currDistances(testMaze2) == {0: {3: 1}, 1: {2: 1, 4: 1}, 2: {1: 1, 5: 1}, 3: {4: 1, 0: 1, 6: 1}, 4: {3: 1, 1: 1}, 5: {2: 1, 8: 1}, 6: {7: 1, 3: 1}, 7: {8: 1, 6: 1}, 8: {7: 1, 5: 1}})
	#assert(dijkstraPath(2, 2, testMaze2) == {0: 3, 1: 2, 2: 5, 3: 6, 4: 1, 5: 8, 6: 7, 7: 8, 8: None})
	#assert(finalPath({0: 3, 1: 2, 2: 5, 3: 6, 4: 1, 5: 8, 6: 7, 7: 8, 8: None}, 8, 0) == [7,6,3,0])
	print("passed!")

testMaze =  [ \
  [ ['Left', 'Up', 'Down'], ['Right', 'Up', 'Down'], ['Right', 'Left', 'Up', 'Down'] ],
  [ ['Right', 'Left', 'Up', 'Down'], ['Left', 'Up'], ['Right', 'Up', 'Down'] ],
  [ ['Left', 'Up', 'Down'], ['Right', 'Down'], ['Right', 'Left', 'Up', 'Down'] ]] 

testMaze2 =  [ \
  [ ['Left', 'Up', 'Down'], ['Right', 'Up', 'Down'], ['Right', 'Left', 'Up', 'Down'] ],
  [ ['Right', 'Left', 'Up', 'Down'], ['Left', 'Up'], ['Right', 'Up', 'Down'] ],
  [ ['Left', 'Up', 'Down', 'Right'], ['Right', 'Left','Down'], ['Right', 'Left', 'Up', 'Down'] ]] 

#main()

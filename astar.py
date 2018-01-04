###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# ai Players: 4th level of "intelligence"
# Basic framework for A* algorithm: https://www.youtube.com/watch?v=pKnV6ViDpAI
# All code implementations completely by Andrea Estrada
#
###############################################################################
import pygame #graphics
import spec
import copy
import player
import ai

class Node(object):
	def __init__(self, y, x):
		self.x = x #x grid coor
		self.y = y #y grid coor
		self.parentNode = None
		self.gCost = 0 #cost from start node to current node
		self.hCost = 0 #cost from current node to end node
		self.fCost = self.gCost + self.hCost

	def __repr__(self):
		return "(%d,%d)" % (self.y,self.x)

###############################################################################
#
# A STAR
#
###############################################################################

class AIFour(ai.AIPlayer): 

	#level four AI player finds most efficent path to a given player's location 
	def move(self):
		if self.getMazeSpot(): #in the center of a square
			self.routeNow = self.aStar()
			self.translatePath()
			if len(self.routeNow) >= 1: 
				self.dX = self.dDistance * self.routeNow[0][1]
				self.dY = self.dDistance * self.routeNow[0][0]
				self.routeNow.pop(0)
		self.collide()
		self.carryOut()

	#a* algorithm
	def aStar(self):
		self.createNodes() #create base nodes, stored in 2D list self.mazeNodes

		self.openList = list() #set of nodes to be evaluated
		self.closedList = list() #set of nodes already evaluated

		#add start node to open
		start = self.currentSlot()
		self.startNode = self.mazeNodes[start[1]][start[0]]
		self.openList.append(self.startNode)

		#designate node that holds "winning" condition
		if self.tag == "me": end = spec.me.currentSlot() #my AI
		elif self.tag == "opponent": end = spec.opponent.currentSlot() #other AI
		self.endNode = self.mazeNodes[end[1]][end[0]]

		while(len(self.openList) > 0):
			self.setCurrentNode() #set current equal to the node in openList with the lowest fCost
			self.openList.remove(self.currentNode)
			self.closedList.append(self.currentNode)

			if self.currentNode == self.endNode: #escape condition -- solved!
				path = self.finalPath(self.startNode, self.endNode)
				return path

			for neighbor in self.findNeighbor():
				if neighbor in self.closedList: continue
				newPathDistance = self.currentNode.gCost + self.getDistance(self.currentNode, neighbor)
				if newPathDistance < neighbor.gCost or neighbor not in self.openList:
					neighbor.gCost = newPathDistance
					neighbor.hCost = self.getDistance(neighbor, self.endNode)
					neighbor.parent = self.currentNode
					if neighbor not in self.openList: self.openList.append(neighbor)

	#returns neighboring nodes
	def findNeighbor(self):
		currX = self.currentNode.x
		currY = self.currentNode.y
		neighbors = []
		#possible moves from current node
		self.moves = spec.maze[currY][currX]
		self.checkX = currX
		self.checkY = currY 
		self.edgeCases()
		for direction in self.moves:
			dX, dY = self.translateMove(direction)
			neighbors.append(self.mazeNodes[currY + dY][currX + dX])
		return neighbors

	#chooses current node from open list based on smalles f cost
	def setCurrentNode(self):
		currentNode = self.openList[0]
		for i in range(1, len(self.openList)):
			if self.openList[i].fCost < currentNode.fCost or (self.openList[i].fCost == currentNode.fCost and self.openList[i].hCost < currentNode.hCost):
				currentNode = self.openList[i]
		self.currentNode = currentNode

	#creates nodes with base info for costs
	def createNodes(self):
		self.mazeNodes = []
		for row in range(len(spec.maze)):
			currRow = []
			for col in range(len(spec.maze[0])):
				currRow.append(Node(row, col))
			self.mazeNodes.append(currRow)

	def getDistance(self, nodeA, nodeB):
		y = abs(nodeA.y - nodeB.y)
		x = abs(nodeA.x - nodeB.x)
		return 1*y + 1*x

	def finalPath(self, startNode, endNode):
		path = []
		currentNode = endNode
		while currentNode != startNode:
			path.append(currentNode)
			currentNode = currentNode.parent
		return path[::-1]

	#translate path produced by a* algorithm
	def translatePath(self):
		currX, currY = self.currentSlot()
		translated = []
		for newNode in self.routeNow:
			y = newNode.y
			x = newNode.x
			dY = y-currY
			dX = x-currX
			translated.append((dY, dX))
			currY = y
			currX = x
		self.routeNow = translated




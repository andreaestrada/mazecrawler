###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Main file handling all major gameplay
# Basic pygame outline (starter code): https://qwewy.gitbooks.io/pygame-module-manual/content/
# Basic server outline (starter code): https://kdchin.gitbooks.io/sockets-module-manual/content/
# 
###############################################################################
import pygame
import sys
import time

from random import *

import spec #game specifications
import generateMaze #creates randomized mazes
import drawMaze #draws randomized mazes
import player #characters
import levels #information for each different level

#features
import pyaudio #play audio
import ammo #ammunition
import features #draw features side panels
import pointPieces #points
import powerupPiles #piles of different powerups
import singlePowerup #single powerups
import levelInstructions 

import drawing #V
import interaction #C

#multiplayer
import socket
import threading
from queue import Queue

#set up server
import server
import subprocess #allow user to start subprocess of running server

###############################################################################
#
# INITIAL SERVER HANDLING
# 
###############################################################################

def setUpServer(data):
	data.p = subprocess.Popen(['python3', 'server.py'])

def joinServer(data):
	data.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	data.server.connect((spec.host,int(spec.port)))
	serverMsg = Queue(100)
	spec.server = data.server
	threading.Thread(target = handleServerMsg, args = (data.server, serverMsg, data)).start()

def handleServerMsg(server, serverMsg, data):
		data.serverMsg = serverMsg
		server.setblocking(1)
		msg = ""
		command = ""
		while True:
			msg += data.server.recv(10).decode("UTF-8")
			command = msg.split("\n")
			while (len(command) > 1):
				readyMsg = command[0]
				msg = "\n".join(command[1:])
				data.serverMsg.put(readyMsg)
				command = msg.split("\n")

###############################################################################
#
# GAMEPLAY
# 
###############################################################################

class MazeGame(object):

	#################################
	#
	# Initialize game
	# 
	#################################

	def init(data):
		spec.startAI = 0
		spec.port = ""

		#allow access of game specifications to all docs
		spec.gameDisplay = pygame.display.set_mode((data.width, data.height))
		spec.screenWidth = data.width
		spec.screenHeight = data.height
		spec.gameWidth = (2/3)*spec.screenWidth
		spec.gameHeight = (3/4)*spec.screenHeight

		spec.server = data.server

		#change when difficulty changes
		spec.cellWidth = spec.gameWidth/spec.difficulty
		spec.cellHeight = spec.gameHeight/spec.difficulty
		spec.wallThickness = spec.cellHeight//10
		spec.vPad = (spec.screenHeight-spec.gameHeight)/2
		spec.hPad = (spec.screenWidth-spec.gameWidth)/2

		spec.maze = generateMaze.createMaze()
		drawMaze.border()
		drawMaze.cellWalls()

		#base player information
		data.players = [player.Character(1), player.Character(2)]

		#game play once players have joined
		#arbitrarily assign values until connect to server
		data.myID = -1
		data.me = data.players[0]
		data.opponent = data.players[1]
		spec.me = data.me
		spec.opponent = data.opponent

		spec.mazeLevels[spec.level-1](data)

	#################################
	#
	# Player <> Computer Interaction
	# 
	#################################

	def mousePressed(data, x, y):
		currentState = spec.gamePath[spec.gameStatus]
		features.checkAudio(x,y)
		homeValid = x > 65 and x < 200 and y > 630 and y < 655
		nextValid = x > 965 and x < 1010 and y > 630 and y < 655
		if currentState == "Splash":
			if x > 370 and x < 710 and y > 345 and y < 390: spec.gameStatus = 1
			if x > 370 and x < 710 and y > 415 and y < 475: spec.gameStatus = 2
		if currentState == "Create" or (currentState == "Join" and not spec.inGame) or currentState == "GameOver":
			if homeValid: 
				spec.gameStatus = 0 #home
			if currentState == "GameOver": #close game
				if "p" in data.__dict__: data.p.kill()
				pygame.quit()
				quit()


		if currentState == "Create" or currentState == "Join" or currentState == "User" or currentState == "Instructions" or "Ranking" in currentState:  #next from screen
			if nextValid: 
				spec.currTimer = 0
				if currentState == "Join": spec.cursorIndex = 0
				if (not currentState == "Join" or data.myID != -1) and "Level" not in currentState: spec.gameStatus += 1 #next
				if currentState == "User": data.sendUser()
				if currentState == "Instructions": 
					spec.currTimer = 0
					data.playerReady()
					spec.outOfLevel = False
				if "Ranking" in currentState:
					if not spec.mazeCommunicated:
						spec.mazeCommunicated = True
						data.sendMaze()
					spec.outOfLevel = False
					data.playerReady()
					spec.reset = False
		if "Level" in currentState and nextValid: #next from round
			spec.me.pause = False
			spec.me.pauseTimer = 0
			spec.opponent.pause = False
			spec.opponent.pauseTimer = 0
			if spec.level <= 4 and int(spec.levelTimer-spec.currTimer) < 0:
				spec.gameStatus += 1
				spec.mazeCommunicated = False
				spec.level += 1
				spec.mazeLevels[spec.level-1](data)
				spec.outOfLevel = True
				if spec.mazeBacklog != "": 
					data.acceptMaze(spec.mazeBacklog)
				spec.sentReady = False
			if spec.level == 5:
				spec.gameStatus += 1

		if currentState == "Create" or currentState == "Join":
			if x > 680 and x < 740 and y > 400 and y < 420: interaction.connection(currentState, data)

	def playerReady(data):
		spec.selfReady = True
		msg = "OpponentReady ExtraneousDetail \n"
		data.server.send(msg.encode())
		if spec.selfReady and spec.otherReady:
			spec.playing = True
			spec.currTimer = 0

	#write selected port number to file
	def replacePort(data, specFile = "spec.py", line = 13, port = spec.port):
		lines = open(specFile, 'r').readlines()
		lines[line] = "port = %s\n" % port
		out = open(specFile, 'w')
		out.writelines(lines)
		out.close()

	#handle user interaction with game via keyboard
	def keyPressed(data, keyCode, modifier):
		currentState = spec.gamePath[spec.gameStatus]

		#control q to quit game
		if keyCode == pygame.K_LCTRL: spec.keys["Control"] = True
		if keyCode == pygame.K_q: spec.keys["q"] = True

		#create game, join game
		if currentState == "Create" or currentState == "Join": interaction.portCursor(data, keyCode, currentState)
		if currentState == "User": interaction.nameCursor(data, keyCode)

		if "Level" in currentState:
			#generate powerups on command, for demonstration purposes
			if keyCode == pygame.K_g: singlePowerup.Single.generateNewPowerup(data, "GhostAdded")
			elif keyCode == pygame.K_3: singlePowerup.Single.generateNewPowerup(data, "ThreeAdded")
			elif keyCode == pygame.K_p: singlePowerup.Single.generateNewPowerup(data, "PauseAdded")

			#generate piles on command, for demonstration purposes
			if keyCode == pygame.K_m: powerupPiles.Piles.generateNewPowerup(data, "AmmoAdded")
			elif keyCode == pygame.K_o: powerupPiles.Piles.generateNewPowerup(data, "PointsAdded")

		#gameplay
		interaction.shootAmmo(keyCode)
		interaction.pressAndHoldGame(keyCode)

	def keyReleased(data, keyCode, modifier):
		#control q to quit game
		if keyCode == pygame.K_LCTRL: spec.keys["Control"] = False
		if keyCode == pygame.K_q: spec.keys["w"] = False

		#gameplay
		interaction.releaseHoldGame(keyCode)

	def isKeyPressed(data, key): return data._keys.get(key, False) #keys being held down

	def mouseReleased(data, x, y): pass

	def mouseMotion(data, x, y): pass 

	def mouseDrag(data, x, y): pass

	#################################
	#
	# Process every timer fired
	# 
	#################################

	def quitGame(data):
		#control q to quit game
		if "q" in spec.keys and "Control" in spec.keys and spec.keys["q"] and spec.keys["Control"]:
			if "p" in data.__dict__: data.p.kill()
			pygame.quit()
			quit()

	def changeSpeed(data):
		if "A" in spec.keys and spec.keys["A"]:
			spec.me.speed -= 0.2
			if spec.me.speed <0: spec.me.speed = 0
			msg = "OpponentSpeed %d \n" % spec.me.speed
			data.server.send(msg.encode())
		if "S" in spec.keys and spec.keys["S"]:
			spec.me.speed += 0.2
			if spec.me.speed > spec.maxSpeed: spec.me.speed = spec.maxSpeed
			msg = "OpponentSpeed %d \n" % spec.me.speed
			data.server.send(msg.encode())

	def playerMovement(data):
		move = spec.me.speed
		dY = 0
		dX = 0
		#my player movement
		if "Up" in spec.keys and spec.keys["Up"]: dY = -move
		if "Down" in spec.keys and spec.keys["Down"]: dY = move
		if "Right" in spec.keys and spec.keys["Right"]: dX = move
		if "Left" in spec.keys and spec.keys["Left"]: dX = -move
		#move yourself
		if dY != 0 or dX != 0: 
			data.me.move(dX, dY)

		move = spec.opponent.speed
		dY = 0
		dX = 0
		#opposing player movement
		if "Up" in spec.otherKeys and spec.otherKeys["Up"]: dY = -move
		if "Down" in spec.otherKeys and spec.otherKeys["Down"]: dY = move
		if "Right" in spec.otherKeys and spec.otherKeys["Right"]: dX = move
		if "Left" in spec.otherKeys and spec.otherKeys["Left"]: dX = -move
		#move opponent
		if dY != 0 or dX != 0: 
			data.opponent.move(dX, dY)

	def aiMovement(data):
		if spec.aiPause or spec.currTimer < 0.25: return None #no movement 
		for compPlayer in spec.computerPlayers: compPlayer.move()

	def changeImgs(data): #gifs
		if spec.pauseCurr == spec.pauseTotal:
			for points in spec.points:
				if choice([True, False]): points.changeImage()
			for ammoPile in spec.staticAmmos: ammoPile.changeImage()
			for pointPile in spec.staticPoints: pointPile.changeImage()
			for pauseElement in spec.pause: pauseElement.changeImage()
			for triple in spec.threeTimes: triple.changeImage()
			for ghostElement in spec.ghost: ghostElement.changeImage()
			for compPlayer in spec.computerPlayers: compPlayer.changeImage()
			data.me.changeImage()
			data.opponent.changeImage()
			spec.pauseCurr = 0
		else: spec.pauseCurr += 1

	def featuresGo(data):
		if "Level" in spec.gamePath[spec.gameStatus] and spec.playing:
			#randomly generate piles
			if not randint(0,spec.fireAmmo) and spec.ammoOn: powerupPiles.Piles.generateNewPowerup(data, "AmmoAdded")
			if not randint(0,spec.firePoints) and spec.pointPilesOn: powerupPiles.Piles.generateNewPowerup(data, "PointsAdded")

			#randomly generate singles
			totalSingles = len(spec.pause.sprites()) + len(spec.threeTimes.sprites()) + len(spec.ghost.sprites())
			if totalSingles <= 5:
				if not randint(0,spec.fireSingles) and spec.singles: singlePowerup.Single.generateNewPowerup(data, "GhostAdded")
				if not randint(0,spec.fireSingles) and spec.singles: singlePowerup.Single.generateNewPowerup(data, "ThreeAdded")
				if not randint(0,spec.fireSingles) and spec.singles: singlePowerup.Single.generateNewPowerup(data, "PauseAdded")

	def checkPowerups(data):
		if data.me.hasPowerup and data.me.powerupEnd <= spec.currTimer: MazeGame.resetPowerups(data.me)
		if data.opponent.hasPowerup and data.opponent.powerupEnd <= spec.currTimer: MazeGame.resetPowerups(data.opponent)

	@staticmethod
	def resetPowerups(character):
		if not character.ghost or not pygame.sprite.spritecollide(character, spec.walls, False): #don't end ghost while player on a wall
			character.hasPowerup = False
			character.bonus = False
			character.ghost = False
			spec.aiPause = False
			character.aiPause = False
			character.powerUpEnd = 0

	#################################
	#
	# Graphics
	# 
	#################################

	def redrawAll(data, screen):
		if "Level" in spec.gamePath[spec.gameStatus]:
			drawing.drawMaze()
			drawing.drawPowerups()
			for compPlayer in spec.computerPlayers:
				compPlayer.draw()
			data.opponent.draw()
			data.me.draw()
			drawing.drawFeatures(data)
		elif spec.gamePath[spec.gameStatus] == "GameOver": drawing.drawGameOver()
		elif spec.gamePath[spec.gameStatus] == "Splash": drawing.drawSplashScreen()
		elif spec.gamePath[spec.gameStatus] == "Create": drawing.inputScreen("create new game...", "create a game key from 10000-65535", "create", data) #draw newgame screen (initalize server)
		elif spec.gamePath[spec.gameStatus] == "Join": drawing.inputScreen("join via game code...", "enter a valid game code from 10000-65535", "join", data) #draw newgame screen (initalize server)
		elif spec.gamePath[spec.gameStatus] == "User": drawing.selectUsername("enter username...", "enter a username up to 7 characters") #draw newgame screen (initalize server)
		elif spec.gamePath[spec.gameStatus] == "Instructions": drawing.instructionsScreen()

		elif spec.gamePath[spec.gameStatus] == "RankingOne": drawing.betweenLevels(levelInstructions.levelTwo)
		elif spec.gamePath[spec.gameStatus] == "RankingTwo": drawing.betweenLevels(levelInstructions.levelThree)
		elif spec.gamePath[spec.gameStatus] == "RankingThree": drawing.betweenLevels(levelInstructions.levelFour)
		elif spec.gamePath[spec.gameStatus] == "RankingFour": drawing.betweenLevels(levelInstructions.levelFive)

	#################################
	#
	# Timer Fired: deal with server
	# 
	#################################!

	def sendMaze(data):
		if data.myAI != None:
			#existing maze, player1 x, player1 y, player2 x, player2 y
			sendMazeMsg = "ExistingMaze %s %d %d %d %d %d %d %d %d\n" % \
				(str(spec.maze).replace(" ", ""), \
				data.me.rect.x, data.me.rect.y, data.opponent.rect.x, data.opponent.rect.y, data.myAI.rect.x, data.myAI.rect.y, data.otherAI.rect.x, data.otherAI.rect.y)
			data.server.send(sendMazeMsg.encode())
		else: 
			#existing maze, player1 x, player1 y, player2 x, player2 y
			sendMazeMsg = "ExistingMaze %s %d %d %d %d\n" % \
				(str(spec.maze).replace(" ", ""), \
				data.me.rect.x, data.me.rect.y, data.opponent.rect.x, data.opponent.rect.y)
			data.server.send(sendMazeMsg.encode())

	def sendUser(data):
		sendUsernameMsg = "OpponentUsername %s\n" % spec.myUser 
		data.server.send(sendUsernameMsg.encode())


	def timerFired(data, dt):
		data.quitGame()
		data.featuresGo()
		data.changeImgs()
		data.checkPowerups()

		data.me.aiCollide()
		data.opponent.aiCollide()

		if spec.countCursor == 7: 
			if spec.showCursor: spec.showCursor = False
			else: spec.showCursor = True 
			spec.countCursor = 0
		else: spec.countCursor += 1

		if spec.countFlash == 10: 
			if spec.flash: spec.flash = False
			else: spec.flash = True 
			spec.countFlash = 0
		else: spec.countFlash += 1

		if spec.playing and spec.speedOn: 
			data.changeSpeed()
			data.playerMovement()
			data.aiMovement()

		for bullet in spec.ammos:
			bullet.move()

		if data.serverMsg and (data.serverMsg.qsize() > 0):
			msg = data.serverMsg.get(False)
			msg = msg.split()
			command = msg[0]

			if (command == "MyIDis"):
				data.myID = int(msg[1][-1]) - 1 #calculate index of you
				data.me = data.players[data.myID]
				if data.myID == 0: data.opponent = data.players[1]
				else: data.opponent = data.players[0]
				spec.me = data.me
				spec.opponent = data.opponent
				spec.inGame = True
				if data.myID == 1: data.sendUser()

			elif (command == "PlayerJoined"): 
				if data.myID == 0: 
					data.sendMaze()
					data.sendUser()

			#opponent movement
			elif (command == "KeyPressed"):
				spec.otherKeys[msg[2]] = True
			elif (command == "KeyUp"):
				spec.otherKeys[msg[2]] = False
			elif (command == "OpponentSpeed"):
				spec.opponent.speed = int(msg[2])

			#opponent ammunition
			elif (command == "OpponentScored"):
				scoreAdd = int(msg[2]) 
				data.opponent.score += scoreAdd
			elif (command == "Ammunition"):
				ammo.Ammunition("Opponent")
				spec.opponent.ammoOwned -= 1

			elif (command == "ExistingMaze"): 
				spec.mazeBacklog = msg
				if spec.outOfLevel: data.acceptMaze(msg)

			#spawned powerups
			elif (command == "AmmoAdded"):
				powerupPiles.AmmoPile(int(msg[2]), int(msg[3]), int(msg[4]))
			elif (command == "PointsAdded"):
				powerupPiles.PointPile(int(msg[2]), int(msg[3]), int(msg[4]))
			elif (command == "GhostAdded"):
				singlePowerup.Ghost(int(msg[2]), int(msg[3]))
			elif (command == "ThreeAdded"):
				singlePowerup.Three(int(msg[2]), int(msg[3]))
			elif (command == "PauseAdded"):
				singlePowerup.Pause(int(msg[2]), int(msg[3]))

			elif (command == "AIat"):
				data.otherAI.rect.centerx = float(msg[2])
				data.otherAI.rect.centery = float(msg[3])

			#opponent game info
			elif (command == "OpponentReady"): 
				spec.otherReady = True
				if not spec.sentReady and spec.selfReady: #account for case where player 2 joins server after player 1 is ready
					spec.sentReady = True 
					msg = "OpponentReady ExtraneousDetail \n"
					data.server.send(msg.encode())
					data.sendUser()
				if spec.selfReady and spec.otherReady:
					spec.playing = True
					spec.currTimer = 0
			elif (command == "OpponentUsername"):
				if msg[2] != "you":
					spec.opponentUser = msg[2]

			data.serverMsg.task_done()

	def acceptMaze(data, msg):
		spec.mazeCommunicated = True
		spec.maze = data.decodeList(msg[2])
		spec.walls.empty()
		spec.borders.empty()
		spec.points.empty()
		#generate new maze + wall sprites
		drawMaze.cellWalls()
		drawMaze.border()
		#data.me.rect.x, data.me.rect.y, data.opponent.rect.x, data.opponent.rect.y
		data.me.rect.x = int(msg[5])
		data.me.rect.y = int(msg[6])
		data.opponent.rect.x = int(msg[3])
		data.opponent.rect.y = int(msg[4])

		if data.myAI != None:
			data.otherAI.rect.x = float(msg[7])
			data.otherAI.rect.y = float(msg[8])
			data.otherAI.tag = "opponent"

			data.myAI.rect.x = float(msg[9])
			data.myAI.rect.y = float(msg[10])

		spec.mazeBacklog = ""


	def decodeList(self, strList): #decode sent list
		decodedList = []
		rows = strList.split("[[")[1:]
		for row in rows:
			decodedRow = []
			cols = row.split(",[")
			for col in cols:
				decodedCol = []
				if "Down" in col: decodedCol.append("Down")
				if "Right" in col: decodedCol.append("Right")
				if "Up" in col: decodedCol.append("Up")
				if "Left" in col: decodedCol.append("Left")
				decodedRow.append(decodedCol)
			decodedList.append(decodedRow)
		return(decodedList)


	#################################
	#
	# Framework
	# 
	#################################

	def __init__(data, width=1080, height=720, fps=50, title="maze"):
		data.width = width
		data.height = height
		data.fps = fps
		data.title = title
		data.bgColor = (255, 255, 255)
		pygame.init()

	def run(data, serverMsg = None, server = None):

		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((data.width, data.height))
		# set the title of the window
		pygame.display.set_caption(data.title)

		pygame.mixer.pre_init(44100,16,2,4096)
		pygame.mixer.music.load("audio/africa.wav")
		pygame.mixer.music.set_volume(spec.volume)
		pygame.mixer.music.play(-1)

		data.serverMsg = serverMsg
		data.server = server

		# call game-specific initialization
		data.init()
		playing = True

		while playing:

			time = clock.tick(data.fps)
			data.timerFired(time)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					data.mousePressed(*(event.pos))
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					data.mouseReleased(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons == (0, 0, 0)):
					data.mouseMotion(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons[0] == 1):
					data.mouseDrag(*(event.pos))
				elif event.type == pygame.KEYDOWN:
					data.keyPressed(event.key, event.mod)
				elif event.type == pygame.KEYUP:
					data.keyReleased(event.key, event.mod)
				elif event.type == pygame.QUIT:
					playing = False
			screen.fill(data.bgColor)
			data.redrawAll(screen)
			pygame.display.flip()

			seconds = clock.tick()/1000
			spec.currTimer += seconds

		pygame.quit()


def main():

	game = MazeGame()
	game.run()

if __name__ == "__main__":
   main()
###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Game specifications used throughout files, initialized upon start
# 
###############################################################################
import pygame #for pygame sprite groups
import os.path
import pygame.mixer
import levels

host = "" #IP Address for cross-computer game play
port = 13333

#player usernames
myUser = ""
opponentUser = "opponent"

pygame.init()
 
#tracks point in the game
gamePath = ["Splash", "Create", "Join", "User", "Instructions", "LevelOne", "RankingOne", 
			"LevelTwo", "RankingTwo", "LevelThree", "RankingThree", "LevelFour", 
			"RankingFour", "LevelFive", "GameOver"]

mazeCommunicated = False
mazeBacklog = ""

gameStatus = 0
inGame = False #wheter you have game code
outOfLevel = True #in level
reset = False

dontJoin = set() #list of non-working ports

server = None

#audio default volume
volume = 0.5

maxSpeed = 4

#create surver, join game, select username
usingCursor = False
showCursor = True
flash = True
countCursor = 0
countFlash = 0
cursorIndex = 0

#timer
pauseTotal = 5
pauseCurr = 0
currTimer = 0
levelTimer = 15

#number of rows/cols in maze determines difficulty of game
difficulty = 1 #square dimensions of maze
mazeLevels = [levels.levelOne, levels.levelTwo, levels.levelThree, levels.levelFour, levels.levelFive]
level = 1
breakWalls = 0.05 #percentage of board to turn into loops

#current gameboard
maze = 0
mazeType = None

#info on keys being pressed
keys = dict()
otherKeys = dict()

#draw to screen
gameDisplay = None

#full window
screenWidth = 0
screenHeight = 0

#inner maze part of screen
gameHeight = 0
gameWidth = 0

#info for drawing maze
vPad = 0
hPad = 0
cellHeight = 0
cellWidth = 0
wallThickness = 0
wallColor = (0,0,0)

#sprite groups
#maze
walls = pygame.sprite.Group()
borders = pygame.sprite.Group()
#players
players = pygame.sprite.Group()
computerPlayers = pygame.sprite.Group()
#powerups
points = pygame.sprite.Group()
staticPoints = pygame.sprite.Group()
ammos = pygame.sprite.Group()
staticAmmos = pygame.sprite.Group()
pause = pygame.sprite.Group()
threeTimes = pygame.sprite.Group()
ghost = pygame.sprite.Group()

#control speed of random powerups appearing: decrease these numbers for faster spawning
firePoints = 100
fireAmmo = 300
fireSingles = 900

#status in terms of playing
selfReady = False
otherReady = False
playing = False 
sentReady = False

#features
ammoOn = False
speedOn = False
pointPilesOn = False
aiPause = True
shotFired = pygame.mixer.Sound("audio/fired.wav")
playerHit = pygame.mixer.Sound("audio/hit.wav")

#load images
player1Images = []
for i in range(8):
    player1Images.append(pygame.image.load("images/player1/" + str(i)+".jpg"))
player2Images = []
for i in range(8):
    player2Images.append(pygame.image.load("images/player2/" + str(i)+".jpg"))
aiImages = []
for i in range(8):
    aiImages.append(pygame.image.load("images/ai/" + str(i)+".jpg"))
pointImages = []
for i in range(5):
    pointImages.append(pygame.image.load("images/point/pieces/" + str(i)+".png"))
pointPileImages = []
for i in range(7): 
	pointPileImages.append(pygame.image.load("images/point/pile/" + str(i) + ".png"))
ammoImage = pygame.image.load("images/ammo/ammo.png")
ammoPileImages = []
for i in range(8):
    ammoPileImages.append(pygame.image.load("images/ammo/ammopile/" + str(i)+".png"))
pauseImages = []
for i in range(2):
	pauseImages.append(pygame.image.load("images/varPowerups/pause/" + str(i)+".png"))
threeTimesImages = []
for i in range(2):
	threeTimesImages.append(pygame.image.load("images/varPowerups/three/" + str(i)+".png"))
ghostImages = []
for i in range(2):
	ghostImages.append(pygame.image.load("images/varPowerups/ghost/" + str(i)+".png"))
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (1080,720))

#load different sized text	
sixteenFont = pygame.font.Font("fonts/raleway.ttf", 16)
twentyFont = pygame.font.Font("fonts/raleway.ttf", 20)
twentyFiveFont = pygame.font.Font("fonts/raleway.ttf", 24)
thirtyFont = pygame.font.Font("fonts/raleway.ttf", 30)
fourtyFont = pygame.font.Font("fonts/raleway.ttf", 40)
fiftyFont = pygame.font.Font("fonts/raleway.ttf", 50)
hundredFont = pygame.font.Font("fonts/raleway.ttf", 90)
largeFont = pygame.font.Font("fonts/raleway.ttf", 160)
featuresColor =  (255,255,255)
validColor = (176, 237, 188)
invalidColor = (237, 180, 176)
backgroundColor = (45,45,45)



###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Redraw all functions
# 
###############################################################################
import pygame
import spec 
import features
import levelInstructions

#draws gameboard
def drawMaze():
        spec.walls.draw(spec.gameDisplay)
        spec.borders.draw(spec.gameDisplay)

#triggers drawing of sidepanels, text, etc.
def drawFeatures(data):
    features.drawGeneral("maze crawler", 0, spec.fiftyFont)

    if spec.flash and spec.me.bonus: features.drawGeneral("powerup: triple points", spec.gameHeight+spec.vPad, spec.thirtyFont)
    if spec.flash and spec.me.ghost: features.drawGeneral("powerup: go through walls", spec.gameHeight+spec.vPad, spec.thirtyFont)
    if spec.flash and spec.me.aiPause: features.drawGeneral("powerup: paused the monsters", spec.gameHeight+spec.vPad, spec.thirtyFont)

    if spec.myUser == "": spec.myUser = "you"
    features.drawText(spec.myUser, spec.opponentUser, spec.thirtyFont, 5)
    features.drawText("score: %d" % data.me.score, "score: %d" % data.opponent.score, spec.twentyFont, 55)
    if spec.ammoOn: features.drawText("ammo: %d" % data.me.ammoOwned, "ammo: %d" % data.opponent.ammoOwned, spec.twentyFont, 85)
    if spec.speedOn: 
        features.drawText("speed:", "speed:", spec.twentyFont, 135)
        features.drawText("-                        +","-                        +", spec.twentyFont, 160)
        features.drawSpeed()
    features.drawAudio()
    features.drawTime()
    features.drawLevel()
    features.drawGameNum()

#points, ammunition, single powerups
def drawPowerups():
    spec.points.draw(spec.gameDisplay)
    spec.staticPoints.draw(spec.gameDisplay)
    spec.ammos.draw(spec.gameDisplay)
    spec.staticAmmos.draw(spec.gameDisplay)
    spec.pause.draw(spec.gameDisplay)
    spec.threeTimes.draw(spec.gameDisplay)
    spec.ghost.draw(spec.gameDisplay)
   
#splash screen 
def drawSplashScreen():
    pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (0,0,spec.screenWidth, spec.screenHeight))
    spec.gameDisplay.blit(spec.background, (0,0))
    pygame.draw.rect(spec.gameDisplay, (0,0,0), (0,125, spec.screenWidth, 400))
    features.drawGeneral("maze crawler", 190, spec.largeFont)
    features.drawGeneral("create new game", spec.screenHeight*1/2-40, spec.fourtyFont)
    features.drawGeneral("join existing game", spec.screenHeight*1/2 + 35, spec.fourtyFont)
    features.drawAudio()

#background for instructions, gameover screen
def drawBackground():
    pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (0,0,spec.screenWidth, spec.screenHeight))
    spec.gameDisplay.blit(spec.background, (0,0))
    pygame.draw.rect(spec.gameDisplay, (0,0,0), (50,50, spec.screenWidth-100, spec.screenHeight-100))

#enter port for connecting to server or joining game
def inputScreen(summaryTxt, instructionTxt, doneTxt, data):
    #color of text based on whether input is valid

    spec.usingCursor = True
    xStart = spec.screenWidth/2-190
    drawBackground()
    myText = spec.fourtyFont.render(summaryTxt, 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (65,65))
    myText = spec.twentyFont.render(instructionTxt, 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (spec.screenWidth/2-200,spec.screenHeight/2-90))
    pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (spec.screenWidth/2-200, spec.screenHeight/2-60, 400, 100))
    if "join" in summaryTxt and str(spec.port) in spec.dontJoin: 
        myText = spec.twentyFont.render("ERROR please try another game code", 1, spec.invalidColor)
        spec.gameDisplay.blit(myText, (spec.screenWidth/2-200,spec.screenHeight/2-110))

    #user input: cursor and user input text
    try:
        if str(spec.port).isdigit() and len(str(spec.port)) == 5 and int(spec.port) <= 65535 and int(spec.port)>= 10000 : color = spec.validColor
        else: color = spec.invalidColor
        if str(spec.port) in spec.dontJoin and "join" in summaryTxt: color = spec.invalidColor

        #draw text, cursor
        myText = spec.hundredFont.render(str(spec.port)[:spec.cursorIndex], 1, color) #first partition of text
        xPad, extra = spec.hundredFont.size(str(spec.port)[:spec.cursorIndex])
        spec.gameDisplay.blit(myText, (xStart,spec.screenHeight/2-70))
        myText = spec.hundredFont.render(str(spec.port)[spec.cursorIndex:], 1, color) #second partition of text
        spec.gameDisplay.blit(myText, (xStart+xPad,spec.screenHeight/2-70))
        if spec.showCursor: pygame.draw.line(spec.gameDisplay, spec.featuresColor, (xStart + xPad, spec.screenHeight/2-50), (xStart + xPad, spec.screenHeight/2 + 30)) #cursor
    except Exception as ex: #text has zero width when adding port
        if spec.showCursor: pygame.draw.line(spec.gameDisplay, spec.featuresColor, (xStart, spec.screenHeight/2-50), (xStart, spec.screenHeight/2 + 30))
        try:
            myText = spec.hundredFont.render(str(spec.port)[spec.cursorIndex:], 1, color)
            spec.gameDisplay.blit(myText, (xStart,spec.screenHeight/2-70))
        except: pass

    if "create" in summaryTxt or not spec.inGame: 
        homeText()
        myText = spec.twentyFont.render(doneTxt, 1, spec.featuresColor)
        xPad, extra = spec.twentyFont.size(doneTxt)
        spec.gameDisplay.blit(myText, (spec.screenWidth/2+200 - xPad, spec.screenHeight/2+40))
    if "create" in summaryTxt: 
        nextText()
    elif data.myID != -1: 
        nextText()
        myText = spec.twentyFont.render("joined!", 1, spec.validColor)
        xPad, extra = spec.twentyFont.size("joined!")
        spec.gameDisplay.blit(myText, (spec.screenWidth/2+200 - xPad, spec.screenHeight/2+40))
    else: 
        myText = spec.twentyFont.render(doneTxt, 1, spec.featuresColor)
        xPad, extra = spec.twentyFont.size(doneTxt)
        spec.gameDisplay.blit(myText, (spec.screenWidth/2+200 - xPad, spec.screenHeight/2+40))
    features.drawAudio()

#allows user to choose their own username
def selectUsername(summaryTxt, instructionTxt):
    spec.usingCursor = True
    xStart = spec.screenWidth/2-190
    drawBackground()
    myText = spec.fourtyFont.render(summaryTxt, 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (65,65))
    myText = spec.twentyFont.render(instructionTxt, 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (spec.screenWidth/2-200,spec.screenHeight/2-90))
    pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (spec.screenWidth/2-200, spec.screenHeight/2-60, 400, 100))

    #user input
    try:
        #color of text based on whether input is valid
        spec.validColor = (176, 237, 188)
        spec.invalidColor = (237, 180, 176)
        if len(spec.myUser) > 0 and len(spec.myUser) < 8: color = spec.validColor
        else: color = spec.invalidColor

        #draw text, cursor
        myText = spec.hundredFont.render(str(spec.myUser)[:spec.cursorIndex], 1, color) #first partition of text
        xPad, extra = spec.hundredFont.size(str(spec.myUser)[:spec.cursorIndex])
        spec.gameDisplay.blit(myText, (xStart,spec.screenHeight/2-70))
        myText = spec.hundredFont.render(str(spec.myUser)[spec.cursorIndex:], 1, color) #second partiotion of text
        spec.gameDisplay.blit(myText, (xStart+xPad,spec.screenHeight/2-70))
        if spec.showCursor: pygame.draw.line(spec.gameDisplay, spec.featuresColor, (xStart + xPad, spec.screenHeight/2-50), (xStart + xPad, spec.screenHeight/2 + 30)) #cursor
    except Exception as ex: #text has zero width when adding port
        if spec.showCursor: pygame.draw.line(spec.gameDisplay, spec.featuresColor, (xStart, spec.screenHeight/2-50), (xStart, spec.screenHeight/2 + 30))
        try:
            myText = spec.hundredFont.render(str(spec.myUser)[spec.cursorIndex:], 1, color)
            spec.gameDisplay.blit(myText, (xStart,spec.screenHeight/2-70))
        except: pass

    nextText()
    features.drawAudio()

#creates a banner for messages before/after gameplay or when player is hit
def banner(bannerText, backgroundOn = True, color = spec.featuresColor, font = spec.fourtyFont):
    if backgroundOn: 
        pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (0, spec.screenHeight/2-60, spec.screenWidth, 100))
    banner = font.render(bannerText, 1, color)
    xPad, extra = font.size(bannerText)
    spec.gameDisplay.blit(banner, (spec.screenWidth/2-xPad/2,spec.screenHeight/2-35))

#go back to the splash screen
def homeText(color = spec.featuresColor):
    homeTxt = spec.twentyFont.render("home", 1, color)
    spec.gameDisplay.blit(homeTxt, (70,spec.screenHeight-90))

#go to next page
def nextText(color = spec.featuresColor):
    nextText = spec.twentyFont.render("next", 1, color)
    xPad, extra = spec.twentyFont.size("next")
    spec.gameDisplay.blit(nextText, (spec.screenWidth - 70 - xPad,spec.screenHeight-90))

#premliminary instructions
def instructionsScreen():
    drawBackground()
    myText = spec.fourtyFont.render("instructions:", 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (65,65))
    instructions = levelInstructions.levelOne
    for i in range(len(instructions)):
        if instructions[i] == None: continue
        myText = spec.twentyFiveFont.render(instructions[i], 1, spec.featuresColor)
        spec.gameDisplay.blit(myText, (80,150+30*i))
    nextText()
    features.drawAudio()

#shows current specs of players
def drawCurrentRankings(yPad = 300):
    myText = spec.fourtyFont.render("current standings:", 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (65,65))

#sreen between levels, shows specs and instrucitons for next round
def betweenLevels(instructions):
    drawBackground()
    nextText()
    drawCurrentRankings()

    for i in range(len(instructions)):
        myText = spec.twentyFiveFont.render(str(instructions[i]), 1, spec.featuresColor)
        xPad, extra = spec.twentyFiveFont.size(str(instructions[i]))
        spec.gameDisplay.blit(myText, (spec.screenWidth*1/2-xPad/2, 500 + i*35))

    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (spec.screenWidth*1/3 + 40, 140), (spec.screenWidth*1/3 + 40, spec.screenHeight/2+80))
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (spec.screenWidth*2/3 - 40, 140), (spec.screenWidth*2/3 - 40, spec.screenHeight/2+80))
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (spec.screenWidth*1/3-200, 200), (spec.screenWidth*2/3+200, 200))
    myText = spec.twentyFiveFont.render("points earned", 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (spec.screenWidth*1/3-190, 200 + 30))
    myText = spec.twentyFiveFont.render("ammo shot", 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (spec.screenWidth*1/3-190, 200 + 90))
    myText = spec.twentyFiveFont.render("powerups used", 1, spec.featuresColor)
    spec.gameDisplay.blit(myText, (spec.screenWidth*1/3-190, 200 + 150))

    if spec.me.score > spec.opponent.score: myColor, opponentColor = spec.validColor, spec.invalidColor
    elif spec.me.score < spec.opponent.score: myColor, opponentColor = spec.invalidColor, spec.validColor
    else: myColor, opponentColor = spec.featuresColor, spec.featuresColor

    drawPerson(spec.me, spec.screenWidth*1/2, str(spec.myUser), myColor)
    drawPerson(spec.opponent, spec.screenWidth*2/3+80, str(spec.opponentUser), opponentColor)

#draws a person's specs
def drawPerson(person, x, name, color):
    myText = spec.twentyFiveFont.render(str(person.score), 1, spec.featuresColor)
    xPad, extra = spec.twentyFiveFont.size(str(person.score))
    spec.gameDisplay.blit(myText, (x-xPad/2, 200 + 30))
    myText = spec.twentyFiveFont.render(str(person.ammoShot), 1, spec.featuresColor)
    xPad, extra = spec.twentyFiveFont.size(str(person.ammoShot))
    spec.gameDisplay.blit(myText, (x-xPad/2, 200 + 90))
    myText = spec.twentyFiveFont.render(str(person.powerupsCollected), 1, spec.featuresColor)
    xPad, extra = spec.twentyFiveFont.size(str(person.powerupsCollected))
    spec.gameDisplay.blit(myText, (x-xPad/2, 200 + 150))
    myText = spec.twentyFiveFont.render(str(name), 1, color)
    xPad, extra = spec.twentyFiveFont.size(str(name))
    spec.gameDisplay.blit(myText, (x-xPad/2, 200 -40))

#game over, quit and exit game
def doneText(color = spec.featuresColor):
    done = spec.twentyFont.render("quit game", 1, color)
    spec.gameDisplay.blit(done, (70,spec.screenHeight-90))

#end game screen
def drawGameOver():
    if spec.myUser == "": spec.myUser = "you"
    pygame.draw.rect(spec.gameDisplay, spec.backgroundColor, (0,0,spec.screenWidth, spec.screenHeight))
    spec.gameDisplay.blit(spec.background, (0,0))
    pygame.draw.rect(spec.gameDisplay, (0,0,0), (0,125, spec.screenWidth, 400))
    features.drawGeneral("game over", 190, spec.hundredFont)
    if spec.me.score == spec.opponent.score: 
        if spec.flash: features.drawGeneral("tie game", 280, spec.fourtyFont)
        myColor = spec.featuresColor
        opponentColor = spec.featuresColor
    else:
        if spec.me.score < spec.opponent.score:
            winner = spec.opponentUser
            myColor = spec.invalidColor
            opponentColor = spec.validColor
        if spec.opponent.score < spec.me.score:
            winner = spec.myUser
            myColor = spec.validColor
            opponentColor = spec.invalidColor
        if spec.flash: features.drawGeneral("%s wins!" %winner, 280, spec.fourtyFont)
    font = spec.fourtyFont
    height = spec.screenHeight/2 + 20

    me = spec.myUser + ": " + str(spec.me.score)
    myText = font.render(me, 1, myColor)

    opponent = spec.opponentUser + ": " + str(spec.opponent.score)
    opponentText = font.render(opponent, 1, opponentColor)

    divide = "  |  "
    divideText = font.render(divide, 1, spec.featuresColor)
    xPad, extra = font.size(me + divide + opponent)

    meX = spec.screenWidth/2 - xPad/2
    xPadDivide, extra = font.size(me)
    divideX = spec.screenWidth/2 - xPad/2 + xPadDivide
    xPadOpp, extra = font.size(me + divide)
    opponentX = spec.screenWidth/2 - xPad/2 + xPadOpp

    spec.gameDisplay.blit(myText, (meX,height))
    spec.gameDisplay.blit(divideText, (divideX,height))
    spec.gameDisplay.blit(opponentText, (opponentX,height))
    doneText()



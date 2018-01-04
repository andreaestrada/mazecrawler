###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Features including audio, username, etc.
# 
###############################################################################
import spec
import pygame
import drawing

#text along columns for me vs opponent
def drawText(myWord, opponentWord, font, yPad):
    myWidth, oppWidth = 0, 0

    y = spec.vPad
    xOpp, xMe = spec.hPad/2, spec.screenWidth - spec.hPad/2

    myWidth, extra = font.size(str(myWord))
    oppWidth, extra = font.size(str(opponentWord))

    myText = font.render(str(myWord), 1, spec.featuresColor)
    oppText = font.render(str(opponentWord), 1, spec.featuresColor)

    spec.gameDisplay.blit(myText, (xMe - myWidth/2, y + yPad))
    spec.gameDisplay.blit(oppText, (xOpp - oppWidth/2, y + yPad))

def drawSpeed():
    #speed line
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (22 + 17, spec.vPad + 172), (158 - 17, spec.vPad + 172))
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (922 + 17, spec.vPad + 172), (1058 - 17, spec.vPad + 172))
    #moveable speed bar
    widthLine = 102
    meX = spec.me.speed/spec.maxSpeed * widthLine
    oppX = spec.opponent.speed/spec.maxSpeed * widthLine
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (22 + 17 + oppX, spec.vPad + 172 - 5), (22 + 17 + oppX, spec.vPad + 172 + 5))
    pygame.draw.line(spec.gameDisplay, spec.featuresColor, (922 + 17 + meX, spec.vPad + 172 - 5), (922 + 17 + meX, spec.vPad + 172 + 5))

#centered text
def drawGeneral(myWord, yPad, font):
    myWidth, myHeight = font.size(str(myWord))

    myText = font.render(str(myWord), 1, spec.featuresColor)

    spec.gameDisplay.blit(myText, (spec.screenWidth/2 - myWidth/2, spec.vPad/2 - myHeight/2 + yPad))


def drawAudio():
    x, y = 10, 10
    toggleWidth, extra = spec.sixteenFont.size("off")
    if spec.volume == 0: 
        myText = spec.sixteenFont.render("off", 1, spec.invalidColor)
        spec.gameDisplay.blit(myText, (spec.screenWidth-x-toggleWidth, y))
    else: 
        myText = spec.sixteenFont.render("on", 1, spec.validColor)
        spec.gameDisplay.blit(myText, (spec.screenWidth-x-toggleWidth, y))
    myText = spec.sixteenFont.render("audio: ", 1, spec.featuresColor)
    myWidth, extra = spec.sixteenFont.size("audio: off")
    spec.gameDisplay.blit(myText, (spec.screenWidth-myWidth-x, y))

def drawTime():
    x, y = 10, 10
    myText = spec.sixteenFont.render("time: ", 1, spec.featuresColor)
    myWidth, extra = spec.sixteenFont.size("time: ")
    spec.gameDisplay.blit(myText, (x, y))

    timeLeft = int(spec.levelTimer-spec.currTimer)

    if not spec.playing and timeLeft > 0: 
        drawing.banner("waiting for opponent...")
        spec.currTimer = 0
        if not spec.reset:
            spec.reset = True
            selfReady = False
            otherReady = False
        timeLeft += 1

    if spec.playing and spec.currTimer < 0.5:
        drawing.banner("play!")

    if spec.me.pause and spec.showCursor: drawing.banner("hit! temporarily disabled")

    if timeLeft >= 60:
        minutes = timeLeft//60
        seconds = timeLeft%60
        if seconds < 10: setTime = "%d:0%d" % (minutes, seconds)
        else: setTime = "%d:%d" % (minutes, seconds)
    elif timeLeft < 0: 
        drawing.nextText()
        drawing.banner("time is up!")
        spec.playing = False
        timeLeft = 0
        setTime = "0:00"
        spec.selfReady = False
        spec.otherReady = False
    elif timeLeft < 10: setTime = "O:0%d" % timeLeft
    else: setTime = "0:%d" % timeLeft
    myTime = spec.sixteenFont.render(setTime, 1, (255, 255, 255))
    spec.gameDisplay.blit(myTime, (x + myWidth, y))

def drawLevel():
    x, y = 10, 30
    myText = spec.sixteenFont.render("level: ", 1, spec.featuresColor)
    myWidth, extra = spec.sixteenFont.size("level: ")
    spec.gameDisplay.blit(myText, (x, y))
    myLevel = spec.sixteenFont.render(str(spec.level), 1, spec.featuresColor)
    spec.gameDisplay.blit(myLevel, (x + myWidth, y))

def drawGameNum():
    if str(spec.port) == "": spec.port = "00000"
    x, y = 10, 50
    myText = spec.sixteenFont.render("game code: ", 1, spec.featuresColor)
    myWidth, extra = spec.sixteenFont.size("game code: ")
    spec.gameDisplay.blit(myText, (x, y))
    try: 
        myGame = spec.sixteenFont.render(str(spec.port), 1, spec.featuresColor) #Text has zero width error when port is empty
        spec.gameDisplay.blit(myGame, (x + myWidth, y))
    except: pass

def checkAudio(x,y):
    audioXLower = spec.screenWidth - 82
    audioXUpper = spec.screenWidth - 10
    #change audio
    if x > audioXLower and x < audioXUpper and y > 10 and y < 30:
        if spec.volume == 0: spec.volume = 0.5
        else: spec.volume = 0
        pygame.mixer.pre_init(44100,16,2,4096)
        pygame.mixer.music.load("audio/africa.wav")
        pygame.mixer.music.set_volume(spec.volume)
        pygame.mixer.music.play(-1)

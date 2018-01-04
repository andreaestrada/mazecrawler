###############################################################################
#
# Andrea Estrada | arestrad
# 112 F17 TP
# Deals with player <> computer interactions
# 
###############################################################################
import pygame
import spec
import main
import ammo

#cursor for adding a port
def portCursor(data, keyCode, currentState):
    if keyCode == pygame.K_BACKSPACE and spec.port[:spec.cursorIndex] != "" and len(spec.port) > 0: 
        spec.port = str(spec.port)[:spec.cursorIndex-1] + str(spec.port)[spec.cursorIndex:]
        spec.cursorIndex -= 1
    elif keyCode == pygame.K_RIGHT: spec.cursorIndex = min(len(str(spec.port)), spec.cursorIndex+1)
    elif keyCode == pygame.K_LEFT: spec.cursorIndex = max(0, spec.cursorIndex-1)
    elif keyCode == pygame.K_RETURN: 
        connection(currentState, data)

    elif keyCode != pygame.K_BACKSPACE:
        char = chr(keyCode)
        if len(str(spec.port)) < 5: 
            spec.port = str(spec.port)[:spec.cursorIndex] + char + str(spec.port)[spec.cursorIndex:]
            spec.cursorIndex += 1

#cursor for adding your username
def nameCursor(data, keyCode):
    if keyCode == pygame.K_BACKSPACE and spec.myUser[:spec.cursorIndex] != "" and len(spec.myUser) > 0: 
        spec.myUser = str(spec.myUser)[:spec.cursorIndex-1] + str(spec.myUser)[spec.cursorIndex:]
        spec.cursorIndex -= 1
    elif keyCode == pygame.K_RIGHT: spec.cursorIndex = min(len(str(spec.myUser)), spec.cursorIndex+1)
    elif keyCode == pygame.K_LEFT: spec.cursorIndex = max(0, spec.cursorIndex-1)
    elif keyCode == pygame.K_RETURN:
        data.sendUser()
        spec.gameStatus += 1 
    elif keyCode != pygame.K_BACKSPACE:
        char = chr(keyCode)
        if len(str(spec.myUser)) < 7: 
            spec.myUser = str(spec.myUser)[:spec.cursorIndex] + char + str(spec.myUser)[spec.cursorIndex:]
            spec.cursorIndex += 1

#allows for pressing and holding keys to have continuous movement
def pressAndHoldGame(keyCode):
    #player movement
    if keyCode == pygame.K_UP: 
        spec.keys["Up"] = True
        sendKeyMovement = "KeyPressed %s \n" % ("Up")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_DOWN: 
        spec.keys["Down"] = True
        sendKeyMovement = "KeyPressed %s \n" % ("Down")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_RIGHT: 
        spec.keys["Right"] = True
        sendKeyMovement = "KeyPressed %s \n" % ("Right")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_LEFT: 
        spec.keys["Left"] = True
        sendKeyMovement = "KeyPressed %s \n" % ("Left")
        spec.server.send(sendKeyMovement.encode())
    #speed
    if keyCode == pygame.K_a: spec.keys["A"] = True
    if keyCode == pygame.K_s: spec.keys["S"] = True

#allows for pressing and holding keys to have continuous movement
def releaseHoldGame(keyCode):
    #player movement
    if keyCode == pygame.K_UP: 
        spec.keys["Up"] = False
        sendKeyMovement = "KeyUp %s \n" % ("Up")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_DOWN: 
        spec.keys["Down"] = False
        sendKeyMovement = "KeyUp %s \n" % ("Down")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_RIGHT: 
        spec.keys["Right"] = False
        sendKeyMovement = "KeyUp %s \n" % ("Right")
        spec.server.send(sendKeyMovement.encode())
    if keyCode == pygame.K_LEFT: 
        spec.keys["Left"] = False
        sendKeyMovement = "KeyUp %s \n" % ("Left")
        spec.server.send(sendKeyMovement.encode())
    #speed
    if keyCode == pygame.K_a: spec.keys["A"] = False
    if keyCode == pygame.K_s: spec.keys["S"] = False

#spacebar to shoot
def shootAmmo(keyCode):
    if spec.playing and spec.me.ammoOwned and keyCode == pygame.K_SPACE: 
        ammo.Ammunition("Me")
        msg = "Ammunition ExtraneousDetail \n"
        spec.server.send(msg.encode())
        spec.me.ammoOwned -= 1

#checks validity of server connection, joins server
def connection(currentState, data):
    if str(spec.port).isdigit() and int(spec.port) <= 65535 and int(spec.port)>= 10000 and len(str(spec.port)) == 5: 
        if currentState == "Create":
            data.replacePort('spec.py', 13, str(spec.port))
            main.setUpServer(data)
            spec.dontJoin.discard(str(spec.port))
        elif currentState == "Join" and str(spec.port) not in spec.dontJoin and data.myID == -1: 
            try: 
                main.joinServer(data)
            except Exception as ex:
                print(ex)
                spec.dontJoin.add(str(spec.port))

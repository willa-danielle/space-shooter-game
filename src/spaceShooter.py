import pygame, sys
from pygame.locals import *

FPS = 30  #frames per second for the program
WINDOWWIDTH = 400
WINDOWHEIGHT = 500
SHIPWIDTH = 20 #ship is represented as a square of width SHIPWIDTH

BULLETWIDTH = 2 #bullets are represented as tall thin rectangles.
BULLETHEIGHT =8 

BULLETSPEED=10

ENEMYWIDTH = 20
ENEMYHEIGHT = 10 #enemies are wider than tall and are also rectangular

#        R   G   B
BLACK = (0,  0,  0  )
WHITE = (255,255,255)
BLUE  = (0,  0,  255)
GREEN = (0,  255,0  )
ORANGE= (255,165,0  )
RED   = (255,0,  0  )


bgColor = BLACK
bulletColor = RED 

#possible ship-direction values
LEFT="left"
RIGHT="right"
UP="up"
DOWN="down"
STOPPED="stopped"


def main():
    global FPSCLOCK, DISPLAYSURF, shipXCoord, shipYCoord, direction, shipColor, enemyColor
    global shipSpeed, shipBullets
    
    shipSpeed=4
    pygame.init()
    shipColor = BLUE
    enemyColor = ORANGE

    shipBullets=[]

    direction = STOPPED

    shipXCoord = int(WINDOWWIDTH/2) #initial ship position
    shipYCoord = WINDOWHEIGHT
    
    FPSCLOCK = pygame.time.Clock()

    
    pygame.display.set_caption('Space Shooter')
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    playGame()

#---------------- exiting if needed ---------------------------

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.type == QUIT or (event.type == KEYUP and event.key==K_ESCAPE):
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()

#------------------- drawing the game elements ------------------

def drawShip():
    shipRect = pygame.Rect(shipXCoord-SHIPWIDTH, shipYCoord-SHIPWIDTH, SHIPWIDTH, SHIPWIDTH)
    pygame.draw.rect(DISPLAYSURF, shipColor, shipRect)

def drawShipBullets():
    global shipBullets
    for bullet in shipBullets:
        bulletRect = pygame.Rect(bullet[0], bullet[1], BULLETWIDTH, BULLETHEIGHT)
        pygame.draw.rect(DISPLAYSURF, bulletColor, bulletRect)

#------------------- game loop structure------------------------

def playGame():
    global shipColor
    
    while True:        
        checkForQuit()
        DISPLAYSURF.fill(bgColor)
        
        drawShip()
        drawShipBullets()
        pygame.display.update()
        controlShip()
        updateShipPos()
        updateShipBulletPos()
        FPSCLOCK.tick(FPS)
        
#----------------- position functions --------------------------

def updateShipPos():
    global shipXCoord, shipYCoord, shipSpeed, shipColor
    
    if direction==LEFT:
        shipXCoord=shipXCoord-shipSpeed #moves ship at given speed in proper direction
        if shipXCoord<SHIPWIDTH:    #failsafe to prevent going out of bounds
            shipXCoord=SHIPWIDTH
    elif direction==RIGHT:
        shipXCoord=shipXCoord+shipSpeed
        if shipXCoord>WINDOWWIDTH:
            shipXCoord=WINDOWWIDTH
    elif direction==UP:
        shipYCoord=shipYCoord-shipSpeed
        if shipYCoord<SHIPWIDTH:
            shipYCoord=SHIPWIDTH
    elif direction==DOWN:
        shipYCoord=shipYCoord+shipSpeed
        if shipYCoord>WINDOWHEIGHT:
            shipYCoord=WINDOWHEIGHT

def updateShipBulletPos():
    global shipBullets
    for bullet in shipBullets:
        bullet[1] = bullet[1]-BULLETSPEED
        if bullet[1]<0:
            shipBullets.remove(bullet)

def locateShipGunX():
    return shipXCoord-int(SHIPWIDTH/2) #gun is at the middle of ship front

def locateShipGunY():
    return shipYCoord-SHIPWIDTH-BULLETHEIGHT #bullet should start at front of ship and be entirely outside ship

#----------------- controls for ship ---------------------------

def shootIfNeeded(event):
    global shipBullets
    if event.key==K_SPACE:
        shipBullets.append([locateShipGunX(), locateShipGunY()]) #adds a bullet in the appropriate coordinates on pressing spacebar

def nullifyDirectionIfNeeded(event):
    global direction
    if (((event.key==K_DOWN or event.key==K_s) and direction==DOWN) #if user presses a 2nd arrow before releasing 1st arrow, should not stop
        or ((event.key==K_UP or event.key==K_w) and direction==UP)
        or ((event.key==K_RIGHT or event.key==K_d) and direction==RIGHT)
        or ((event.key==K_LEFT or event.key==K_a) and direction==LEFT)):
        direction=STOPPED

def updateDirection(event):
    global direction
    if (event.key==K_LEFT or event.key==K_a): #support for both arrow keys and WASD controls.
        direction=LEFT
    elif (event.key==K_RIGHT or event.key==K_d):
        direction=RIGHT
    elif (event.key==K_UP or event.key==K_w):
        direction=UP
    elif (event.key==K_DOWN or event.key==K_s):
        direction=DOWN


def controlShip():
    for event in pygame.event.get(KEYDOWN):
        updateDirection(event)
        shootIfNeeded(event)
    for event in pygame.event.get(KEYUP):
        nullifyDirectionIfNeeded(event)




if __name__=='__main__':
    main()

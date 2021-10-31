import math
import random
import time
import os
import sys

import pygame
from pygame import Rect, mixer

pygame.init()

# File Setup
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
DATA_FOLDER = os.path.join(APP_FOLDER, "Data")
AUDIO_FOLDER = os.path.join(DATA_FOLDER, "Audio")

# Screen Setup
screenScale = 0.7
screenWidth = int(screenScale * 1920)
screenHeight = int(screenScale * 1080)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Shooter 2: Rewritten")
pygame.display.set_icon(pygame.image.load(os.path.join(DATA_FOLDER, "Player.png")))

# FPS Setup
targetFPS = 60
setFPS = 60
clock = pygame.time.Clock()
prevTime = time.time()
deltaTime = 0

# Settings
volume = 100/100

# Game Objects
class Player:
    def __init__(self, x, y):
        self.acceleration = 0.9 * screenScale
        self.drag = 0.9

        self.alive = True

        self.scale = int(screenHeight/16)
        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Player.png"))
        self.image = pygame.transform.scale(self.image , (self.scale, self.scale))

        self.collisionOffset = self.scale/2

        self.x = x
        self.y = y
        
        self.xInput = 0
        self.yInput = 0

        self.angle = 0

        self.xMovement = 0
        self.yMovement = 0

        self.health = 20
        self.damage = self.health

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Player Death.wav"))
        self.removeSound.set_volume(0.6 * volume)
        
        self.score = 0

    # Gets Inputs
    def getInput(self, event, up, down, left, right):
        if(event.type == pygame.KEYDOWN):
            if(event.key == left):
                self.xInput += -1
            if(event.key == right):
                self.xInput += 1
            if(event.key == up):
                self.yInput += -1
            if(event.key == down):
                self.yInput += 1
        
        if(event.type == pygame.KEYUP):
            if(event.key == left):
                self.xInput -= -1
            if(event.key == right):
                self.xInput -= 1
            if(event.key == up):
                self.yInput -= -1
            if(event.key == down):
                self.yInput -= 1

    # Calculates The Different Movements
    def moveX(self):
        self.xMovement += self.acceleration * self.xInput
        self.xMovement *= self.drag
    
    def moveY(self):
        self.yMovement += self.acceleration * self.yInput
        self.yMovement *= self.drag
    
    # Moves The Player
    def movePlayer(self):
        self.moveX()
        self.moveY()

        # Attempt to normalize movement
        if(self.xInput != 0 and self.yInput != 0):
            self.xMovement *= 0.97
            self.yMovement *= 0.97

        self.x += self.xMovement * deltaTime * targetFPS
        self.y += self.yMovement * deltaTime * targetFPS
        
        if(self.x < 0 - self.scale):
            self.x += screenWidth + self.scale
        if(self.x > screenWidth):
            self.x -= screenWidth + self.scale

        if(self.y < 0 - self.scale):
            self.y += screenHeight + self.scale
        if(self.y > screenHeight):
            self.y -= screenHeight + self.scale
    
    # Finds Angle To Mouse
    def getRelativeAngle(self):
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0]
        mouseY = mousePos[1]
        self.angle = math.degrees(math.atan2(self.y - (mouseY - self.scale / 2), mouseX - (self.x + self.scale / 2)))

    # Draws The player With Rotation
    def drawPlayer(self):
        rotatedPlayerImage = pygame.transform.rotate(self.image, self.angle)
        newRect = rotatedPlayerImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotatedPlayerImage, newRect)

    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Adds To Score
    def addScore(self, score):
        self.score += score

    # Returns True To Remove
    def remove(self, object):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()
            self.alive = False

            explosionList.add(PlayerExplosion(self.x + self.scale / 2 - playerExplosionTemp.scale / 2, self.y + self.scale / 2 - playerExplosionTemp.scale / 2))

            return True
        else:
            self.alive = True
            return False

    # Resets The Player
    def reset(self, x, y):
        self.alive = True

        self.health = 20
        self.damage = self.health

        self.x = x
        self.y = y

        self.xMovement = 0
        self.yMovement = 0

        self.score = 0

    # Runs Most Needed Functions
    def updatePlayer(self):
        self.movePlayer()

        self.getRelativeAngle()
        self.drawPlayer()

class Laser:
    def __init__(self, x, y, direction, speed, player):
        self.x = x
        self.y = y

        self.direction = direction

        self.fireCooldown = 0.1

        self.speed = speed * screenScale

        self.scale = int(screenHeight/104)
        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Laser.png"))
        self.image = pygame.transform.scale(self.image, (int(self.scale*3.5), self.scale))

        self.collisionOffset = self.scale/3

        self.sound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.sound.set_volume(0.1 * volume)

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser Hit.wav"))

        self.health = 1
        self.damage = self.health

        self.origin = player

    # Offsets To Avoid Player
    def offset(self):
        self.x += math.cos(math.radians(self.direction)) * self.scale * 2.75
        self.y += -1 * math.sin(math.radians(self.direction)) * self.scale * 2.75

    # Moves In Direction
    def move(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed * deltaTime * targetFPS
        self.y += -1 * math.sin(math.radians(self.direction)) * self.speed * deltaTime * targetFPS

    # Draws With Rotation
    def draw(self):
        rotatedImage = pygame.transform.rotate(self.image, self.direction)
        newRect = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotatedImage, newRect)
    
    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Returns True To Remove
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            explosionList.add(LaserExplosion(self.x, self.y))

            return True
        else:
            return False

    # Returns True When Out Of Bounds
    def check(self):
        return self.x < -50 or self.x > screenWidth + 50 or self.y < -50 or self.y > screenHeight + 50

class LargeAsteroid:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y

        self.scale = int(screenHeight / 4)
        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Large Asteroid.png"))
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))

        self.collisionOffset = self.scale/2
        
        self.accuracy = 15

        self.direction = 0
        self.getDirection(player)
        self.speed = random.randint(3, 5) * screenScale

        self.angle = random.randint(1,360)
        self.spinDirection = random.randint(1,2)
        if(self.spinDirection == 2):
            self.spinDirection = -1
        self.spinSpeed = random.randint(1,5)

        self.health = 5
        self.damage = self.health

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Big Explosion.wav"))
        self.removeSound.set_volume(0.5 * volume)

        self.score = 20

    # Moves In Direction and rotates
    def move(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed * deltaTime * targetFPS
        self.y += -1 * math.sin(math.radians(self.direction)) * self.speed * deltaTime * targetFPS

        self.angle += self.spinSpeed * self.spinDirection * deltaTime * targetFPS
    
    # Draws With Rotation
    def draw(self):
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        newRect = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotatedImage, newRect)
    
    # Find Angle To Player
    def getDirection(self, player):
        playerX = player.x
        playerY = player.y
        self.direction = math.degrees(math.atan2(self.y - (playerY - self.scale / 2), playerX - (self.x + self.scale / 2))) + random.randint(self.accuracy * -1, self.accuracy)

    # Returns True When Out Of Bounds
    def check(self):
        return self.x < -300 or self.x > screenWidth + 300 or self.y < -300 or self.y > screenHeight + 300
    
    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Removes Health And Checks To See If Removeable
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            # Adds Score If Needed
            if(isinstance(object, Laser)):
                if(isinstance(object.origin, Player)):
                    object.origin.addScore(self.score)

            explosionList.add(LargeAsteroidExplosion(self.x + self.scale / 2 - largeAsteroidExplosionTemp.scale / 2, self.y + self.scale / 2 - largeAsteroidExplosionTemp.scale / 2))

            return True
        else:
            return False

class MediumAsteroid:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y

        self.scale = int(screenHeight / 9)
        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Medium Asteroid.png"))
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))

        self.collisionOffset = self.scale/2
        
        self.accuracy = 60

        self.direction = direction
        self.getDirection()
        self.speed = random.randint(4, 6) * screenScale

        self.angle = random.randint(1,360)
        self.spinDirection = random.randint(1,2)
        if(self.spinDirection == 2):
            self.spinDirection = -1
        self.spinSpeed = random.randint(3,7)

        self.health = 2
        self.damage = self.health

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Medium Explosion.wav"))
        self.removeSound.set_volume(0.3 * volume)

        self.score = 5

    # Moves In Direction and rotates
    def move(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed * deltaTime * targetFPS
        self.y += -1 * math.sin(math.radians(self.direction)) * self.speed * deltaTime * targetFPS

        self.angle += self.spinSpeed * self.spinDirection * deltaTime * targetFPS
    
    # Draws With Rotation
    def draw(self):
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        newRect = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotatedImage, newRect)
    
    # Find Angle To Player
    def getDirection(self):
        self.direction += random.randint(self.accuracy * -1, self.accuracy)

    # Returns True When Out Of Bounds
    def check(self):
        return self.x < -300 or self.x > screenWidth + 300 or self.y < -300 or self.y > screenHeight + 300
    
    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Removes A Health And Checks To See If Removeable
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            # Adds Score If Needed
            if(isinstance(object, Laser)):
                if(isinstance(object.origin, Player)):
                    object.origin.addScore(self.score)

            explosionList.add(MediumAsteroidExplosion(self.x + self.scale / 2 - MediumAsteroidExplosionTemp.scale / 2, self.y + self.scale / 2 - MediumAsteroidExplosionTemp.scale / 2))

            return True
        else:
            return False

# Explosions
class Explosion:
    def __init__ (self, x, y, maxFrame, scale, FRAME_PATH):
        self.x = x
        self.y = y

        self.frame = -1
        self.maxFrame = maxFrame

        self.scale = scale
        self.frames = []
        for i in range(0,self.maxFrame):
            img = pygame.image.load(os.path.join(FRAME_PATH, str(i) + ".png"))
            img = pygame.transform.scale(img, (self.scale, self.scale))
            self.frames.append(img)
    
    def move(self):
        self.frame += 1

    def draw(self):
        if(self.frame<self.maxFrame):
            screen.blit(self.frames[self.frame], (self.x, self.y))

    def check(self):
        return self.frame >= self.maxFrame

class PlayerExplosion(Explosion):
    def __init__ (self, x, y):
        super().__init__(x, y, 15, int(screenHeight/6), os.path.join(DATA_FOLDER, "Player Death"))

class LaserExplosion(Explosion):
    def __init__(self, x, y):
        super().__init__(x, y, 6, int(screenHeight/26), os.path.join(DATA_FOLDER, "Laser Explosion"))

class LargeAsteroidExplosion(Explosion):
    def __init__ (self, x, y):
        super().__init__(x, y, 17, int(screenHeight * 7/16), os.path.join(DATA_FOLDER, "Large Asteroid Explosion"))

class MediumAsteroidExplosion(Explosion):
    def __init__ (self, x, y):
        super().__init__(x, y, 9, int(screenHeight/6), os.path.join(DATA_FOLDER, "Medium Asteroid Explosion"))

# General List
class ObjectList:
    def __init__(self):
        self.list = []

    # Adds Object To The List
    def add(self, object):
        self.list.append(object)

    # Moves All Objects In List
    def move(self):
        for object in self.list:
            object.move()
    
    # Draws All Objects In List
    def draw(self):
        for object in self.list:
            object.draw()
    
    # Checks If Object Should Be Removed And If So, Removes It
    def remove(self, object, object2, explosionList):
        if(object.remove(object2, explosionList) == True):
            if(self.checkContains(object)):
                self.list.remove(object)
                return True
        return False

    # Check If Object Is In List
    def checkContains(self, quarry):
        for object in self.list:
            if(object == quarry):
                return True
        
        return False

    # Check All Objects In List
    def check(self):
        for object in self.list:
            if(object.check() == True):
                self.list.remove(object)

    # Clears Entire List
    def clear(self):
        self.list.clear()

    # Runs All Appropiate Functions
    def update(self):
        self.move()

        self.check()

        self.draw()

# UI
# Graphics
class Title:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

        self.scale = int(screenHeight/1.75)

        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Name.png"))
        self.image = pygame.transform.scale(self.image, (self.scale * 2, self.scale))
        
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Text:
    def __init__(self, x, y,  colour,size):
        self.x = x
        self.y = y

        self.colour = colour

        self.font = pygame.font.Font(os.path.join(DATA_FOLDER, "Moonrising.ttf"), size)

    # Draw From The Left    
    def drawCentered(self, text):
        textRendered = self.font.render(str(text), True, self.colour)
        screen.blit(textRendered, (self.x, self.y)) 

    # Draw From The Center    
    def drawCentered(self, text):
        textRendered = self.font.render(str(text), True, self.colour)
        textRect = textRendered.get_rect()
        screen.blit(textRendered, (self.x - (textRect.right - textRect.left)/2, self.y)) 

    # Draw From The Right
    def drawRight(self, text):
        textRendered = self.font.render(str(text), True, self.colour)
        textRect = textRendered.get_rect()
        screen.blit(textRendered, (self.x - (textRect.right - textRect.left), self.y)) 
    
class Bar:
    def __init__ (self, x, y, width, height, backColour, fillColour):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.backColour = backColour

        self.fillColour = fillColour

        self.backRect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, fillTotal, fillAmount):
        # Background
        pygame.draw.rect(screen, self.backColour, self.backRect)

        # Fill
        fillRect = Rect(self.x - 2 ,self.y + 2, self.width * fillAmount/fillTotal, self.height - 4)
        pygame.draw.rect(screen, self.fillColour, fillRect)

# Buttons
class StartButton:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.selected = False

        self.scale = int(screenHeight/5)

        self.image = pygame.image.load(os.path.join(DATA_FOLDER, "Start Button.png"))
        self.image = pygame.transform.scale(self.image, (int(self.scale * 2.3), self.scale))

        self.pressedSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.pressedSound.set_volume(0.6 * volume)

        self.rect = self.image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
    
    # Checks it mouse is over the button, and if it's pressed
    def check(self, mousePos, mouseState):
        # If mouse is over the button
        if(self.rect.collidepoint(mousePos)):
            self.angle = math.sin(time.time()*10)

            if(mouseState[0] == True):
                self.pressedSound.play()
                return True
        else:
            self.angle = 0
        
        return False

    # Draw Button
    def draw(self):
        rotatedImage = self.image

        # If selected, enlarge slightly
        if(self.selected == True):
            rotatedImage = pygame.transform.scale(rotatedImage, (int(self.scale * 2.3 * 1.1), int(self.scale * 1.1)))
        
        # Rotate The Image
        rotatedImage = pygame.transform.rotate(rotatedImage, self.angle * 5)
        newRect = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)

        screen.blit(rotatedImage, newRect)

# Functions
def findAsteroidSpawn():
    side = random.randint(1,4)

    if(side == 1):
        position = random.randint(-20, screenHeight + 20)
        return (-200, position)
    elif(side == 2):
        position = random.randint(-20, screenWidth + 20)
        return (position, -200)
    elif(side == 3):
        position = random.randint(-20, screenHeight + 20)
        return (200 + screenWidth, position)
    elif(side == 4):
        position = random.randint(-20, screenWidth + 20)
        return (position, 200 + screenHeight)

def CheckCircleCollision(x, y, x2, y2, range):
    distance = math.sqrt(math.pow((x - x2), 2) + math.pow((y - y2), 2))
    if(distance < range):
        return True
    return False

def checkListCollisions(list1, list2):
    for object1 in list1.list:
        for object2 in list2.list:
            if(CheckCircleCollision(object1.x + object1.collisionOffset, object1.y + object1.collisionOffset, object2.x + object2.collisionOffset, object2.y + object2.collisionOffset, object1.scale*9/16 + object2.scale*9/16)):
                if(object1 != object2):
                    # Tries To Remove Objects
                    object1Removed = list1.remove(object1, object2, explosionList)
                    object2Removed = list2.remove(object2, object1, explosionList)

                    # Update Damage If Needed
                    if(object1Removed != True):
                        object1.damage = object1.health
                    if(object2Removed != True):
                        object2.damage = object2.health

                    # Adds Debris And Such
                    if(isinstance(object1, LargeAsteroid) and object1Removed):
                        for l in range(random.randint(2,4)):
                            asteroidList.add(MediumAsteroid(object1.x, object1.y, object1.direction))
                    elif(isinstance(object2, LargeAsteroid) and object2Removed):
                        for l in range(random.randint(2,4)):
                            asteroidList.add(MediumAsteroid(object2.x, object2.y, object2.direction))

def checkPlayerCollisions(player, list):
    for object2 in list.list:
        if(CheckCircleCollision(player.x + player.collisionOffset, player.y + player.collisionOffset, object2.x + object2.collisionOffset, object2.y + object2.collisionOffset, player.scale*9/16 + object2.scale*9/16)):
            playerRemoved = player.remove(object2)
            object2Removed = list.remove(object2, player, explosionList)

            if(playerRemoved != True):
                player.damage = player.health
            if(object2Removed != True):
                object2.damage = object2.health
        
            # Adds Debris If needed
            if(isinstance(object2, LargeAsteroid) and object2Removed):
                for l in range(random.randint(2,4)):
                    asteroidList.add(MediumAsteroid(object2.x, object2.y, object2.direction))

# Temps !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! REMOVE NEED FOR TEMPS
playerTemp = Player(0,0)
playerExplosionTemp = PlayerExplosion(0,0)
laserTemp = Laser(0 ,0 ,0, 12, playerTemp)
largeAsteroidExplosionTemp = LargeAsteroidExplosion(0,0)
MediumAsteroidExplosionTemp = MediumAsteroidExplosion(0,0)
startButtonTemp = StartButton(0,0)
titleTemp = Title(0,0)

# Players
player = Player(screenWidth/2, screenHeight/2)

# Laser
laserPrevTime = time.time()
laserList = ObjectList()

# Asteroids
asteroidList = ObjectList()

# Explosions
explosionList = ObjectList()

# Graphics
title = Title((screenWidth - titleTemp.scale * 2) / 2, screenHeight * 1/3 - titleTemp.scale/2)
healthBar = Bar(screenHeight/40, screenHeight / 40, screenWidth/6, screenHeight/16, (50,50,50), (18, 161, 58))
score = Text(screenWidth * 39/40, screenHeight / 39, (255,255,255), int(screenHeight/25))

finalScore = Text(screenWidth / 2, screenHeight /3, (255,255,255), int(screenHeight / 7))

# Buttons
startButton = StartButton((screenWidth - startButtonTemp.scale * 2.3) / 2, screenHeight * 2/3)

# Main Loop
playing = True
while(playing):
    # Setup
    timeCount = 0
    frequency = 0
    deathTime = 0
    
    gameState = "menu"

    running = True
    # Game Loop
    while(running):
        # FPS Limit
        clock.tick(setFPS)

        # Calculate Delta Time
        deltaTime = time.time() - prevTime
        prevTime = time.time()

        timeCount += deltaTime

        # Loop Through Key Input Events
        for event in pygame.event.get():
            # Quit
            if(event.type == pygame.QUIT):
                running = False
                playing = False
                break
            
            # Player Movement
            player.getInput(event, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

            # Keydown
            if(event.type == pygame.KEYDOWN):
                # Escape / Quit
                if(event.key == pygame.K_ESCAPE):
                    running = False
                    break
        
        # Get Mouse Input
        mousePos = pygame.mouse.get_pos()
        mouseState = pygame.mouse.get_pressed(num_buttons = 3)

        # Background
        screen.fill((0,0,0))

        # Run Games
        if(gameState == "menu"):
            if(startButton.check(mousePos, mouseState)):
                gameState = "main"
                timeCount = 0
            
            startButton.draw()
            title.draw()

        if(gameState == "main"):
            # Small Wait Right After Starting
            if(timeCount < 0.2):
                continue

            # Player Shooting
            # Fire If Left Mouse Down And Time Since Last Firing Is Longer Than Cooldown
            if(mouseState[0] == True and time.time() - laserPrevTime >= laserTemp.fireCooldown and player.alive):
                laserAdder = Laser(player.x + player.scale/2 - laserTemp.scale*3/2, player.y + player.scale/2 - laserTemp.scale/2, player.angle, 12, player)
                laserAdder.offset()
                laserAdder.sound.play()
                laserList.add(laserAdder)
                laserPrevTime = time.time()

            # Asteroid Spawning System
            if(timeCount < 50):
                frequency = timeCount
            else:
                frequency = 50
            
            if(timeCount - int(timeCount) < 0.1 and int(timeCount) % 2 == 0):
                randnum = random.randint(0,100)
                if(randnum < frequency):
                    pos = findAsteroidSpawn()
                    asteroidList.add(LargeAsteroid(pos[0], pos[1], player))

            # Check Collisions Between Lasers and Asteroids
            checkListCollisions(laserList, asteroidList)
            
            # Check Collisions If Player Is Alive
            if(player.alive):
                checkPlayerCollisions(player, asteroidList)

            # Process Asteroids
            asteroidList.update()

            # Process Lasers
            laserList.update()

            # Process Explosions
            explosionList.update()

            # Process Player
            if(player.alive == True):
                player.updatePlayer()
            else:
                # Wait After Dying
                if(deathTime == 0):
                    deathTime = timeCount
                elif(timeCount - deathTime > 4):
                    gameState = "death"
            
            # UI
            healthBar.draw(playerTemp.health, player.health)

            score.drawRight(player.score)

        if(gameState == "death"):
            finalScore.drawCentered(player.score)
            if(timeCount - (deathTime + 4) > 4):
                gameState = "restart"

        if(gameState == "restart"):
            running = False

        pygame.display.update()

    # Reset for next round
    player.reset(screenWidth/2, screenHeight/2)
    laserList.clear()
    asteroidList.clear()
    explosionList.clear()

    pygame.mixer.stop()

pygame.quit()
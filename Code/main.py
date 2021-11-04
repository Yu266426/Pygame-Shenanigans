import random
import time
import os

import pygame

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *

from data.code.Player import Player
from data.code.Laser import Laser
from data.code.LargeAsteroid import LargeAsteroid
from data.code.MediumAsteroid import MediumAsteroid

from data.code.Title import Title
from data.code.Text import Text
from data.code.Bar import Bar
from data.code.StartButton import StartButton

# Initalization
pygame.init()
pygame.mixer.init()

# Limit Events
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Shooter 2")

icon = pygame.image.load(os.path.join(ASSET_FOLDER, "Player.png")).convert_alpha()
pygame.display.set_icon(icon)

# FPS Setup
targetFPS = 60
setFPS = 60
clock = pygame.time.Clock()
prevTime = time.time()
deltaTime = 0

# Functions
def findAsteroidSpawn():
    side = random.randint(1,4)

    if(side == 1):
        position = random.randint(-20, screenHeight + 20)
        return (float(-200), float(position))
    elif(side == 2):
        position = random.randint(-20, screenWidth + 20)
        return (float(position), float(-200))
    elif(side == 3):
        position = random.randint(-20, screenHeight + 20)
        return (float(200 + screenWidth), float(position))
    elif(side == 4):
        position = random.randint(-20, screenWidth + 20)
        return (float(position), float(200 + screenHeight))

def asteroidLaserIntersection(list):
    for asteroid in list:
        for laser in list[asteroid]:
            asteroid.remove(laser, explosionList)
            laser.remove(asteroid, explosionList)

            if(asteroid.alive()):
                asteroid.damage = asteroid.health
            
            if(laser.alive()):
                laser.damage = laser.health
        
        if(isinstance(asteroid, LargeAsteroid) and asteroid.alive() == False):
            for l in range(random.randint(2,4)):
                asteroidList.add(MediumAsteroid(asteroid.rect.center, asteroid.direction))

def playerAsteroidIntersection(list):
    for player in list:
        for asteroid in list[player]:
            player.remove(asteroid, explosionList)

            asteroid.remove(player, explosionList)

            if(player.alive()):
                player.damage = player.health

            if(asteroid.alive()):
                asteroid.damage = asteroid.health
            
            if(isinstance(asteroid, LargeAsteroid) and asteroid.alive() == False):
                for l in range(random.randint(2,4)):
                    asteroidList.add(MediumAsteroid(asteroid.rect.center, asteroid.direction))

# Players
player = pygame.sprite.GroupSingle(Player((float(screenWidth/2), float(screenHeight/2))))

# Laser
laserPrevTime = time.time()
laserList = pygame.sprite.Group()

# Asteroids
asteroidList = pygame.sprite.Group()

# Explosions
explosionList = pygame.sprite.Group()

# Graphics
title = pygame.sprite.GroupSingle(Title(((screenWidth - titleScale[0]) / 2, screenHeight * 1/3 - titleScale[1] / 2)))

healthBar = Bar(screenHeight / 40, screenHeight / 40, screenWidth/6, screenHeight/16, (50,50,50), (18, 161, 58))
score = Text(screenWidth * 39/40, screenHeight / 39, (255,255,255), int(screenHeight/25))

ScoreText = Text(screenWidth / 2, screenHeight / 3, (255,255,255), int(screenHeight / 7))
highScoreText = Text(screenHeight / 40, screenHeight / 40, (220,220,220), int(screenHeight / 20))

restartInfoText = Text(screenWidth /2, screenHeight * 5/8, (200,200,200), int(screenHeight / 16))

# Buttons
startButton = StartButton((screenWidth - startButtonScale[0]) / 2, screenHeight * 2/3)

# Variables
scoreKeeper = player.sprite.score
highScore = 0

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
            if(player.sprite != None):
                player.sprite.getInput(event, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

            # Keydown
            if(event.type == pygame.KEYDOWN):
                # Escape / Quit
                if(event.key == pygame.K_ESCAPE):
                    running = False
                    playing = False

                # Restart If Dead
                if(event.key == pygame.K_SPACE):
                    if(gameState == "death"):
                        gameState = "restart"
        
        # Get Mouse Input
        mousePos = pygame.mouse.get_pos()
        mouseState = pygame.mouse.get_pressed(num_buttons = 3)

        # Background
        screen.fill((0,0,0))

        # Run Games
        if(gameState == "menu"):
            # Checks If Mouse Is Over/Clicking Button
            if(startButton.check(mousePos, mouseState)):
                gameState = "main"
                timeCount = 0
            
            startButton.draw(screen)
            title.draw(screen)

        if(gameState == "main"):
            # Small Wait Right After Starting
            if(timeCount < 0.2):
                continue

            # Player Shooting
            # Fire If Left Mouse Down And Time Since Last Firing Is Longer Than Cooldown
            if(mouseState[0] == True and time.time() - laserPrevTime >= laserFireCooldown and player.sprite != None):
                laserAdder = Laser((float(player.sprite.rect.center[0] - laserScale[0] / 2), float(player.sprite.rect.center[1] - laserScale[1] / 2)), player.sprite.angle, 12, player.sprite)
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
                    pos = findAsteroidSpawn() ###################### Make exception due to the checks deleting after spawning
                    if(player.sprite != None):
                        asteroidList.add(LargeAsteroid(pos, player.sprite.rect.center))
                    else:
                        asteroidList.add(LargeAsteroid(pos, (0,0)))

            # Check Collisions Between Lasers and Asteroids
            asteroidLaserIntersection(pygame.sprite.groupcollide(asteroidList, laserList, False, False, pygame.sprite.collide_circle))
            
            # Check Collisions If Player Is Alived
            if(player.sprite != None):
                playerAsteroidIntersection(pygame.sprite.groupcollide(player, asteroidList, False, False, pygame.sprite.collide_circle))

            # Process Asteroids
            asteroidList.update(deltaTime, targetFPS)

            # Process Lasers
            laserList.update(deltaTime, targetFPS)

            # Process Explosions
            explosionList.update()

            # Process Player
            if(player.sprite != None):
                player.update()
            else:
                # Wait After Dying
                if(deathTime == 0):
                    deathTime = timeCount
                elif(timeCount - deathTime > 4):
                    gameState = "death"
            
            # Draw Everything
            asteroidList.draw(screen)

            laserList.draw(screen)

            if(player.sprite != None):
                player.draw(screen)

            explosionList.draw(screen)

            if(player.sprite != None):
                scoreKeeper = player.sprite.score

            # UI
            if(player.sprite != None):
                healthBar.draw(playerStartingHealth, player.sprite.health, screen)
            else:
                healthBar.draw(playerStartingHealth, 0, screen)

            score.drawRight(scoreKeeper, screen)

        if(gameState == "death"):
            # Save High Score
            highScore = max(highScore, scoreKeeper)

            # Render Score
            ScoreText.drawCentered(str(scoreKeeper), screen)

            # Render High Score
            highScoreText.drawLeft("HIGHSCORE: " + str(highScore), screen)

            # Tells You To Press Space
            restartInfoText.drawCentered("PRESS SPACE TO RESTART", screen)

        if(gameState == "restart"):
            running = False
        
        pygame.display.update()

    # Reset for next round
    player.empty()
    player.add(Player((float(screenWidth/2), float(screenHeight/2))))
    laserList.empty()
    asteroidList.empty()
    explosionList.empty()

    pygame.mixer.stop()

pygame.quit()
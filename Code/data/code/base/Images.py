import os

import pygame

from data.code.base.Constants import playerExplosionScale, laserExplosionScale, largeAsteroidExplosionScale, mediumAsteroidExplosionScale
from data.code.base.FileSetup import ASSET_FOLDER, EXPLOSION_FOLDER


def getImageSequence(path, scale, sequence):
    for directory, folders, images in os.walk(path):
        for image in images:
            imagePath = os.path.join(path, image)

            tempImage = pygame.image.load(imagePath).convert_alpha()
            tempImage = pygame.transform.scale(tempImage, scale)

            sequence.append(tempImage)


# pygame.image.load().convert_alpha()

playerImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Player.png")).convert_alpha()
playerExplosion = []
getImageSequence(os.path.join(EXPLOSION_FOLDER, "Player Death Explosion"), playerExplosionScale, playerExplosion)

laserImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Laser.png")).convert_alpha()
laserExplosion = []
getImageSequence(os.path.join(EXPLOSION_FOLDER, "Laser Explosion"), laserExplosionScale, laserExplosion)

largeAsteroidImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Large Asteroid.png")).convert_alpha()
largeAsteroidExplosion = []
getImageSequence(os.path.join(EXPLOSION_FOLDER, "Large Asteroid Explosion"), largeAsteroidExplosionScale, largeAsteroidExplosion)

mediumAsteroidImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Medium Asteroid.png")).convert_alpha()
mediumAsteroidExplosion = []
getImageSequence(os.path.join(EXPLOSION_FOLDER, "Medium Asteroid Explosion"), mediumAsteroidExplosionScale, mediumAsteroidExplosion)

titleImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Title.png")).convert_alpha()

startButtonImage = pygame.image.load(os.path.join(ASSET_FOLDER, "Start Button.png")).convert_alpha()

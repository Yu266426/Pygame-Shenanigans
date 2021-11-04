# Screen Setup
screenScale = 0.7
screenWidth = int(screenScale * 1920)
screenHeight = int(screenScale * 1080)

# Game Settings
largeAsteroidAccuracy = 15
mediumAsteroidAccuracy = 60

playerStartingHealth = 20

# Object Scales
playerScale = (int(screenHeight/16), int(screenHeight/16))
playerExplosionScale = (int(screenHeight/6), int(screenHeight/6))

laserScale = (int(screenHeight/104 * 3.5), int(screenHeight/104))
laserExplosionScale = (int(screenHeight/26), int(screenHeight/26))

largeAsteroidScale = (int(screenHeight / 4), int(screenHeight / 4))
largeAsteroidExplosionScale = (int(screenHeight * 7/16), int(screenHeight * 7/16))

mediumAsteroidScale = (int(screenHeight / 9), int(screenHeight / 9))
mediumAsteroidExplosionScale = (int(screenHeight/6), int(screenHeight/6))

titleScale = (int(screenHeight/1.75) * 2, int(screenHeight/1.75))

startButtonScale = (int(screenHeight/5 * 2.3), int(screenHeight/5))

# Changing
laserFireCooldown = 0.1
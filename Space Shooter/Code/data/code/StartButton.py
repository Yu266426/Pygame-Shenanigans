from pygame import mixer

from data.code.base.Button import Button
from data.code.base.Constants import *
from data.code.base.FileSetup import *
from data.code.base.Images import startButtonImage


class StartButton(Button):
    def __init__(self, pos):
        super().__init__(startButtonScale, startButtonImage, pos, mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav")), 0.6)

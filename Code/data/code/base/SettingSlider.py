import json

from data.code.base.FileSetup import *
from data.code.base.Slider import Slider

class SettingsSlider(Slider):
    def __init__(self, pos, size, startingLevel):
        super().__init__(pos, size, startingLevel)
        
        self.settingsFile = open(SETTINGS_FILE)
        self.settingsJSON = json.load(self.settingsFile)
        self.settingsFile.close()

    def changeSetting(self, setting):
        if self.selected:
            if self.settingsFile.closed:
                self.settingsFile = open(SETTINGS_FILE, "w")
            
            self.settingsJSON[setting] = round(self.fillAmount, 2)
            
        else:
            if not self.settingsFile.closed:
                json.dump(self.settingsJSON, self.settingsFile)
                self.settingsFile.close()

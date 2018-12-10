from Object import Object
from enum import Enum

class EButtonStatus(Enum):
    blank = 0
    withBox = 1

class Button(Object):
    buttonWithBoxPixmap = None
    buttonWithBoxPixmap0 = None
    buttonPixmap = None

    def setButtonWithBoxPixmap(buttonWithBoxPixmap):
        Button.buttonWithBoxPixmap = buttonWithBoxPixmap

    def setButtonPixmap(buttonPixmap):
        Button.buttonPixmap = buttonPixmap

    def __init__(self, x , y, pixmap):
        super().__init__(x, y, pixmap)
        self.status = EButtonStatus.blank

    def changeStatus(self, staus):
        self.status = staus
        print('ChangStatus Called')
        if self.status == EButtonStatus.blank:
            self.setPixmap(self.buttonPixmap)
        elif self.status == EButtonStatus.withBox:
            self.setPixmap(self.buttonWithBoxPixmap)
        self.applySize()
        pass

    def setStatus(self, status):
        self.status = status
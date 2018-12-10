from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class Object(QLabel):
    positionOffsetX = 0
    positionOffsetY = 0
    size = 32
    qWidget = None

    def __init__(self, x , y , pixmap):
        super().__init__(Object.qWidget)
        self.setPixmap(pixmap)
        self.setPixmap(pixmap.scaled(Object.size, Object.size, Qt.KeepAspectRatio))
        self.setVisible(1)
        self.x = x
        self.y = y
        super().move(self.x * Object.size + Object.positionOffsetX, self.y * Object.size + Object.positionOffsetY)

    def setQWidget(qWidget):
        Object.qWidget = qWidget

    def setPositionOffset(x, y):
        Object.positionOffsetX = x
        Object.positionOffsetY = y

    def setPositionOffsetX(x):
        Object.positionOffsetX = x

    def setPositionOffsetY(y):
        Object.positionOffsetY = y

    def setSize(size):
        Object.size = size

    def applySize(self):
        self.setPixmap(self.pixmap().scaled(Object.size, Object.size, Qt.KeepAspectRatio))

    def draw(self):
        self.setVisible(1)

    def erase(self):
        self.setVisible(0)

    def move(self, x, y):
        self.x += x
        self.y += y
        super().move(self.x * Object.size + Object.positionOffsetX, self.y * Object.size + Object.positionOffsetY)

    def jump(self, x, y):
        self.x = x
        self.y = y
        super().move(self.x * Object.size + Object.positionOffsetX, self.y * Object.size + Object.positionOffsetY)
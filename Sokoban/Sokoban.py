import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont
from Object import Object
from Box import Box
from Blank import Blank
from Player import Player
from Wall import Wall
from Button import Button, EButtonStatus
from enum import Enum
import MapData
import random
import gc


class EObjects:
    EBlank = 0
    EPlayer = 1
    EBox = 2
    EButton = 3
    EWall = 4
    EBlankWithNoGlass = 5


class EGameStatus(Enum):
    EMenu = 0
    EPlaying = 1


def randomPercent(double):
    if random.random() < double:
        return True
    else:
        return False


class App(QWidget):
    # Player reference
    player = None

    def __init__(self):
        super().__init__()

        # 이미지를 로드한다.
        self.boxPixmap = QPixmap('Resource/CatBox.png')
        self.buttonWithBoxPixmap = QPixmap('Resource/ButtonWithBox.png')
        self.buttonWithBoxPixmap0 = QPixmap('Resource/ButtonWithBox0.png')
        self.buttonPixmap = QPixmap('Resource/Button.png')
        self.playerPixmap = QPixmap('Resource/Player1.png')
        self.blankPixmap0 = QPixmap('Resource/Blank0.png')
        self.blankPixmap1 = QPixmap('Resource/Blank1.png')
        self.blankPixmap2 = QPixmap('Resource/Blank2.png')
        self.blankPixmap3 = QPixmap('Resource/Blank3.png')
        self.wallPixmap = QPixmap('Resource/Wall.png')
        self.backgroundPixmap = QPixmap('Resource/Background.png')

        # 박스 default Pixmap 설정
        Button.setButtonPixmap(self.buttonPixmap)
        Button.setButtonWithBoxPixmap(self.buttonWithBoxPixmap)

        # 상태 설정
        self.status = EGameStatus.EPlaying

        # 윈도우 제목 설정 및 화면 크기 설정
        self.title = '고양이는 박스가 필요해'
        self.setWindowTitle(self.title)
        self.width = 640
        self.height = 640
        self.setFixedHeight(self.height)
        self.setFixedWidth(self.width)

        # 배경 출력
        Object.setQWidget(self)
        Object.setSize(self.width)  # 배경의 크기는 화면의 길이와 같음
        self.background = Object(0, 0, self.backgroundPixmap)
        self.background.draw()
        Object.setSize(64)

        # 버튼 만들기
        self.backButton = QPushButton('Back', self)
        resetButton = QPushButton('Reset', self)
        self.nextButton = QPushButton('Next', self)
        self.nextButton.setEnabled(False)

        self.backButton.setFocusPolicy(Qt.NoFocus)
        resetButton.setFocusPolicy(Qt.NoFocus)
        self.nextButton.setFocusPolicy(Qt.NoFocus)

        # 버튼 위치 이동
        self.backButton.move(0, 610)
        resetButton.move(self.width / 3 * 1 + 45, 610)
        self.nextButton.move(self.width / 3 * 2 + 100, 610)

        # 버튼 크기 조절
        self.backButton.setFixedHeight(30)
        resetButton.setFixedHeight(30)
        self.nextButton.setFixedHeight(30)

        # 함수 연결
        self.backButton.clicked.connect(self.onClickBack)
        resetButton.clicked.connect(self.onClickReset)
        self.nextButton.clicked.connect(self.onClickNext)

        # 폰트 만들기
        font = QFont('Times', 20, QFont.Bold)

        # text 만들기
        self.stageText = QLabel('Stage: ', self)
        self.stageText.setFont(font)
        self.stageText.setStyleSheet('color: white')
        self.stageText.setFixedWidth(200)

        self.goalText = QLabel('Goal:', self)
        self.goalText.setFont(font)
        self.goalText.setStyleSheet('color: white')
        self.goalText.setFixedWidth(200)
        self.goalText.move(240, 0)

        self.stepText = QLabel('Step:', self)
        self.stepText.setFont(font)
        self.stepText.setStyleSheet('color: white')
        self.stepText.setFixedWidth(200)
        self.stepText.move(475, 0)

        # 피클을 통해 로드해야 하는 mapData
        self.mapData = None

        # 데이터 로딩
        self.loadData()

        # 현재 화면의 오브젝트들이 들어있는 리스트(blank를 저장하기 위해 사용)
        self.blankList = []

        # 게임 데이터로부터 복사받을 리스트. 배열 내의 위치는 실제 위치와 같음
        self.currentStage = []

        self.step = 0  # 움직인 횟수
        self.currentLevel = 0  # 현재 스테이지
        self.maxStage = len(self.mapData)
        self.goal = 0
        self.show()

        # 게임 데이터를 복사받음(깊은 복사로 해야되는데 일단 앝을 복사로 함)
        self.loadStage(self.currentLevel)

    def onClickBack(self):
        print('Back Pressed')
        if self.currentLevel > 0:
            self.currentLevel -= 1
            self.loadStage(self.currentLevel)

    def onClickReset(self):
        print('Reset Pressed')
        self.loadStage(self.currentLevel)

    def onClickNext(self):
        print('Next Pressed')

        if (self.currentLevel < self.maxStage - 1):
            self.currentLevel += 1
            print('Load Next Level')
            self.loadStage(self.currentLevel)
        else:
            print('End Of Game')

    def loadData(self):
        # 피클을 통해 해야하지만 임시로 데이터를 직접 넣음

        self.mapData = MapData.contents
        print(self.mapData)
        '''
        self.mapData = [
            [
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EButton, EObjects.EBlank, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBox, EObjects.EBlank, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EButton, EObjects.EBox, EObjects.EPlayer, EObjects.EBox, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBox, EObjects.EBlank, EObjects.EBlank,EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EButton, EObjects.EBlank, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall]
            ],
            [
                [EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBox, EObjects.EBox, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EPlayer, EObjects.EButton, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
            ],
            [
                [EObjects.EBlankWithNoGlass, EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EButton, EObjects.EBox, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBox, EObjects.EPlayer, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall]
            ],
            [
                [EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBox, EObjects.EBox, EObjects.EPlayer, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EWall, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
            ],
            [
                [EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EPlayer, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EWall],
                [EObjects.EBlankWithNoGlass, EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBox, EObjects.EBox, EObjects.EBox, EObjects.EBlank, EObjects.EBlank, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EBlank, EObjects.EWall, EObjects.EWall, EObjects.EBlank,EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EButton, EObjects.EButton, EObjects.EButton, EObjects.EWall],
                [EObjects.EWall, EObjects.EBlank, EObjects.EBlank, EObjects.EBlank, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall],
                [EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall, EObjects.EWall]
            ]
        ]
        '''

    def loadStage(self, number):
        self.eraseStage()
        self.currentStage = [[] for i in range(0, len(self.mapData[number]))]
        self.blankList = []
        self.step = 0
        goalNum = 0
        self.nextButton.setEnabled(False)
        if number == 0:
            self.backButton.setEnabled(False)
        else:
            self.backButton.setEnabled(True)

        gc.collect()

        self.stageText.setText('Stage: ' + str(number + 1))
        self.stepText.setText('Step: ' + str(self.step))
        self.currentLevel = number

        # 게임 화면을 중앙으로
        x = (self.width - Object.size * len(self.mapData[number][0])) * 0.5
        y = (self.height - Object.size * len(self.mapData[number])) * 0.5
        Object.setPositionOffset(x, y + 40)

        for y in range(0, len(self.mapData[number])):
            for x in range(0, len(self.mapData[number][y])):
                # 일단 모든 맵을 공백으로 채운다. blankList에 blank를 추가한다.
                print(type(self.mapData[number][y][x]),type(EObjects.EPlayer), y, x)
                if self.mapData[number][y][x] != EObjects.EBlankWithNoGlass:
                    if randomPercent(0.1):
                        blank = Blank(x, y, self.blankPixmap1)
                    elif randomPercent(0.05):
                        blank = Blank(x, y, self.blankPixmap2)
                    elif randomPercent(0.02):
                        blank = Blank(x, y, self.blankPixmap3)
                    else:
                        blank = Blank(x, y, self.blankPixmap0)
                    self.blankList.append(blank)
                    blank.lower()
                    # pass
                    self.background.stackUnder(blank)

                if self.mapData[number][y][x] == EObjects.EBox:
                    box = Box(x, y, self.boxPixmap)
                    self.currentStage[y].append(box)
                    box.raise_()
                elif self.mapData[number][y][x] == EObjects.EPlayer:
                    playerStartX = x
                    playerStartY = y
                    print('Player found!')

                    blank = Blank(x, y, self.blankPixmap0)
                    self.currentStage[y].append(blank)
                    blank.erase()
                elif self.mapData[number][y][x] == EObjects.EWall:
                    self.currentStage[y].append(Wall(x, y, self.wallPixmap))
                elif self.mapData[number][y][x] == EObjects.EButton:
                    goalNum += 1
                    self.currentStage[y].append(Button(x, y, self.buttonPixmap))
                elif self.mapData[number][y][x] == EObjects.EBlank or self.mapData[number][y][
                    x] == EObjects.EBlankWithNoGlass:
                    blank = Blank(x, y, self.blankPixmap0)
                    self.currentStage[y].append(blank)
                    blank.erase()

        self.goal = goalNum
        self.goalText.setText('Goal: ' + str(self.goal))

        # ordering을 위해 player는 마지막에 생성한다!
        App.player = Player(playerStartX, playerStartY, self.playerPixmap)
        # self.currentStage[playerStartY].insert(playerStartX, self.player)

    def drawMap(self):
        # Layer0 상호작용 하지 않는 고정된 Object. 리스트 내의 순서와 위치가 무관
        for object in self.blankList:
            object.draw()

        # Layer1 상호작용하는 Object로 currentStage에 들어있는 것들. 리스트 내 순서 = 실제 위치!
        for y in range(0, len(self.currentStage)):
            for x in range(0, len(self.currentStage[y])):
                self.currentStage[y][x].draw()

    def keyPressEvent(self, event):
        self.canKeyboardInput = True
        key = event.key()

        if self.status == EGameStatus.EPlaying:

            if self.player is None:
                print('Null player')
                return

            # delta 값 초기화
            deltaX = 0
            deltaY = 0

            if key == Qt.Key_Left:
                # print('Left Arrow Pressed')
                deltaX = -1
                deltaY = 0
            elif key == Qt.Key_Right:
                # print('Right Arrow Pressed')
                deltaX = 1
                deltaY = 0
            elif key == Qt.Key_Up:
                # print('Up Arrow Pressed')
                deltaX = 0
                deltaY = -1
            elif key == Qt.Key_Down:
                # print('Down Arrow Pressed')
                deltaX = 0
                deltaY = 1
            elif key == Qt.Key_R:
                self.onClickReset()
                return
            elif key == Qt.Key_1:
                if self.backButton.isEnabled():
                    self.onClickBack()
                return
            elif key == Qt.Key_2:
                if self.nextButton.isEnabled():
                    self.onClickNext()
                return
            else:
                return

            # currentStage에 있는 object들
            deltaObject = self.currentStage[App.player.y + deltaY][App.player.x + deltaX]
            playerPositionOnStage = self.currentStage[App.player.y][App.player.x]
            deltaClassName = type(deltaObject).__name__

            # 끔찍한 코드... 더 낫게 할 수 없을까?
            if deltaClassName == 'Blank':
                print('You can go (Blank)')
                self.gamePlayerMove(deltaX, deltaY)
            elif deltaClassName == 'Button':
                if deltaObject.status == EButtonStatus.blank:
                    print('You can go (Button-Blank)')
                    self.gamePlayerMove(deltaX, deltaY)
                elif deltaObject.status == EButtonStatus.withBox:
                    doubleDeltaObject = self.currentStage[App.player.y + deltaY * 2][App.player.x + deltaX * 2]
                    doubleDeltaClassName = type(doubleDeltaObject).__name__

                    if doubleDeltaClassName == 'Blank':
                        print('You can go (Button(with Box)-Blank)')
                        deltaObject.changeStatus(EButtonStatus.blank)
                        self.currentStage[doubleDeltaObject.y][doubleDeltaObject.x] = Box(doubleDeltaObject.x,
                                                                                          doubleDeltaObject.y,
                                                                                          self.boxPixmap)
                        self.goal += 1
                        self.gamePlayerMove(deltaX, deltaY)
                    elif doubleDeltaClassName == 'Button':
                        if doubleDeltaObject.status == EButtonStatus.blank:
                            doubleDeltaObject.changeStatus(EButtonStatus.withBox)
                            deltaObject.changeStatus(EButtonStatus.blank)
                            print('You can go (Button(withBox) - Button(Blank))')
                            self.gamePlayerMove(deltaX, deltaY)
                        elif doubleDeltaObject.status == EButtonStatus.withBox:
                            print('You can\'t go (Button(with Box)-(Button(with Box))')
                    elif doubleDeltaClassName == 'Box':
                        print('You can\'t go (Button(with Box)-Box)')
                    elif doubleDeltaClassName == 'Wall':
                        print('You can\'t go (Button(With Box) - Wall)')
            elif deltaClassName == 'Wall':
                print('You can\'t go (Wall)')
                pass
            elif deltaClassName == 'Box':
                doubleDeltaObject = self.currentStage[App.player.y + deltaY * 2][App.player.x + deltaX * 2]
                doubleDeltaClassName = type(doubleDeltaObject).__name__

                if doubleDeltaClassName == 'Box':
                    print('You can\'t go (Box - Box)')
                    pass
                elif doubleDeltaClassName == 'Wall':
                    print('You can\'t go (Box - Wall)')
                    pass
                elif doubleDeltaClassName == 'Blank':
                    print('You can go (Box - Blank)')
                    self.swapInCurrentStage(doubleDeltaObject, deltaObject)
                    self.gamePlayerMove(deltaX, deltaY)
                elif doubleDeltaClassName == 'Button':
                    if doubleDeltaObject.status == EButtonStatus.blank:
                        deltaObject.erase()
                        print('You can go (Box - Button(Blank))')
                        blank = Blank(deltaObject.x, deltaObject.y, self.blankPixmap0)
                        self.currentStage[App.player.y + deltaY][App.player.x + deltaX] = blank
                        blank.erase()
                        del deltaObject
                        self.goal -= 1
                        self.gamePlayerMove(deltaX, deltaY)
                        doubleDeltaObject.changeStatus(EButtonStatus.withBox)
                    elif doubleDeltaObject.status == EButtonStatus.withBox:
                        print('You can\'t go (Box - Button(With Box))')

        if self.goal == 0:
            print('Clear!')
            self.nextButton.setEnabled(True)

    def swapInCurrentStage(self, object1, object2):
        self.currentStage[object1.y][object1.x], self.currentStage[object2.y][object2.x] = self.currentStage[object2.y][
                                                                                               object2.x], \
                                                                                           self.currentStage[object1.y][
                                                                                               object1.x]
        x, y = object2.x, object2.y
        object2.jump(object1.x, object1.y)
        object1.jump(x, y)

    def printCurrentStage(self):
        print('print')
        for y in range(0, len(self.currentStage)):
            for x in range(0, len(self.currentStage[y])):
                print(type(self.currentStage[y][x]).__name__, ' ', end='')
            print()

    def gamePlayerMove(self, x, y):
        self.step += 1
        self.stepText.setText('Step: ' + str(self.step))
        self.goalText.setText('Goal: ' + str(self.goal))
        self.player.move(x, y)

    def eraseStage(self):
        for object in self.blankList:
            object.erase()
        for y in range(0, len(self.currentStage)):
            for x in range(0, len(self.currentStage[y])):
                self.currentStage[y][x].erase()
        if App.player is not None:
            App.player.erase()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())

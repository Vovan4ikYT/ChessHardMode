import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QCheckBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect
from game import ChessHardGame
from pygame import mixer

mixer.init()


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(700, 700)
        self.setWindowTitle('Главное меню')
        mixer.music.load('main_menu_theme.mp3')
        mixer.music.play()

        self.taunt = QLabel('Слабак! Таких шахматистов у нас не жалуют!', self)
        self.taunt.resize(500, 30)
        self.taunt.move(225, 550)
        self.taunt.hide()

        self.black, self.lava, self.anger = False, False, False
        self.count1, self.count2, self.count3 = 0, 0, 0

        self.main_label = QLabel(self)
        self.main_label.resize(300, 200)
        self.main_label.move(200, 20)
        self.hard_mode = QMovie('menu_gif.gif')
        self.main_label.setMovie(self.hard_mode)
        self.hard_mode.frameChanged.connect(self.stop_gif)
        self.hard_mode.start()

        self.label = QLabel('ШАХМАТЫ', self)
        self.label.setFont(QFont('RUSBoycott', 17))
        self.label.setStyleSheet('color: red')
        self.label.move(300, 0)

        self.challenge_label = QLabel(self)
        self.challenge_label.resize(70, 60)
        self.challenge_label.setPixmap(QPixmap('challenge_label.png'))
        self.challenge_label.move(20, 335)

        self.blackout = QCheckBox('Blackout', self)
        self.blackout.move(20, 330)
        self.blackout.stateChanged.connect(self.set_challenge)
        self.lava_floor = QCheckBox('Lava Floor', self)
        self.lava_floor.move(20, 350)
        self.lava_floor.stateChanged.connect(self.set_challenge)
        self.rage = QCheckBox('Rage', self)
        self.rage.move(20, 370)
        self.rage.stateChanged.connect(self.set_challenge)

        self.challenges = [self.blackout, self.lava_floor, self.rage]

        self.blackout_label = QLabel('Blackout (И погаснет свет навсегда) - \nмир вокруг тебя погружается во тьму!\n'
                                     'Теперь, кроме вражеского короля \nда твоих фигур, больше не видно \nНИЧЕГО!!!',
                                     self)
        self.blackout_label.resize(200, 200)
        self.blackout_label.move(350, 100)
        self.blackout_label.hide()

        self.lava_label = QLabel('Lava Floor (Пол - это лава) - \nслучайные клетки\nблокируются лавой!\n'
                                     'Ставить фигуры на них - \nБЕСЧЕСТЬЕ И ГРЕХ!!!',
                                     self)
        self.lava_label.resize(200, 200)
        self.lava_label.move(350, 200)
        self.lava_label.hide()

        self.rage_label = QLabel('Rage (Ярость) - \nкогда враг ест твою фигуру, \n'
                                     'он ходит ещё раз! \nКровавая ночь \nНАЧАЛАСЬ!!!',
                                     self)
        self.rage_label.resize(200, 200)
        self.rage_label.move(350, 300)
        self.rage_label.hide()

        self.start_button = QPushButton('Щёлкните, чтобы СТРАДАТЬ!!!', self)
        self.start_button.setFont(QFont('RUSBoycott', 15))
        self.start_button.setGeometry(QRect(300, 50, 300, 50))
        self.start_button.move(200, 600)
        self.start_button.clicked.connect(self.start_game)

    def stop_gif(self, frame):
        if self.hard_mode.frameCount() == frame + 1:
            self.hard_mode.stop()

    def start_game(self):
        with open('game_info.txt', 'w+') as f:
            if any([self.black, self.lava, self.anger]) is False:
                self.taunt.show()
            else:
                if self.black is True:
                    f.write('BLACKOUT\n')
                if self.lava is True:
                    f.write('LAVA FLOOR\n')
                if self.anger is True:
                    f.write('RAGE\n')
                mixer.music.stop()
                ex.hide()
                ex1.show()


    def set_challenge(self):
        global count1, count2, count3
        if self.challenges.index(self.sender()) == 0:
            if self.count1 == 0:
                self.count1 += 1
                self.black = True
                self.blackout_label.show()
            else:
                self.count1 = 0
                self.black = False
                self.blackout_label.hide()
        elif self.challenges.index(self.sender()) == 1:
            if self.count2 == 0:
                self.count2 += 1
                self.lava = True
                self.lava_label.show()
            else:
                self.count2 = 0
                self.lava = False
                self.lava_label.hide()
        elif self.challenges.index(self.sender()) == 2:
            if self.count3 == 0:
                self.count3 += 1
                self.anger = True
                self.rage_label.show()
            else:
                self.count3 = 0
                self.anger = False
                self.rage_label.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MainMenu()
    ex1 = ChessHardGame()
    ex.show()
    sys.exit(app.exec_())
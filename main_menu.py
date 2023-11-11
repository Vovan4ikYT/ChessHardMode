import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QCheckBox, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect, Qt
from game import ChessHardGame
from skinsshow import SkinsShow
from pygame import mixer

mixer.init(channels=2)

with open('game_info.txt', 'w') as f:
    f.write('')  # перезапись файла с данными игры для новой игры


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(700, 700)
        self.setWindowTitle('Главное меню')
        main_menu = mixer.Sound('sounds/main_menu_theme.mp3')
        mixer.Channel(0).set_volume(0.1)
        mixer.Channel(0).play(main_menu, loops=-1)

        self.taunt = QLabel('Перед боем шахматист должен выбрать скин. \n'
                            'Стиль - это тоже важно, ведь если \n'
                            'шахматист придёт на бой голым, \n'
                            'он и сам опростоволосится, и врага насмешит.', self)   # и не говорите мне,
        # что я не предупреждал
        self.taunt.resize(500, 70)
        self.taunt.move(225, 525)
        self.secret = ''   # ???

        self.count1, self.count2 = 0, 0   # счётчики испытаний
        self.skin_count = 0   # открытие меню со скинами
        self.black, self.lava = False, False   # условия испытаний

        self.main_label = QLabel(self)
        self.main_label.resize(300, 200)
        self.main_label.move(200, 20)
        self.hard_mode = QMovie('menu_gif.gif')   # гифка
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
        self.lava_floor.move(20, 370)
        self.lava_floor.stateChanged.connect(self.set_challenge)
        # установка испытаний

        self.challenges = [self.blackout, self.lava_floor]

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
        self.lava_label.move(350, 350)
        self.lava_label.hide()

        self.start_button = QPushButton('Щёлкните, чтобы СТРАДАТЬ!!!', self)
        self.start_button.setFont(QFont('RUSBoycott', 15))
        self.start_button.setGeometry(QRect(300, 50, 300, 50))
        self.start_button.move(200, 600)
        self.start_button.clicked.connect(self.start_game)

        self.skins_button = QPushButton('Скин-паки', self)
        self.skins_button.move(50, 600)
        self.skins_button.clicked.connect(self.skins_show)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_J or event.key() == Qt.Key_O or event.key() == Qt.Key_Y:
            self.secret += str(event.key())
        if self.secret == '747989':
            secret = mixer.Sound('sounds/secret.mp3')
            mixer.Channel(1).play(secret, loops=0)

            que = sqlite3.connect('skins')
            cur = que.cursor()
            cur.execute('''UPDATE info SET unlockation = 'unlocked' WHERE names = 'smeshariki' ''')
            que.commit()
            que.close()
            # запись Смешариков в БД

    def stop_gif(self, frame):
        if self.hard_mode.frameCount() == frame + 1:
            self.hard_mode.stop()   # остановка воспроизведения

    def skins_show(self):
        global ex2
        with open('game_info.txt', 'r') as f:
            lines = f.read()
            if 'BLACKOUT\n' not in lines and 'LAVA_FLOOR\n' not in lines:
                self.taunt.setText('Сначала выбери испытания.')   # просьба выбрать испытания
                self.taunt.show()
            else:
                ex2 = SkinsShow()   # открытие меню со скинами
                ex2.show()

                skins = mixer.Sound('sounds/skins.mp3')
                mixer.music.set_volume(0.5)
                mixer.Channel(0).play(skins, loops=-1)

    def start_game(self):
        global ex1
        with open('game_info.txt', 'r') as f:
            lines = f.read()
            if 'BLACKOUT\n' not in lines and 'LAVA_FLOOR\n' not in lines:
                self.taunt.setText('Слабак! Таких шахматистов у нас не жалуют!')   # да-да, не жалуют!
                self.taunt.show()
            else:
                mixer.Channel(0).stop()
                ex.hide()
                ex1 = ChessHardGame()   # игра
                ex1.show()

    def closeEvent(self, event):
        check = QMessageBox.question(self, 'Уже уходишь?', 'Ну и ладно! Давай, топай спасать свою никчёмную жизнь! '
                                                           'Но этим ты лишь докажешь, что в шахматисты ты '
                                                           'НЕ ГОДЕН!!!', QMessageBox.Yes, QMessageBox.No)
        # когда мы показали ему, кто тут босс доски, он делает выбор
        if check == QMessageBox.Yes:
            event.accept()   # закрытие
        else:
            event.ignore()   # игнорирование

    def set_challenge(self):
        global count1, count2, count3
        if self.challenges.index(self.sender()) == 0:   # проверка испытания
            if self.count1 == 0:   # проверка индекса
                self.count1 += 1
                with open('game_info.txt', 'a') as f:
                    f.write('BLACKOUT\n')   # запись в файл
                self.blackout_label.show()
                self.black = True
            else:
                self.count1 = 0
                with open('game_info.txt', 'r') as f:
                    data = f.read()
                    new_data = data.replace('BLACKOUT\n', '')
                with open('game_info.txt', 'w') as f:
                    f.write(new_data)
                self.blackout_label.hide()
                self.black = False
        elif self.challenges.index(self.sender()) == 1:
            if self.count2 == 0:
                self.count2 += 1
                with open('game_info.txt', 'a') as f:
                    f.write('LAVA_FLOOR\n')
                self.lava_label.show()
                self.lava = True
            else:
                self.count2 = 0
                with open('game_info.txt', 'r') as f:
                    data = f.read()
                    new_data = data.replace('LAVA_FLOOR\n', '')
                with open('game_info.txt', 'w') as f:
                    f.write(new_data)
                self.lava_label.hide()
                self.lava = False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MainMenu()
    ex1 = None   # изначально None, чтобы он не генерировался сразу
    ex2 = None
    ex.show()
    sys.exit(app.exec_())

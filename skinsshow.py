import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QRect
from pygame import mixer

con = sqlite3.connect('skins')
cur = con.cursor()   # работа с базой данной

mixer.init(channels=2)


class SkinsShow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(700, 700)
        self.setWindowTitle('Скин-паки')

        result = cur.execute('''SELECT names from info WHERE unlockation = 'unlocked' ''').fetchall()
        # проверка наличия скинов

        for b in range(len(result)):
            result[b] = str(result[b])[2:-3]   # подгонка названий скинов

        self.images = {}   # изображения
        self.names = []   # имена изображений
        for k in result:   # установка изображений в зависимости от БД
            if 'default' in k:
                self.images[k] = 'skin_images/default.png'
            elif 'blue_sky' in k:
                self.images[k] = 'skin_images/blue_sky.png'
            elif 'mk1' in k:
                self.images[k] = 'skin_images/mk1.png'
            elif 'fnaf' in k:
                self.images[k] = 'skin_images/fnaf.png'
            elif 'smeshariki' in k:
                self.images[k] = 'skin_images/smeshariki.png'
            self.names.append(k)

        self.skins_buttons = []
        for i in range(5):   # кнопки
            button = QPushButton(self)
            button.setGeometry(QRect(140, 140, 140, 140))
            button.move(140 * i, 280)
            button.clicked.connect(self.set_skin)
            self.skins_buttons.append(button)

        for j in range(len(result)):   # изображения
            self.skins_buttons[j].setStyleSheet(f'background-image: url({self.images[self.names[j]]});')

    def closeEvent(self, event):   # замена музыки на музыку из главного меню
        main_menu = mixer.Sound('sounds/main_menu_theme.mp3')
        mixer.Channel(0).set_volume(0.1)
        mixer.Channel(0).play(main_menu, loops=-1)

    def set_skin(self):   # запись скина в файл
        with open('game_info.txt', 'r') as f:
            data = f.readlines()
            with (open('game_info.txt', 'w') as f):
                for i in data:
                    if i != 'default' and i != 'blue_sky' and i != 'mk1' and i != 'fnaf' and i != 'smeshariki':
                        f.write(i)
            with open('game_info.txt', 'a') as f:
                f.write(self.names[self.skins_buttons.index(self.sender())] + '\n')
                # +'\n' чтобы потом открывался конец


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = SkinsShow()
    ex.show()
    sys.exit(app.exec_())

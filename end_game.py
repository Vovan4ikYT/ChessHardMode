import sys
import sqlite3
from random import choice

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFont
from pygame import mixer

mixer.init()

que = sqlite3.connect('skins')
cur = que.cursor()   # БД


class End(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setFixedSize(1000, 1000)
        self.setWindowTitle('КОНЕЦ')
        self.label = QLabel(self)
        self.text = QLabel(choice(['Король умер. \nДа здравствует король.',
                                   'Покойся с миром... \nили нет.',
                                   'Нет покоя голове в венце.',
                                   'Есть участи похуже смерти.']), self.label)
        # рандомный выбор фразы
        self.label.resize(1000, 1000)
        self.text.resize(300, 50)
        self.text.setFont(QFont('RUSBoycott', 15))
        self.text.setStyleSheet('color: white')
        self.text.move(350, 400)
        with open('game_info.txt', 'r') as f:
            lines = f.readlines()
            if 'white' in lines:
                self.pixmap = QPixmap('win.png')
                self.label.setPixmap(self.pixmap)
                self.text.hide()
                if 'BLACKOUT\n' in lines:
                    cur.execute('''UPDATE info SET unlockation = 'unlocked' WHERE names = 'mk1' ''')
                    que.commit()
                if 'LAVA FLOOR\n' in lines:
                    cur.execute('''UPDATE info SET unlockation = 'unlocked' WHERE names = 'fnaf' ''')
                    que.commit()
                # проверка на прохождение испытаний, если да то открываем скины
            elif 'black' in lines:
                self.pixmap = QPixmap('lose.png')
                self.label.setPixmap(self.pixmap)
                self.text.show()

        que.close()   # закрытие БД
        mixer.music.load('sounds/end.mp3')
        mixer.music.play(loops=-1)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = End()
    ex.show()
    sys.exit(app.exec_())

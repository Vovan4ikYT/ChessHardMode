import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QIcon


class ChessHardGame(QMainWindow):
    def __init__(self):
        super().__init__()
        board_label = QLabel(self)
        board_label.resize(800, 800)
        board = QPixmap('board.png')
        board_label.setPixmap(board)
        self.resize(board.width(), board.height())

        self.figures = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        bpawn_count = 0
        for i in range(8):
            bpawn_label = QLabel(self)
            bpawn_label.resize(100, 100)
            bpawn_label.move(bpawn_count, 100)
            bpawn = QPixmap('fighters/black/bpawn.png')
            bpawn_label.setPixmap(bpawn)
            bpawn_count += 100
            self.figures[1][bpawn_count // 100 - 1] = bpawn_label

        bknight_count = 100
        for i in range(2):
            bknight_label = QLabel(self)
            bknight_label.resize(100, 100)
            bknight_label.move(bknight_count, 0)
            bknight = QPixmap('fighters/black/bknight.png')
            bknight_label.setPixmap(bknight)
            bknight_count += 500

        bbishop_count = 200
        for i in range(2):
            bbishop_label = QLabel(self)
            bbishop_label.resize(100, 100)
            bbishop_label.move(bbishop_count, 0)
            bbishop = QPixmap('fighters/black/bbishop.png')
            bbishop_label.setPixmap(bbishop)
            bbishop_count += 300

        brook_count = 0
        for i in range(2):
            brook_label = QLabel(self)
            brook_label.resize(100, 100)
            brook_label.move(brook_count, 0)
            brook = QPixmap('fighters/black/brook.png')
            brook_label.setPixmap(brook)
            brook_count += 700

        bqueen_label = QLabel(self)
        bqueen_label.resize(100, 100)
        bqueen_label.move(400, 0)
        bqueen = QPixmap('fighters/black/bqueen.png')
        bqueen_label.setPixmap(bqueen)

        bking_label = QLabel(self)
        bking_label.resize(100, 100)
        bking_label.move(300, 0)
        bking = QPixmap('fighters/black/bking.png')
        bking_label.setPixmap(bking)

        wpawn_count = 0
        for i in range(8):
            wpawn_label = QLabel(self)
            wpawn_label.resize(100, 100)
            wpawn_label.move(wpawn_count, 600)
            wpawn = QPixmap('fighters/white/default/wpawn.png')
            wpawn_label.setPixmap(wpawn)
            wpawn_count += 100

        wknight_count = 100
        for i in range(2):
            wknight_label = QLabel(self)
            wknight_label.resize(100, 100)
            wknight_label.move(wknight_count, 700)
            wknight = QPixmap('fighters/white/default/wknight.png')
            wknight_label.setPixmap(wknight)
            wknight_count += 500

        wbishop_count = 200
        for i in range(2):
            wbishop_label = QLabel(self)
            wbishop_label.resize(100, 100)
            wbishop_label.move(wbishop_count, 700)
            wbishop = QPixmap('fighters/white/default/wbishop.png')
            wbishop_label.setPixmap(wbishop)
            wbishop_count += 300

        wrook_count = 0
        for i in range(2):
            wrook_label = QLabel(self)
            wrook_label.resize(100, 100)
            wrook_label.move(wrook_count, 700)
            wrook = QPixmap('fighters/white/default/wrook.png')
            wrook_label.setPixmap(wrook)
            wrook_count += 700

        wqueen_label = QLabel(self)
        wqueen_label.resize(100, 100)
        wqueen_label.move(300, 700)
        wqueen = QPixmap('fighters/white/default/wqueen.png')
        wqueen_label.setPixmap(wqueen)

        wking_label = QLabel(self)
        wking_label.resize(100, 100)
        wking_label.move(400, 700)
        wking = QPixmap('fighters/white/default/wking.png')
        wking_label.setPixmap(wking)

        self.setWindowTitle('Это твои последние шахматы...')
        self.setWindowIcon(QIcon('game_icon.ico'))
        for i in self.figures:
            print(i)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pole = QApplication(sys.argv)
    sys.excepthook = except_hook
    board_of_death = ChessHardGame()
    board_of_death.show()
    sys.exit(pole.exec_())
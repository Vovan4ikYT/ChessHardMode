import sys
from pygame import mixer
from random import choice

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QIcon

mixer.init()


class ChessHardGame(QMainWindow):
    def __init__(self):
        super().__init__()
        board_label = QLabel(self)
        board_label.resize(800, 800)
        board = QPixmap('board.png')
        board_label.setPixmap(board)
        gui_label = QLabel(self)
        gui_label.resize(800, 300)
        gui_label.move(0, 800)
        gui = QPixmap('button_gui.png')
        gui_label.setPixmap(gui)
        self.setFixedSize(800, 1100)

        self.first_position_label = QLabel(board_label)
        self.first_position_label.resize(100, 100)
        self.first_position = QPixmap('selected.png')

        self.second_position_label = QLabel(board_label)
        self.second_position_label.resize(100, 100)
        self.second_position = QPixmap('selected.png')

        self.first_coordinates = (0, 0)
        self.second_coordinates = (0, 0)

        self.count = 0

        self.figures, self.chars = ([[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']],

                                    [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

        self.cells = {'a8': (0, 0), 'b8': (100, 0), 'c8': (200, 0), 'd8': (300, 0),
                      'e8': (400, 0), 'f8': (500, 0), 'g8': (600, 0), 'h8': (700, 0),
                      'a7': (0, 100), 'b7': (100, 100), 'c7': (200, 100), 'd7': (300, 100),
                      'e7': (400, 100), 'f7': (500, 100), 'g7': (600, 100), 'h7': (700, 100),
                      'a6': (0, 200), 'b6': (100, 200), 'c6': (200, 200), 'd6': (300, 200),
                      'e6': (400, 200), 'f6': (500, 200), 'g6': (600, 200), 'h6': (700, 200),
                      'a5': (0, 300), 'b5': (100, 300), 'c5': (200, 300), 'd5': (300, 300),
                      'e5': (400, 300), 'f5': (500, 300), 'g5': (600, 300), 'h5': (700, 300),
                      'a4': (0, 400), 'b4': (100, 400), 'c4': (200, 400), 'd4': (300, 400),
                      'e4': (400, 400), 'f4': (500, 400), 'g4': (600, 400), 'h4': (700, 400),
                      'a3': (0, 500), 'b3': (100, 500), 'c3': (200, 500), 'd3': (300, 500),
                      'e3': (400, 500), 'f3': (500, 500), 'g3': (600, 500), 'h3': (700, 500),
                      'a2': (0, 600), 'b2': (100, 600), 'c2': (200, 600), 'd2': (300, 600),
                      'e2': (400, 600), 'f2': (500, 600), 'g2': (600, 600), 'h2': (700, 600),
                      'a1': (0, 700), 'b1': (100, 700), 'c1': (200, 700), 'd1': (300, 700),
                      'e1': (400, 700), 'f1': (500, 700), 'g1': (600, 700), 'h1': (700, 700)}

        bpawn_count = 0
        self.bpawn = QPixmap('fighters/black/bpawn.png')
        for i in range(8):
            bpawn_label = QLabel(board_label)
            bpawn_label.resize(100, 100)
            bpawn_label.move(bpawn_count, 100)
            bpawn_label.setPixmap(self.bpawn)
            bpawn_count += 100
            self.figures[1][bpawn_count // 100 - 1] = bpawn_label
            self.chars[1][bpawn_count // 100 - 1] = 'BP'

        bknight_count = 100
        self.bknight = QPixmap('fighters/black/bknight.png')
        for i in range(2):
            bknight_label = QLabel(board_label)
            bknight_label.resize(100, 100)
            bknight_label.move(bknight_count, 0)
            bknight_label.setPixmap(self.bknight)
            self.figures[0][bknight_count // 100] = bknight_label
            self.chars[0][bknight_count // 100] = 'BKn'
            bknight_count += 500

        bbishop_count = 200
        self.bbishop = QPixmap('fighters/black/bbishop.png')
        for i in range(2):
            bbishop_label = QLabel(board_label)
            bbishop_label.resize(100, 100)
            bbishop_label.move(bbishop_count, 0)
            bbishop_label.setPixmap(self.bbishop)
            self.figures[0][bbishop_count // 100] = bbishop_label
            self.chars[0][bbishop_count // 100] = 'BB'
            bbishop_count += 300

        brook_count = 0
        self.brook = QPixmap('fighters/black/brook.png')
        for i in range(2):
            brook_label = QLabel(board_label)
            brook_label.resize(100, 100)
            brook_label.move(brook_count, 0)
            brook_label.setPixmap(self.brook)
            self.figures[0][brook_count // 100] = brook_label
            self.chars[0][brook_count // 100] = 'BR'
            brook_count += 700

        bqueen_label = QLabel(board_label)
        self.bqueen = QPixmap('fighters/black/bqueen.png')
        bqueen_label.resize(100, 100)
        bqueen_label.move(400, 0)
        bqueen_label.setPixmap(self.bqueen)
        self.figures[0][400 // 100] = bqueen_label
        self.chars[0][400 // 100] = 'BQ'

        bking_label = QLabel(board_label)
        self.bking = QPixmap('fighters/black/bking.png')
        bking_label.resize(100, 100)
        bking_label.move(300, 0)
        bking_label.setPixmap(self.bking)
        self.figures[0][300 // 100] = bking_label
        self.chars[0][300 // 100] = 'BK'

        wpawn_count = 0
        self.wpawn = QPixmap('fighters/white/default/wpawn.png')
        for i in range(8):
            wpawn_label = QLabel(board_label)
            wpawn_label.resize(100, 100)
            wpawn_label.move(wpawn_count, 600)
            wpawn_label.setPixmap(self.wpawn)
            wpawn_count += 100
            self.figures[6][wpawn_count // 100 - 1] = wpawn_label
            self.chars[6][wpawn_count // 100 - 1] = 'WP'

        wknight_count = 100
        self.wknight = QPixmap('fighters/white/default/wknight.png')
        for i in range(2):
            wknight_label = QLabel(board_label)
            wknight_label.resize(100, 100)
            wknight_label.move(wknight_count, 700)
            wknight_label.setPixmap(self.wknight)
            self.figures[7][wknight_count // 100] = wknight_label
            self.chars[7][wknight_count // 100] = 'WKn'
            wknight_count += 500

        wbishop_count = 200
        self.wbishop = QPixmap('fighters/white/default/wbishop.png')
        for i in range(2):
            wbishop_label = QLabel(board_label)
            wbishop_label.resize(100, 100)
            wbishop_label.move(wbishop_count, 700)
            wbishop_label.setPixmap(self.wbishop)
            self.figures[7][wbishop_count // 100] = wbishop_label
            self.chars[7][wbishop_count // 100] = 'WB'
            wbishop_count += 300

        wrook_count = 0
        self.wrook = QPixmap('fighters/white/default/wrook.png')
        for i in range(2):
            wrook_label = QLabel(board_label)
            wrook_label.resize(100, 100)
            wrook_label.move(wrook_count, 700)
            wrook_label.setPixmap(self.wrook)
            self.figures[7][wrook_count // 100] = wrook_label
            self.chars[7][wrook_count // 100] = 'WR'
            wrook_count += 700

        wqueen_label = QLabel(board_label)
        self.wqueen = QPixmap('fighters/white/default/wqueen.png')
        wqueen_label.resize(100, 100)
        wqueen_label.move(300, 700)
        wqueen_label.setPixmap(self.wqueen)
        self.figures[7][300 // 100] = wqueen_label
        self.chars[7][300 // 100] = 'WQ'

        wking_label = QLabel(board_label)
        self.wking = QPixmap('fighters/white/default/wking.png')
        wking_label.resize(100, 100)
        wking_label.move(400, 700)
        wking_label.setPixmap(self.wking)
        self.figures[7][400 // 100] = wking_label
        self.chars[7][400 // 100] = 'WK'

        button_x, button_y, button_count = 0, 0, 0
        for i in self.cells:
            button = QPushButton(i, gui_label)
            button.setStyleSheet('QPushButton {color: red; background-image: url(button_background.jpg)}')
            button.setGeometry(QRect(100, 25, 100, 25))
            button.clicked.connect(self.choose)
            button.move(button_x, button_y)
            button_x += 100
            button_count += 1
            if button_count == 8:
                button_count = 0
                button_x = 0
                button_y += 25

        self.move_button = QPushButton('Ход', self)
        self.move_button.setGeometry(QRect(200, 100, 200, 100))
        self.move_button.move(300, 1000)
        self.move_button.clicked.connect(self.move_figure)

        self.setWindowTitle('Это твои последние шахматы...')
        self.setWindowIcon(QIcon('game_icon.ico'))
        for i in self.figures:
            print(i)
        print()
        for j in self.chars:
            print(j)

    def set_first_position(self):
        self.count += 1
        self.first_position_label.setPixmap(self.first_position)
        self.first_position_label.move(*self.cells[self.sender().text()])
        self.first_coordinates = (self.first_position_label.x(), self.first_position_label.y())
        print(self.first_coordinates)
        print(self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100])

    def set_second_position(self):
        self.count = 0
        self.second_position_label.setPixmap(self.second_position)
        self.second_position_label.move(*self.cells[self.sender().text()])
        self.second_coordinates = (self.second_position_label.x(), self.second_position_label.y())
        print(self.second_coordinates)

    def choose(self):
        if self.count == 0:
            self.set_first_position()
        else:
            self.set_second_position()

    def pawn_move(self, color):
        if color == 'white':
            current = self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
            if self.figures[self.first_coordinates[1] // 100 - 1][self.first_coordinates[0] // 100] == ' ':
                if self.first_coordinates[1] - self.second_coordinates[1] == 100:
                    current.move(self.second_coordinates[0], self.second_coordinates[1])
                    self.chars[self.first_coordinates[1] // 100 - 1][self.first_coordinates[0] // 100] = 'WP'
                    self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.figures[self.first_coordinates[1] // 100 - 1][self.first_coordinates[0] // 100] = current
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
            elif ((self.first_coordinates[1] - self.second_coordinates[1] == 100 and
                  self.first_coordinates[0] - self.second_coordinates[0] == 100) or
                  (self.second_coordinates[1] - self.first_coordinates[1] == 100 and
                  self.second_coordinates[0] - self.first_coordinates[0] == 100)):
                current.move(self.second_coordinates[0], self.second_coordinates[1])
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = current
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
        elif color == 'black':
            y = 400
            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]), self.second_coordinates[1] - y)
            current = self.figures[position[1] // 100][position[0] // 100]
            while True:
                    try:
                        while self.figures[position[1] // 100 + 1][position[0] // 100] != ' ':
                            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                        choice([0, 100, 200, 300, 400, 500, 600, 700]))
                            current = self.figures[position[1] // 100][position[0] // 100]
                        if (self.figures[position[1] // 100 + 1][position[0] // 100] == ' '
                                and self.chars[position[1] // 100][position[0] // 100] == 'BP'):
                            current.move(position[0], position[1] + 100)
                            self.chars[position[1] // 100 + 1][position[0] // 100] = 'BP'
                            self.chars[position[1] // 100][position[0] // 100] = ' '
                            self.figures[position[1] // 100 + 1][position[0] // 100] = current
                            self.figures[position[1] // 100][position[0] // 100] = ' '
                            break
                        else:
                            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                        choice([0, 100, 200, 300, 400, 500, 600, 700]))
                            current = self.figures[position[1] // 100][position[0] // 100]
                    except AttributeError:
                        position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700]))
                        while self.chars[position[1] // 100][position[0] // 100] != 'BP':
                            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                        choice([0, 100, 200, 300, 400, 500, 600, 700]))
                            if self.chars[position[1] // 100][position[0] // 100] == 'BP':
                                break
                        current = self.figures[position[1] // 100][position[0] // 100]
                    except IndexError:
                        position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700]))
                        current = self.figures[position[1] // 100][position[0] // 100]


    def move_figure(self):
        if self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WP':
            self.pawn_move('white')
            self.pawn_move('black')
            for i in self.figures:
                print(i)
            print()
            for j in self.chars:
                print(j)


mixer.music.load('london_bridge.mp3')
mixer.music.play()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pole = QApplication(sys.argv)
    sys.excepthook = except_hook
    board_of_death = ChessHardGame()
    board_of_death.show()
    sys.exit(pole.exec_())
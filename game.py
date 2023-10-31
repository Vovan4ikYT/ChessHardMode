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


        class Figure(QLabel):
            def __init__(self):
                super().__init__(board_label)
                self.resize(100, 100)


        self.figures, self.chars = ([[Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure()],
                                    [Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure()],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure()],
                                    [Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure(), Figure()]],

                                    [['BR', 'BKn', 'BB', 'BK', 'BQ', 'BB', 'BKn', 'BR'],
                                    ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                    ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
                                    ['WR', 'WKn', 'WB', 'WK', 'WQ', 'WB', 'WKn', 'WR']])

        for i in range(8):
            for j in range(8):
                if self.chars[i][j] == 'BP':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bpawn.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WP':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wpawn.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BR':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/brook.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WR':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wrook.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BKn':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bknight.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WKn':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wknight.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BB':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bbishop.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WB':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wbishop.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BK':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bking.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WK':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wking.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BQ':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bqueen.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WQ':
                    self.figures[i][j].setPixmap(QPixmap('fighters/white/default/wqueen.png'))
                    self.figures[i][j].move(j * 100, i * 100)

        self.move_button = QPushButton('Ход', self)
        self.move_button.setGeometry(QRect(200, 100, 200, 100))
        self.move_button.move(300, 900)
        self.move_button.clicked.connect(self.move_figure)

        self.setWindowTitle('Это твои последние шахматы...')
        self.setWindowIcon(QIcon('game_icon.ico'))
        for i in self.figures:
            print(i)
        print()
        for j in self.chars:
            print(j)

    def mousePressEvent(self, event):
        if self.count == 0:
            self.count += 1
            self.first_position_label.setPixmap(self.first_position)
            self.first_position_label.move(event.x() // 100 * 100, event.y() // 100 * 100)
            self.first_coordinates = event.x() // 100 * 100, event.y() // 100 * 100
            print(self.first_coordinates)
        else:
            self.count = 0
            self.second_position_label.setPixmap(self.second_position)
            self.second_position_label.move(event.x() // 100 * 100, event.y() // 100 * 100)
            self.second_coordinates = event.x() // 100 * 100, event.y() // 100 * 100
            print(self.second_coordinates)

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
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = current
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                current.move(self.second_coordinates[0], self.second_coordinates[1])
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

    def knight_move(self, color):
        if color == 'white':
            current = self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
            if (((self.first_coordinates[1] - self.second_coordinates[1] == 200 and
                    self.second_coordinates[0] - self.first_coordinates[0] == 100) or
                    (self.first_coordinates[1] - self.second_coordinates[1] == 200 and
                    self.first_coordinates[0] - self.second_coordinates[0] == 100)) or
                    (self.second_coordinates[1] - self.first_coordinates[1] == 200 and
                    self.second_coordinates[0] - self.first_coordinates[0] == 100) or
                    (self.second_coordinates[1] - self.first_coordinates[1] == 200 and
                    self.first_coordinates[0] - self.second_coordinates[0] == 100)):
                current.move(self.second_coordinates[0], self.second_coordinates[1])
                self.chars[self.first_coordinates[1] // 100 - 1][self.first_coordinates[0] // 100] = 'WKn'
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.figures[self.first_coordinates[1] // 100 - 1][self.first_coordinates[0] // 100] = current
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '

    def move_figure(self):
        if self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WP':
            self.pawn_move('white')
            self.pawn_move('black')
        elif self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WKn':
            self.knight_move('white')
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
import sys
from pygame import mixer
from random import choice

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QMovie

mixer.init()


class ChessHardGame(QMainWindow):
    def __init__(self):
        super().__init__()
        board_label = QLabel(self)
        board_label.resize(800, 800)
        with open('game_info.txt', 'r') as f:
            lines = f.readlines()
            if 'BLACKOUT\n' in lines:
                board = QPixmap('board_blackout.png')
                board_label.setPixmap(board)
            else:
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

        self.death_label = QLabel(self)
        self.death_label.resize(800, 800)

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
        self.move_button.move(100, 900)
        self.move_button.clicked.connect(self.move_figure)

        self.reset_button = QPushButton('Сброс позиции', self)
        self.reset_button.setGeometry(QRect(200, 100, 200, 100))
        self.reset_button.move(500, 900)
        self.reset_button.clicked.connect(self.reset_move)

        self.setWindowTitle('Это твои последние шахматы...')
        self.setWindowIcon(QIcon('game_icon.ico'))
        for i in self.figures:
            print(i)
        print()
        for j in self.chars:
            print(j)

    def die_already(self, death):
        self.death_label.setMovie(death)
        self.death_label.move(0, 0)
        death.start()
        self.death_label.show()
        timer = QTimer()
        timer.singleShot(1400, self.death_label.hide)

        mixer.music.load('death.mp3')
        mixer.music.play(loops=1)

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
            if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] == ' ' and
                    self.second_coordinates[1] - self.first_coordinates[1] == -100 and
                    abs(self.second_coordinates[0] - self.first_coordinates[0]) != 100):
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
            elif (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                  abs(self.second_coordinates[0] - self.first_coordinates[0]) == 100):
                      self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                      self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                          self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                      self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                          self.second_coordinates[0], self.second_coordinates[1])
                      self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                      self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                      self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
                      self.die_already(QMovie('deaths/pawn_death.gif'))
        elif color == 'black':
            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700]))
            while True:
                try:
                    if (self.chars[position[1] // 100 + 1][position[0] // 100] == ' ' and
                            self.chars[position[1] // 100][position[0] // 100] == 'BP' and
                            'W' not in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                        self.figures[position[1] // 100 + 1][position[0] // 100] = (
                            self.figures)[position[1] // 100][position[0] // 100]
                        self.figures[position[1] // 100][position[0] // 100].move(
                            position[0], position[1] + 100)
                        self.figures[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100 + 1][position[0] // 100] = 'BP'
                        break
                    elif (self.chars[position[1] // 100 + 1][position[0] // 100 - 1] != ' ' and
                          abs((position[0] // 100 - 1) - position[0] // 100) and
                          self.chars[position[1] // 100][position[0] // 100] == 'BP' and 'B' not in
                          self.chars[position[1] // 100 + 1][position[0] // 100 - 1]):
                        self.figures[position[1] // 100 + 1][position[0] // 100 - 1].hide()
                        self.figures[position[1] // 100 + 1][position[0] // 100 - 1] = (
                            self.figures)[position[1] // 100][position[0] // 100]
                        self.figures[position[1] // 100][position[0] // 100].move(
                            position[0] - 100, position[1] + 100)
                        self.figures[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100 + 1][position[0] // 100 - 1] = 'BP'
                        self.die_already(QMovie('deaths/pawn_death.gif'))
                        break
                    elif (self.chars[position[1] // 100 + 1][position[0] // 100 + 1] != ' ' and
                          abs((position[0] // 100 + 1) - position[0] // 100) and
                          self.chars[position[1] // 100][position[0] // 100] == 'BP' and 'B' not in
                          self.chars[position[1] // 100 + 1][position[0] // 100 + 1]):
                        self.figures[position[1] // 100 + 1][position[0] // 100 + 1].hide()
                        self.figures[position[1] // 100 + 1][position[0] // 100 + 1] = (
                            self.figures)[position[1] // 100][position[0] // 100]
                        self.figures[position[1] // 100][position[0] // 100].move(
                            position[0] + 100, position[1] + 100)
                        self.figures[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100][position[0] // 100] = ' '
                        self.chars[position[1] // 100 + 1][position[0] // 100 + 1] = 'BP'
                        self.die_already(QMovie('deaths/pawn_death.gif'))
                        break
                    else:
                        position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700]))
                except AttributeError:
                    position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700]))
                    while self.chars[position[1] // 100][position[0] // 100] != 'BP':
                        position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700]))
                        if self.chars[position[1] // 100][position[0] // 100] == 'BP':
                            break
                except IndexError:
                    position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700]))


    def knight_move(self, color):
        if color == 'white':
            if ((abs(self.second_coordinates[0] - self.first_coordinates[0]) == 100 and
                abs(self.second_coordinates[1] - self.first_coordinates[1]) == 200) or
                    (abs(self.second_coordinates[0] - self.first_coordinates[0]) == 200 and
                     abs(self.second_coordinates[1] - self.first_coordinates[1]) == 100)):
                if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                        'W' not in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                    self.die_already(QMovie('deaths/knight_death.gif'))
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WKn'
        elif color == 'black':
            position1, position2 = (
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])),
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])))
            while True:
                try:
                    if 'B' in self.chars[position2[1] // 100][position1[0] // 100]:
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        continue
                    else:
                        if ((((abs(position2[0] - position1[0]) == 100 and abs(position2[1] - position1[1]) == 200) or
                                (abs(position2[0] - position1[0]) == 200 and abs(position2[1] - position1[1]) == 100)))
                                and
                                (self.chars[position1[1] // 100][position1[0] // 100] == 'BKn') and ('B' not in
                                self.chars[position2[1] // 100][position1[0] // 100])):
                            if (self.chars[position2[1] // 100][position1[0] // 100] != ' ' and 'W' in
                                    self.chars[position2[1] // 100][position1[0] // 100]):
                                self.figures[position2[1] // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/knight_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BKn'
                            break
                        else:
                            position1, position2 = (
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                 choice([0, 100, 200, 300, 400, 500, 600, 700])),
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                 choice([0, 100, 200, 300, 400, 500, 600, 700])))
                except AttributeError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))
                    while self.chars[position1[1] // 100][position1[0] // 100] != 'BKn':
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        if self.chars[position1[1] // 100][position1[0] // 100] == 'BKn':
                            break
                except IndexError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))

    def bishop_move(self, color):
        if color == 'white':
            if (abs(self.second_coordinates[0] - self.first_coordinates[0]) != 0 and
                    abs(self.second_coordinates[1] - self.first_coordinates[1]) ==
                    abs(self.second_coordinates[0] - self.first_coordinates[0])):
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WB'

    def rook_move(self, color):
        if color == 'white':
            if (self.first_coordinates[0] == self.second_coordinates[0] or
                    self.first_coordinates[1] == self.second_coordinates[1]):
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WR'

    def queen_move(self, color):
        if color == 'white':
            if (self.first_coordinates[0] == self.second_coordinates[0] or
                    self.first_coordinates[1] == self.second_coordinates[1] or
                    (abs(self.second_coordinates[0] - self.first_coordinates[0]) != 0 and
                     abs(self.second_coordinates[1] - self.first_coordinates[1]) ==
                     abs(self.second_coordinates[0] - self.first_coordinates[0]))):
                if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                        'W' not in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                    self.die_already(QMovie('deaths/queen_death.gif'))
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WQ'
        elif color == 'black':
            position1, position2 = (
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])),
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])))
            while True:
                try:
                    if 'B' in self.chars[position2[1] // 100][position1[0] // 100]:
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        continue
                    else:
                        if (((abs(position2[0] - position1[0]) != 0 and
                                abs(position2[1] - position1[1]) ==
                                abs(position2[0] - position1[0])) or position1[0] == position2[0] or
                                position1[1] == position2[1]) and
                                self.chars[position1[1] // 100][position1[0] // 100] == 'BQ'):
                            if self.chars[position2[1] // 100][position1[0] // 100] != ' ':
                                self.figures[position2[1] // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/queen_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BQ'
                            break
                        else:
                            position1, position2 = (
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700])),
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700])))
                except AttributeError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))
                    while self.chars[position1[1] // 100][position1[0] // 100] != 'BQ':
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        if self.chars[position1[1] // 100][position1[0] // 100] == 'BQ':
                            break
                except IndexError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))
    def move_figure(self):
        if self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WP':
            self.pawn_move('white')
        elif self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WKn':
            self.knight_move('white')
        elif self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WB':
            self.bishop_move('white')
        elif self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WR':
            self.rook_move('white')
        elif self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] == 'WQ':
            self.queen_move('white')
        choice([self.pawn_move, self.knight_move, self.queen_move])('black')
        for i in self.figures:
            print(i)
        print()
        for j in self.chars:
            print(j)

    def reset_move(self):
        self.first_coordinates = (0, 0)
        self.second_coordinates = (0, 0)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pole = QApplication(sys.argv)
    sys.excepthook = except_hook
    board_of_death = ChessHardGame()
    board_of_death.show()
    sys.exit(pole.exec_())
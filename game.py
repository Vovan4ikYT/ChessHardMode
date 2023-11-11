import sys
from pygame import mixer
from random import choice

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from end_game import End

mixer.init(channels=3)

skin = None  # скин, который будет стоять, если не поставить изначально, будет невидимый. А я предупреждал про скины!


class ChessHardGame(QWidget):
    def __init__(self):
        super().__init__()
        board_label = QLabel(self)
        board_label.resize(800, 800)

        self.moved = False   # походили ли чёрные

        class Figure(QLabel):   # класс фигуры
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
        # две матрицы: с классами фигур и их обозначениями

        with open('game_info.txt', 'r') as f:
            lines = f.readlines()
            if 'BLACKOUT\n' in lines:
                board = QPixmap('board_blackout.png')
                board_label.setPixmap(board)
            else:
                board = QPixmap('board.png')
                board_label.setPixmap(board)   # постановка доски в зависимости от испытания
            if 'LAVA_FLOOR\n' in lines:
                for i in range(choice(range(3, 9))):
                    lava_label = QLabel(board_label)
                    lava_label.resize(100, 100)
                    if 'BLACKOUT\n' in lines:
                        lava = QPixmap('lava_blackout.png')
                        lava_label.setPixmap(lava)
                    else:
                        lava = QPixmap('lava.png')
                        lava_label.setPixmap(lava)
                    temp1, temp2 = [0, 100, 200, 300, 400, 500, 600, 700], [300, 400, 500]
                    coordinates = [choice(temp1), choice(temp2)]
                    lava_label.move(coordinates[0], coordinates[1])
                    self.chars[coordinates[1] // 100][coordinates[0] // 100] = 'LAVA'
                    self.figures[coordinates[1] // 100][coordinates[0] // 100] = 'LAVA'
                    temp1.remove(lava_label.x())
                    temp2.remove(lava_label.y())
                    # размещение лавы в зависимости от испытания
            if lines[-1] != 'BLACKOUT\n' and lines[-1] != 'LAVA FLOOR\n':
                skin = lines[-1].rstrip('\n')   # установка скина
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
        self.second_position = QPixmap('selected.png')   # выделение позиций хода

        self.first_coordinates = (0, 0)
        self.second_coordinates = (0, 0)   # координаты ходов белых

        self.count = 0

        self.death_label = QLabel(self)
        self.death_label.resize(800, 800)   # местозаниматель для смерти

        self.move_count = 0
        (self.black_pawn_count, self.black_rook_count, self.black_knight_count,
         self.black_bishop_count, self.black_queen_count) = 8, 2, 2, 2, 1
        (self.white_pawn_count, self.white_rook_count, self.white_knight_count,
         self.white_bishop_count, self.white_queen_count) = 8, 2, 2, 2, 1  # кол-во фигур,
        # нужно убить определённое количество за определённое время

        for i in range(8):
            for j in range(8):
                if self.chars[i][j] == 'BP':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bpawn.png'))  # установка картинок
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WP':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wpawn.png'))  # установка скина
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BR':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/brook.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WR':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wrook.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BKn':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bknight.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WKn':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wknight.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BB':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bbishop.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WB':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wbishop.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BK':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bking.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WK':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wking.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'BQ':
                    self.figures[i][j].setPixmap(QPixmap('fighters/black/bqueen.png'))
                    self.figures[i][j].move(j * 100, i * 100)
                elif self.chars[i][j] == 'WQ':
                    self.figures[i][j].setPixmap(QPixmap(f'fighters/white/{skin}/wqueen.png'))
                    self.figures[i][j].move(j * 100, i * 100)

        self.move_button = QPushButton('Ход', self)
        self.move_button.setGeometry(QRect(200, 100, 200, 100))
        self.move_button.move(100, 900)
        self.move_button.clicked.connect(self.move_figure)   # ход

        self.reset_button = QPushButton('Сброс позиции', self)
        self.reset_button.setGeometry(QRect(200, 100, 200, 100))
        self.reset_button.move(500, 900)
        self.reset_button.clicked.connect(self.reset_move)   # сброс позиции

        self.setWindowTitle('Это твои последние шахматы...')
        self.setWindowIcon(QIcon('game_icon.ico'))

    def die_already(self, death):
        self.death_label.setMovie(death)
        self.death_label.move(0, 0)
        death.start()
        self.death_label.show()
        timer = QTimer()
        timer.singleShot(1400, self.death_label.hide)

        death_sound = mixer.Sound('sounds/death.mp3')
        mixer.Channel(0).set_volume(0.2)
        mixer.Channel(0).play(death_sound)   # СМЕРТЬ

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
            print(self.second_coordinates)   # обработка координат

    def eat(self, color, char):
        if color == 'black':
            if 'P' in char:
                self.black_pawn_count -= 1   # уменьшение кол-ва фигур в зависимости от фигуры и цвета
            elif 'R' in char:
                self.black_rook_count -= 1
            elif 'Kn' in char:
                self.black_knight_count -= 1
            elif 'BB' in char:
                self.black_bishop_count -= 1
            elif 'Q' in char:
                self.black_queen_count -= 1
        elif color == 'white':
            if 'P' in char:
                self.white_pawn_count -= 1
            elif 'R' in char:
                self.white_rook_count -= 1
            elif 'Kn' in char:
                self.white_knight_count -= 1
            elif 'WB' in char:
                self.white_bishop_count -= 1
            elif 'Q' in char:
                self.white_queen_count -= 1

    def pawn_move(self, color):   # здесь и далее: как ходят фигуры
        if color == 'white':   # цвет
            if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] == ' ' and
                    self.second_coordinates[1] - self.first_coordinates[1] == -100 and
                    abs(self.second_coordinates[0] - self.first_coordinates[0]) != 100):   # проверка условия
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                    self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                    self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
                # перемещение фигуры
                self.moved = False
            elif (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                  abs(self.second_coordinates[0] - self.first_coordinates[0]) == 100 and 'B' in
                  self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] and
                  self.second_coordinates[1] - self.first_coordinates[1] == -100):
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                self.eat('black', self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100])
                # съедение фигуры
                self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                          self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                          self.second_coordinates[0], self.second_coordinates[1])
                self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WP'
                self.moved = False
                self.die_already(QMovie('deaths/pawn_death.gif'))   # СМЕРТЬ
        elif color == 'black':
            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700]))
            # рандомный выбор позиции
            while True:
                try:
                    if self.black_pawn_count == 0:   # если таких фигур больше нет
                        pass
                    else:
                        if ((self.chars[position[1] // 100 + 1][position[0] // 100] == ' ') and
                                self.chars[position[1] // 100][position[0] // 100] == 'BP'):   # проверка условия
                            self.figures[position[1] // 100 + 1][position[0] // 100] = (
                                self.figures)[position[1] // 100][position[0] // 100]
                            self.figures[position[1] // 100][position[0] // 100].move(
                                position[0], position[1] + 100)
                            self.figures[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100 + 1][position[0] // 100] = 'BP'
                            self.move_count += 1
                            self.moved = True
                            break   # ход
                        elif (abs((position[0] // 100 - 1) - position[0] // 100) and
                              self.chars[position[1] // 100][position[0] // 100] == 'BP' and 'W' in
                              self.chars[position[1] // 100 + 1][position[0] // 100 - 1]):
                            self.eat('white', self.chars[position[1] // 100 + 1][position[0] // 100 - 1])
                            # съедение
                            self.figures[position[1] // 100 + 1][position[0] // 100 - 1].hide()
                            self.figures[position[1] // 100 + 1][position[0] // 100 - 1] = (
                                self.figures)[position[1] // 100][position[0] // 100]
                            self.figures[position[1] // 100][position[0] // 100].move(
                                position[0] - 100, position[1] + 100)
                            self.figures[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100 + 1][position[0] // 100 - 1] = 'BP'
                            self.die_already(QMovie('deaths/pawn_death.gif'))
                            self.move_count += 1
                            self.moved = True
                            break
                        elif (abs((position[0] // 100 + 1) - position[0] // 100) and
                              self.chars[position[1] // 100][position[0] // 100] == 'BP' and 'W' in
                              self.chars[position[1] // 100 + 1][position[0] // 100 + 1]):
                            self.eat('white', self.chars[position[1] // 100 + 1][position[0] // 100 + 1])
                            self.figures[position[1] // 100 + 1][position[0] // 100 + 1].hide()
                            self.figures[position[1] // 100 + 1][position[0] // 100 + 1] = (
                                self.figures)[position[1] // 100][position[0] // 100]
                            self.figures[position[1] // 100][position[0] // 100].move(
                                position[0] + 100, position[1] + 100)
                            self.figures[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100][position[0] // 100] = ' '
                            self.chars[position[1] // 100 + 1][position[0] // 100 + 1] = 'BP'
                            self.die_already(QMovie('deaths/pawn_death.gif'))
                            self.move_count += 1
                            self.moved = True
                            break
                        else:
                            position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                        choice([0, 100, 200, 300, 400, 500, 600, 700]))
                            # выбор позиции по-новой
                except AttributeError:
                    position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700]))
                    while self.chars[position[1] // 100][position[0] // 100] != 'BP':
                        position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                    choice([0, 100, 200, 300, 400, 500, 600, 700]))
                        if self.chars[position[1] // 100][position[0] // 100] == 'BP':
                            break   # выбор позиции по-новой, пока не выбрана подходящая фигура
                except IndexError:
                    position = (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                choice([0, 100, 200, 300, 400, 500, 600, 700]))   # выбор позиции по-новой

    def knight_move(self, color):
        if color == 'white':
            if self.move_count < 8:
                pass
            else:
                if ((abs(self.second_coordinates[0] - self.first_coordinates[0]) == 100 and
                    abs(self.second_coordinates[1] - self.first_coordinates[1]) == 200) or
                        (abs(self.second_coordinates[0] - self.first_coordinates[0]) == 200 and
                         abs(self.second_coordinates[1] - self.first_coordinates[1]) == 100)):
                    if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                            'B' in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                        self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                        self.eat('black',
                                 self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100])
                        self.die_already(QMovie('deaths/knight_death.gif'))
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                        self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                        self.second_coordinates[0], self.second_coordinates[1])
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WKn'
                    self.moved = False
        elif color == 'black':
            position1, position2 = \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])), \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700]))
            while True:
                try:
                    if self.black_knight_count == 0:
                        pass
                    else:
                        if ((((abs(position2[0] - position1[0]) == 100 and abs(position2[1] - position1[1]) == 200) or
                                (abs(position2[0] - position1[0]) == 200 and abs(position2[1] - position1[1]) == 100)))
                                and
                                (self.chars[position1[1] // 100][position1[0] // 100] == 'BKn')):
                            if ('W' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'B' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'LAVA' in self.chars[position2[1] // 100][position2[0] // 100]):
                                if 'W' in self.chars[position2[1] // 100][position2[0] // 100]:
                                    self.eat('white', self.chars[position2[1] // 100][position2[0] // 100])
                                self.figures[position2[1] // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/knight_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BKn'
                            self.move_count += 1
                            self.moved = True
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
            if self.move_count < 8:
                pass
            else:
                if (abs(self.second_coordinates[0] - self.first_coordinates[0]) != 0 and
                        abs(self.second_coordinates[1] - self.first_coordinates[1]) ==
                        abs(self.second_coordinates[0] - self.first_coordinates[0])):
                    if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                            'B' in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                        self.eat('black',
                                 self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100])
                        self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                        self.die_already(QMovie('deaths/bishop_death.gif'))
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                        self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                        self.second_coordinates[0], self.second_coordinates[1])
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WB'
                    self.moved = False
        elif color == 'black':
            position1, position2 = \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])), \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700]))
            while True:
                try:
                    if self.black_bishop_count == 0:
                        pass
                    else:
                        if (abs(position2[0] - position1[0]) != 0 and
                                abs(position2[1] - position1[1]) ==
                                abs(position2[0] - position1[0])) and \
                                self.chars[position1[1] // 100][position1[0] // 100] == 'BB':
                            if ('W' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'B' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'LAVA' in self.chars[position2[1] // 100][position2[0] // 100]):
                                if 'W' in self.chars[position2[1] // 100][position2[0] // 100]:
                                    self.eat('white', self.chars[position2[1] // 100][position2[0] // 100])
                                self.figures[position2[1]
                                             // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/bishop_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BB'
                            self.move_count += 1
                            self.moved = True
                            break
                        else:
                            position1, position2 = \
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                 choice([0, 100, 200, 300, 400, 500, 600, 700])), \
                                (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                                 choice([0, 100, 200, 300, 400, 500, 600, 700]))
                except AttributeError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))
                    while self.chars[position1[1] // 100][position1[0] // 100] != 'BB':
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        if self.chars[position1[1] // 100][position1[0] // 100] == 'BB':
                            break
                except IndexError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))

    def rook_move(self, color):
        if color == 'white':
            if self.move_count < 8:
                pass
            else:
                if (self.first_coordinates[0] == self.second_coordinates[0] or
                        self.first_coordinates[1] == self.second_coordinates[1]):
                    if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                            'B' in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                        self.eat('black',
                                 self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100])
                        self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                        self.die_already(QMovie('deaths/rook_death.gif'))
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                        self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                        self.second_coordinates[0], self.second_coordinates[1])
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WR'
                    self.moved = False
        elif color == 'black':
            position1, position2 = \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])), \
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700]))
            while True:
                try:
                    if self.black_rook_count == 0:
                        pass
                    else:
                        if ((position2[0] == position1[0] or position2[1] == position1[1])
                                and self.chars[position1[1] // 100][position1[0] // 100] == 'BR'):
                            if ('W' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'B' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'LAVA' in self.chars[position2[1] // 100][position2[0] // 100]):
                                if 'W' in self.chars[position2[1] // 100][position2[0] // 100]:
                                    self.eat('white', self.chars[position2[1] // 100][position2[0] // 100])
                                self.figures[position2[1] // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/rook_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BR'
                            self.move_count += 1
                            self.moved = True
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
                    while self.chars[position1[1] // 100][position1[0] // 100] != 'BR':
                        position1, position2 = (
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])),
                            (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                             choice([0, 100, 200, 300, 400, 500, 600, 700])))
                        if self.chars[position1[1] // 100][position1[0] // 100] == 'BR':
                            break
                except IndexError:
                    position1, position2 = (
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])),
                        (choice([0, 100, 200, 300, 400, 500, 600, 700]),
                         choice([0, 100, 200, 300, 400, 500, 600, 700])))

    def queen_move(self, color):
        if color == 'white':
            if self.move_count < 8:
                pass
            else:
                if (self.first_coordinates[0] == self.second_coordinates[0] or
                        self.first_coordinates[1] == self.second_coordinates[1] or
                        (abs(self.second_coordinates[0] - self.first_coordinates[0]) != 0 and
                         abs(self.second_coordinates[1] - self.first_coordinates[1]) ==
                         abs(self.second_coordinates[0] - self.first_coordinates[0]))):
                    if (self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] != ' ' and
                            'B' in self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100]):
                        self.eat('black',
                                 self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100])
                        self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100].hide()
                        self.die_already(QMovie('deaths/queen_death.gif'))
                    self.figures[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = (
                        self.figures)[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100]
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100].move(
                        self.second_coordinates[0], self.second_coordinates[1])
                    self.figures[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.first_coordinates[1] // 100][self.first_coordinates[0] // 100] = ' '
                    self.chars[self.second_coordinates[1] // 100][self.second_coordinates[0] // 100] = 'WQ'
                    self.moved = False
        elif color == 'black':
            position1, position2 = (
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])),
                (choice([0, 100, 200, 300, 400, 500, 600, 700]), choice([0, 100, 200, 300, 400, 500, 600, 700])))
            while True:
                try:
                    if self.black_queen_count == 0:
                        pass
                    else:
                        if (((abs(position2[0] - position1[0]) != 0 and
                                abs(position2[1] - position1[1]) ==
                                abs(position2[0] - position1[0])) or position1[0] == position2[0] or
                                position1[1] == position2[1]) and
                                self.chars[position1[1] // 100][position1[0] // 100] == 'BQ'):
                            if ('W' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'B' in self.chars[position2[1] // 100][position2[0] // 100] or
                                    'LAVA' in self.chars[position2[1] // 100][position2[0] // 100]):
                                if 'W' in self.chars[position2[1] // 100][position2[0] // 100]:
                                    self.eat('white', self.chars[position2[1] // 100][position2[0] // 100])
                                self.figures[position2[1] // 100][position2[0] // 100].hide()
                                self.die_already(QMovie('deaths/queen_death.gif'))
                            self.figures[position2[1] // 100][position2[0] // 100] = (
                                self.figures)[position1[1] // 100][position1[0] // 100]
                            self.figures[position1[1] // 100][position1[0] // 100].move(
                                position2[0], position2[1])
                            self.figures[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position1[1] // 100][position1[0] // 100] = ' '
                            self.chars[position2[1] // 100][position2[0] // 100] = 'BQ'
                            self.move_count += 1
                            self.moved = True
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

    def final(self):
        global end_of_the_line   # виджет конца
        with (open('game_info.txt', 'a') as f):
            if (self.black_pawn_count != 3 and self.black_queen_count != 0 and self.black_knight_count != 0 and
                    self.black_bishop_count != 1):   # проверка условия
                f.write('black')   # запись в файл кто победил
            else:
                f.write('white')
        self.die_already(QMovie('deaths/king_death.gif'))
        end_of_the_line = End()   # виджет конца
        self.hide()
        end_of_the_line.show()

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
        # осуществление движения белых
        if self.move_count < 5:
            self.pawn_move('black')   # первые 5 ходов ходят только пешки
        elif self.move_count == 10:
            self.final()   # конец
        else:   # осуществление движения чёрных
            choice([self.pawn_move, self.knight_move, self.queen_move, self.bishop_move, self.rook_move])('black')
            while self.moved is False:
                choice([self.pawn_move, self.knight_move, self.queen_move, self.bishop_move, self.rook_move])('black')
                if self.moved is True:
                    break

    def reset_move(self):   # сброс позиции
        self.first_coordinates = (0, 0)
        self.second_coordinates = (0, 0)
        self.count = 0


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    pole = QApplication(sys.argv)
    sys.excepthook = except_hook
    board_of_death = ChessHardGame()
    board_of_death.show()
    end_of_the_line = None
    sys.exit(pole.exec_())

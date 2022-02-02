"""
Course: CSE 251
File: cse251.py
Author: Brother Comeau

Purpose: Common classes for the CSE 251 course
"""

import os
import sys
import time
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import turtle
import cv2

# ===============================================================================================
def print_dict(dict, title=''):
    """ Display a dictionary in a structured format """
    if title != '':
        print(f'Dictionary: {title}')
    print(json.dumps(dict, indent=3))


# ===============================================================================================
def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file: 
            data = json.load(json_file)
        return data
    else:
        return {}


# ===============================================================================================
class Log():
    """ Logger Class for CSE 251 """

    def __init__(self, filename_log='',
                 linefmt='',
                 show_levels=False,
                 show_terminal=False,
                 include_time=True):
        self._start_time = time.perf_counter()
        self._show_terminal = show_terminal

        if filename_log == '':
            d = datetime.now()
            localtime = d.strftime("%m%d-%H%M%S")
            filename_log = f'{localtime}.log'

        self._filename = filename_log

        if linefmt == '':
          linefmt = '%(message)s'

        if show_levels:
            linefmt = '%(levelname)s - ' + linefmt

        if include_time:
            date_format = '%H:%M:%S'
            linefmt = '%(asctime)s| ' + linefmt
        else:
            date_format = ''

        # Create and configure logger
        logging.basicConfig(filename=self._filename,
                            # format='%(asctime)s %(levelname)s %(message)s',
                            format=linefmt,
                            datefmt=date_format,
                            filemode='w')

        self.logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

        if show_terminal:
            formatter = logging.Formatter(linefmt, datefmt=date_format)
            terminal_handler = logging.StreamHandler()
            terminal_handler.setFormatter(formatter)
            self.logger.addHandler(terminal_handler)


    def start_timer(self, message=''):
        """Start a new timer"""
        if message != '':
            self.write(message)
            
        self._start_time = time.perf_counter()

    def step_timer(self, message=''):
        """Current timer value"""
        t = time.perf_counter() - self._start_time
        if message == '':
            self.write(f'{t:0.8f}')
        else:
            self.write(f'{message} = {t:0.8f}')
        return t

    def stop_timer(self, message=''):
        """Stop the timer, and report the elapsed time"""
        t = time.perf_counter() - self._start_time
        if message == '':
            self.write(f'{t:0.8f}')
        else:
            self.write(f'{message} = {t:0.8f}')
        return t

    def get_time(self):
        return time.perf_counter()

    def write_blank_line(self):
        """Write info message to log file"""
        self.logger.info(' ')
        # if self._show_terminal:
        #   print(f'LOG: {message}')

    def write(self, message=''):
        """Write info message to log file"""
        self.logger.info(message)
        # if self._show_terminal:
        #   print(f'LOG: {message}')

    def write_warning(self, message=''):
        """Write warning message to log file"""
        self.logger.warning('WARNING: ' + message)
        # if self._show_terminal:
        #   print(f'LOG: {message}')

    def write_error(self, message=''):
        """Write error message to log file"""
        self.logger.error('ERROR: ' + message)
        # if self._show_terminal:
        #   print(f'LOG: {message}')

# ===============================================================================================
class Plots:
    """ Create plots for reports """
    def __init__(self, title=''):
        self._title = title

    def line(self, xdata, ydata,
                  desc='', title='', x_label='', y_label='', show_plot=True, filename=''):
        # fig, ax = plt.subplots()
        plt.plot(xdata, ydata)

        if title == '':
            title = self._title

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        # fig.savefig("test.png")
        if filename != '':
            plt.savefig(filename)

        if show_plot:
            plt.show()

    def bar(self, xdata, ydata,
                 desc='', title='', x_label='', y_label='', show_plot=True, filename=''):

        plt.bar(xdata, ydata)

        if title == '':
            title = self._title

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        # fig.savefig("test.png")
        if filename != '':
            plt.savefig(filename)

        if show_plot:
            plt.show()




class CSE251Turtle:

    # Consts values
    COMMAND_UP = 1
    COMMAND_GOTO = 2
    COMMAND_DOWN = 3
    COMMAND_FORWARD = 4
    COMMAND_LEFT = 5
    COMMAND_RIGHT = 6
    COMMAND_BACKWARD = 7
    COMMAND_COLOR = 8
    COMMAND_SETHEADING = 9
    COMMAND_PENSIZE = 10

    SLEEP = 0.00001

    def __init__(self):
        self.commands = []

    def pensize(self, size):
        self.commands.append((self.COMMAND_PENSIZE, size))

    def move(self, x, y):
        self.up()
        self.goto(x, y)
        self.down()

    def up(self):
        self.commands.append((self.COMMAND_UP, ))

    def goto(self, x, y):
        self.commands.append((self.COMMAND_GOTO, x, y))

    def down(self):
        self.commands.append((self.COMMAND_DOWN, ))

    def forward(self, amount):
        time.sleep(self.SLEEP)
        self.commands.append((self.COMMAND_FORWARD, amount))

    def backward(self, amount):
        time.sleep(self.SLEEP)
        self.commands.append((self.COMMAND_BACKWARD, amount))

    def left(self, amount):
        self.commands.append((self.COMMAND_LEFT, amount))

    def right(self, amount):
        self.commands.append((self.COMMAND_RIGHT, amount))

    def color(self, color):
        self.commands.append((self.COMMAND_COLOR, color))

    def setheading(self, amount):
        self.commands.append((self.COMMAND_SETHEADING, amount))

    def clear(self):
        self.commands = []

    def print_commands(self):
        # print(self.commands)
        print(f'There are {len(self.commands)} commands created')

    def get_command_count(self):
        return len(self.commands)

    def play_commands(self, tur):
        for action in self.commands:
            code = action[0]
            if code == self.COMMAND_UP:
                tur.up()
            elif code == self.COMMAND_GOTO:
                tur.goto(action[1], action[2])
            elif code == self.COMMAND_DOWN:
                tur.down()
            elif code == self.COMMAND_FORWARD:
                tur.forward(action[1])
            elif code == self.COMMAND_LEFT:
                tur.left(action[1])
            elif code == self.COMMAND_RIGHT:
                tur.right(action[1])
            elif code == self.COMMAND_BACKWARD:
                tur.backward(action[1])
            elif code == self.COMMAND_COLOR:
                tur.color(action[1])
            elif code == self.COMMAND_SETHEADING:
                tur.setheading(action[1])
            elif code == self.COMMAND_PENSIZE:
                tur.pensize(action[1])
            else:
                print(f'Invalid action found: {action}')


class Screen:

    # Consts values
    COMMAND_MOVE = 1
    COMMAND_COLOR = 2
    COMMAND_UPDATE = 3
    COMMAND_BLOCK = 4
    COMMAND_LINE = 5

    def __init__(self, width, height):
        self.commands = []
        self.width = width
        self.height = height

        self.board = np.zeros((width, height, 3), dtype=np.uint8)

    def __del__(self):
        cv2.destroyAllWindows()

    def background(self, color):
        pt1 = (0, 0)
        pt2 = (self.width, self.height)
        cv2.rectangle(self.board, pt1, pt2, color, -1)

    def move(self, x, y):
        self.commands.append((self.COMMAND_MOVE, int(x), int(y)))

    def color(self, color):
        self.commands.append((self.COMMAND_COLOR, color))

    def clear(self):
        self.commands = []

    def print_commands(self):
        # print(self.commands)
        print(f'There are {len(self.commands)} commands created')

    def get_command_count(self):
        return len(self.commands)

    def line(self, x1, y1, x2, y2, color='black'):
        self.commands.append((self.COMMAND_LINE, int(x1), int(y1), int(x2), int(y2), color))

    def update(self):
        self.commands.append((self.COMMAND_UPDATE, ))

    def block(self, x, y, width, height, color='black'):
        self.commands.append((self.COMMAND_BLOCK, int(x), int(y), int(width), int(height), color))

    def play_commands(self, speed=0):
        pos_x = 0
        pos_y = 0
        color = (0, 0, 0)
        sleep_time = speed * 10
        finish = False

        title = 'Maze: Press "q" to quit, "f" to finish, "-" to slow down, "+" to go faster, "p" to play again'

        cv2.namedWindow(title)

        for action in self.commands:
            # print(action)
            code = action[0]
            if   code == self.COMMAND_MOVE:
                pos_x = action[1]
                pos_y = action[2]

            elif code == self.COMMAND_COLOR:            
                color = action[1]

            elif code == self.COMMAND_UPDATE:
                if not finish:
                    cv2.imshow(title, self.board)
                    if sleep_time > 0:
                        key = cv2.waitKey(sleep_time)
                    else:
                        key = cv2.waitKey(1)

                    if key == 27 or key == ord('q') or key == ord('Q'):
                        return False

                    if key == ord('f') or key == ord('F'):
                        finish = True

            elif code == self.COMMAND_LINE:
                cv2.line(self.board, (action[1], action[2]), (action[3], action[4]), action[5], 1)

            elif code == self.COMMAND_BLOCK:
                cv2.rectangle(self.board, (action[1], action[2]), (action[1] + action[3], action[2] + action[4]), action[5], -1)

            else:
                print(f'Invalid action found: {action}')

        cv2.imshow(title, self.board)
        return True



COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_VISITED = (128, 128, 128)

OPEN = 1
WALL = 2
VISITED = 3

class Maze():

    def __init__(self, screen, width, height, bitmap_file, delay=False):
        super().__init__()
        self.screen = screen
        self.filename = bitmap_file
        self.screen_w = width
        self.screen_h = height
        self.delay = delay

        # numpy array
        self.pixels = cv2.imread(bitmap_file, 0)

        self.width, self.height = self.pixels.shape

        self.start_pos = (0, 1)
        self.end_pos = (self.width - 1, self.height - 2)
        
        self.border_size = 50

        self.scale_w = (self.screen_w - self.border_size) / self.width
        self.scale_h = (self.screen_h - self.border_size) / self.height
        self.offset_x = self.border_size // 2
        self.offset_y = self.border_size // 2

        self.colors = [ [COLOR_BLACK for _ in range(self.height)] for _ in range(self.width)]
        # Set colors
        for row in range(self.height):
            for col in range(self.width):
                if self.pixels[row, col] == 255:
                    self.colors[row][col] = COLOR_WHITE

        self._draw()


    def move(self, row, col, color):
        """ Change a color of a square """
        state = self._state(row, col)
        if state != OPEN:
            print(f'ERROR: You are trying to move on a spot that is a wall or already visited: {row}, {col}, color = {self.colors[row][col]}')
            return

        self.colors[row][col] = color
        pos_x, pos_y = self._calc_screen_pos(row, col)
        self.screen.block(pos_x, pos_y, self.scale_w, self.scale_h, color=color)
        self.screen.update()
        if self.delay:
            time.sleep(0.00000001)

    def restore(self, row, col):
        """ Change the color to show that this square was visited """
        self.colors[row][col] = COLOR_VISITED
        pos_x, pos_y = self._calc_screen_pos(row, col)
        self.screen.block(pos_x, pos_y, self.scale_w, self.scale_h, color=COLOR_VISITED)
        self.screen.update()


    def can_move_here(self, row, col):
        """ Is the square free to move to """
        return self._state(row, col) == OPEN


    def get_possible_moves(self, row, col):
        """ Given a square location, returns possible moves """
        if not self._pos_ok(row, col):
            return []

        possible = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        random.shuffle(possible)

        moves = []
        for x, y in possible:
            if self._state(x, y) == OPEN:
                moves.append((x, y))

        return moves


    def get_start_pos(self):
        """ Return the starting position of the maze """
        return self.start_pos


    def at_end(self, row, col):
        """ Did we reach the end of the maze """
        return self.end_pos == (row, col)


    # *************************************************************************
    # Local methods for this class - don't call directly

    def _draw(self):
        # Assume that the background on the screen is black
        for row in range(self.height):
            for col in range(self.width):
                if self._state(row, col) == OPEN:
                    pos_x, pos_y = self._calc_screen_pos(row, col)
                    self.screen.block(pos_x, pos_y, self.scale_w, self.scale_h, color=COLOR_WHITE)
                else:
                    pos_x, pos_y = self._calc_screen_pos(row, col)
                    self.screen.block(pos_x, pos_y, self.scale_w, self.scale_h, color=COLOR_BLACK)
        self.screen.update()

    def _state(self, x, y):
        if x < 0 or y < 0 or x >= self.height or y >= self.width:
            return WALL
        if self.colors[x][y] == COLOR_WHITE:
            return OPEN
        else:
            return WALL

    def _calc_screen_pos(self, x, y):
        pos_x = (self.scale_w * x) + self.offset_x
        pos_y = (self.scale_h * y) + self.offset_y
        return (pos_x, pos_y)

    def _pos_ok(self, x, y):
        if x < 0 or y < 0 or x >= self.height or y >= self.width:
            return False
        return True
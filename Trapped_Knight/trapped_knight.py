# Copyright © 2024 Charles Theetten
# Tous droits réservés.
#

# pylint: disable=C0301, C0200, E0611, E1101

################################################################################

""" Trapped Knight """

################################################################################

import  argparse
import  sys
import  numpy   as np
import  pygame

################################################################################

from    pygame  import init
from    pygame  import display
from    pygame  import draw
from    pygame  import Rect
from    pygame  import time
from    pygame  import QUIT

################################################################################

BLACK   = (0, 0, 0)
WHITE   = (244, 246, 247)
BLUE    = (28, 40, 51)
LIME    = (0, 255, 0)
FUCHSIA = (255, 0, 255)
AQUA    = (0, 255, 255)

################################################################################

class ChessBoard():
    """ ChessBoard class """

    ############################################################################

    def __init__(self, dim, origin, delay):
        """ init function """
        self.dim    = dim
        self.origin = origin
        self.delay  = delay
        self.start  = None
        self.coor   = None
        self.win    = None
        self.board  = None
        self.size   = 0
        self.init   = False
        self.path   = []

        self.init_pygame()
        self.reset()

    ############################################################################

    def reset(self):
        """ reset function """
        self.init   = True
        self.path   = []

        if self.origin == 0:
            self.init_board_diag()
        else:
            self.init_board_center()

        self.draw_board()

    ############################################################################

    def init_pygame(self):
        """ init_pygame function """
        init()

        self.win    = display.set_mode((1200, 1200), 0, 32)
        self.size   = self.win.get_height() / self.dim

        display.set_caption("Trapped Knight")
        display.update()

    ############################################################################

    def init_board_diag(self):
        """ init_board_diag function """
        self.board  = np.ones((self.dim, self.dim), dtype = np.uint16)
        n           = 1

        for i in range(self.dim):
            for j in range(i + 1):
                self.board[j][i - j] = n
                n += 1

        n = self.dim * self.dim

        for i in range(self.dim - 1):
            for j in range(i + 1):
                self.board[self.dim - 1 - j][self.dim - i - 1 + j] = n
                n -= 1

    ############################################################################

    def init_board_center(self):
        """ init_board_center function """
        self.board          = np.ones((self.dim, self.dim), dtype = np.uint16)
        i                   = 0 if (self.dim & 1) == 0 else self.dim - 1
        j                   = i + 1 if (self.dim & 1) == 0 else i - 1
        k                   = self.dim * self.dim
        self.board[i][i]    = k
        direction           = "E" if (self.dim & 1) == 0 else "W"

        while k > 1:
            if direction == "E":
                while j < self.dim and self.board[i][j] == 1:
                    k -= 1
                    self.board[i][j] = k
                    j += 1
                direction = "S"
                j -= 1
                i += 1
            if direction == "S":
                while i < self.dim and self.board[i][j] == 1:
                    k -= 1
                    self.board[i][j] = k
                    i += 1
                direction = "W"
                i -= 1
                j -= 1
            if direction == "W":
                while j >= 0 and self.board[i][j] == 1:
                    k -= 1
                    self.board[i][j] = k
                    j -= 1
                direction = "N"
                j += 1
                i -= 1
            if direction == "N":
                while i >= 0 and self.board[i][j] == 1:
                    k -= 1
                    self.board[i][j] = k
                    i -= 1
                direction = "E"
                i += 1
                j += 1

    ############################################################################

    def init_start(self, pos):
        """ init_start function """
        x = int(pos[0] // self.size)
        y = int(pos[1] // self.size)

        print(x, y)
        self.start  = np.array([y, x])
        self.coor   = self.start
        radius      = self.size / 4
        x_center    = self.coor[1] * self.size + self.size / 2
        y_center    = self.coor[0] * self.size + self.size / 2

        draw.circle(self.win, LIME, (x_center, y_center), radius)
        display.update()

        self.init = True

    ############################################################################

    def trapped_knight(self):
        """ trapped_knight function """
        steps   = self.dim * self.dim
        moves   = np.array(([-2, -1], [-2, 1], [2, 1], [2, -1],
                            [-1, -2], [-1, 2], [1, 2], [1, -2]))

        self.path.append(self.board[self.coor[0]][self.coor[1]])

        for i in range(0, steps):
            valid_cases = self.start + moves
            mask_x      = (valid_cases > -1).all(axis = 1)
            valid_cases = valid_cases[mask_x, :]
            mask_y      = (valid_cases < self.dim).all(axis = 1)
            valid_cases = valid_cases[mask_y, :]
            new_cases   = []

            for i in range(len(valid_cases)):
                case = self.board[valid_cases[i][0]][valid_cases[i][1]]
                if case not in self.path:
                    new_cases.append(case)

            if len(new_cases) == 0:
                break

            case        = min(new_cases)
            self.start  = np.argwhere(self.board == case)[0]
            self.coor   = np.append(self.coor, self.start)
            self.path.append(case)

        print(np.array(self.path))

    ############################################################################

    def draw_board(self):
        """ draw_board function """
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if (i + j) & 1 == 0:
                    draw.rect(self.win, BLACK, Rect(j * self.size, i * self.size, self.size, self.size))
                else:
                    draw.rect(self.win, BLUE, Rect(j * self.size, i * self.size, self.size, self.size))
            j = 0
            i += self.size

        display.update()

    ############################################################################

    def draw_path(self):
        """ draw_path function """
        for i in range(2, len(self.coor), 2):
            y1 = self.coor[i - 2] * self.size + self.size / 2
            x1 = self.coor[i - 1] * self.size + self.size / 2
            y2 = self.coor[i] * self.size + self.size / 2
            x2 = self.coor[i + 1] * self.size + self.size / 2

            draw.line(self.win, WHITE, (x1, y1), (x2, y2), 2)
            draw.circle(self.win, AQUA, (x2, y2), self.size / 6)
            time.delay(self.delay)
            display.update()

        draw.circle(self.win, FUCHSIA, (x2, y2), self.size / 4)
        display.update()

    ############################################################################

    def solve(self):
        """ solve function """
        if self.init is True:
            self.trapped_knight()
            self.draw_path()
            self.init = False

    ############################################################################

    def run(self):
        """ run function """
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.reset()
                        self.init_start(pygame.mouse.get_pos())
                    if event.button == 3:
                        self.solve()

################################################################################

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("DIMENSION", help = "values in {4... 100}.", type = int)
    parser.add_argument("ORIGIN",  help = "values in {0, 1}.", type = int)
    parser.add_argument("DELAY",  help = "values in {1... 1000}.", type = float)

    args = parser.parse_args()

    try:
        if args.DIMENSION not in range(4, 101):
            raise argparse.ArgumentTypeError(f"DIMENSION : {args.DIMENSION} is an invalid value.")
        if args.ORIGIN not in [0, 1]:
            raise argparse.ArgumentTypeError(f"ORIGIN : {args.ORIGIN} is an invalid value.")
        if args.DELAY not in range(1, 1001):
            raise argparse.ArgumentTypeError(f"DELAY : {args.DELAY} is an invalid value.")
    except argparse.ArgumentTypeError as e:
        print(f"Argument Error - {e}\n")
        parser.print_help()
        sys.exit(-1)

################################################################################

def main():
    """ main function"""
    check_args()

    dim     = int(sys.argv[1])
    origin  = int(sys.argv[2])
    delay   = int(sys.argv[3])

    chessboard = ChessBoard(dim, origin, delay)
    chessboard.run()

    pygame.quit()

################################################################################

if __name__ == '__main__':
    main()

################################################################################

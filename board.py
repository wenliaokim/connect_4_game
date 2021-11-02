

class Board:
    """A class representing a game board"""
    def __init__(self, row, column, size_base):
        """Initialize instance attributes"""
        self.DIVISION = 2
        self.row = row
        self.column = column
        self.size_base = size_base
        self.half_size_base = self.size_base/self.DIVISION
        self.board_limit = self.row*self.column
        self.played_disks = 0
        # Initialize a board with zero value representing no disk in the
        # corresponding position
        self.board = [[0]*self.column for i in range(self.row)]
        # A list with nested list collecting played disks in each column
        self.columns_list = [[] for i in range(self.column)]
        self.new_disk = (-1, -1)
        self.board_full = -1

    def draw_board(self):
        """Draw a board"""
        STROKEWEIGHT = 20
        COLOR_BLUE = (0, 0, 1)
        noFill()
        strokeWeight(STROKEWEIGHT)
        stroke(*COLOR_BLUE)
        for i in range(self.row + 1):
            line(0, self.size_base*(i + 1),
                 self.column*self.size_base, self.size_base*(i + 1))
        for j in range(self.column + 1):
            line(self.size_base*j, self.size_base,
                 self.size_base*j, (self.row + 1)*self.size_base)

    def add_to_board(self, row_index, column_index, player):
        """
        Add a played disk to the board, with 1 representing player's disk,
        2 representing computer's disk
        """
        self.board[row_index][column_index] = player
        self.columns_list[column_index].insert(0, player)
        self.played_disks += 1
        self.new_disk = (row_index, column_index)

    def get_row_index(self, column_index):
        if len(self.columns_list[column_index]) < self.row:
            row_index = self.row \
                        - len(self.columns_list[column_index]) \
                        - 1
            return row_index
        else:
            return None

    def check_board_status(self):
        """
        Check if new played disk will connect four of same colored disks in
        a row, or if the board is full of disks
        """
        INCRE_1 = DECRE_1 = 1
        INCRE_2 = DECRE_2 = 2
        INCRE_3 = DECRE_3 = 3
        MIN_LENGTH = 4

        x = self.new_disk[0]
        y = self.new_disk[1]

        if (x != -1) and (y != -1):
            # Check if the new disk will achieve 4 in a row vertically
            if len(self.columns_list[y]) >= MIN_LENGTH:
                if (
                      self.columns_list[y][0]
                      == self.columns_list[y][INCRE_1]
                      == self.columns_list[y][INCRE_2]
                      == self.columns_list[y][INCRE_3]):
                    return self.columns_list[y][0]
            # Check if the new disk will achieve 4 in a row horizontally
            i = 0
            while (i < MIN_LENGTH) and (y - i >= 0):
                left_y = y - i
                i += 1
            j = 0
            while (j < MIN_LENGTH) and (y + j < self.column):
                right_y = y + j
                j += 1
            for k in range(left_y, right_y - DECRE_3 + 1):
                if (
                      self.board[x][k]
                      == self.board[x][k + INCRE_1]
                      == self.board[x][k + INCRE_2]
                      == self.board[x][k + INCRE_3]):
                    return self.board[x][k]
            # Check if the new disk will achieve 4 in a row diagonally
            # (the direction is from upper left to lower right)
            i = 0
            while (i < MIN_LENGTH) and (x - i >= 0) and (y - i >= 0):
                left_x = x - i
                left_y = y - i
                i += 1
            j = 0
            while (
                    (j < MIN_LENGTH)
                    and (x + j < self.row) and (y + j < self.column)):
                right_x = x + j
                right_y = y + j
                j += 1
            if i + j > MIN_LENGTH:
                k = 0
                while (left_x + k + DECRE_3 <= right_x):
                    new_x = left_x + k
                    new_y = left_y + k
                    if (
                          self.board[new_x][new_y]
                          == self.board[new_x + INCRE_1][new_y + INCRE_1]
                          == self.board[new_x + INCRE_2][new_y + INCRE_2]
                          == self.board[new_x + INCRE_3][new_y + INCRE_3]):
                        return self.board[new_x][new_y]
                    k += 1
            # Check if the new disk will achieve 4 in a row diagonally
            # (the direction is from upper right to lower left)
            i = 0
            while (i < MIN_LENGTH) and (x + i < self.row) and (y - i >= 0):
                left_x = x + i
                left_y = y - i
                i += 1
            j = 0
            while (j < MIN_LENGTH) and (x - j >= 0) and (y + j < self.column):
                right_x = x - j
                right_y = y + j
                j += 1
            if i + j > MIN_LENGTH:
                k = 0
                while (left_x - k - DECRE_3 >= right_x):
                    new_x = left_x - k
                    new_y = left_y + k
                    if (
                          self.board[new_x][new_y]
                          == self.board[new_x - DECRE_1][new_y + INCRE_1]
                          == self.board[new_x - DECRE_2][new_y + INCRE_2]
                          == self.board[new_x - DECRE_3][new_y + INCRE_3]):
                        return self.board[new_x][new_y]
                    k += 1
            # If the game is not over by the new played disk, check if the
            # board is full
            if self.played_disks == self.board_limit:
                return self.board_full

        return 0

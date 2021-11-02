from board import Board
from disk import Disk
from computer import Computer


class GameController:
    """A class for controlling the simplified 2*2 board game"""
    def __init__(self, row, column, size_base):
        """Initialize the attributes"""
        self.DIVISION = 2
        self.human_disk = 1
        self.computer_disk = 2
        self.row = row
        self.column = column
        self.size_base = size_base
        self.half_size_base = size_base/self.DIVISION
        self.start_y = self.half_size_base
        self.disk_x = 0
        self.disk_y = self.half_size_base
        self.row_index = -1
        self.column_index = -1
        self.result_text = ""
        # this boolean value is to control disk's appearance or disappearance
        # in the empty area above the board when we hold mouse
        self.pre_to_drop = False
        # this boolean value is to make sure that disk won't appear in the area
        # above the board even with mouse held unlesss previous disk has landed
        self.allow_pre = True
        # this boolean value is to allow the disk to start dropping, which is
        # mainly controlled by mouseReleased()
        self.start_drop = False
        self.is_human_turn = True
        self.is_computer_turn = False
        self.is_game_over = False
        self.is_human_win = False
        self.computer_depth = 0
        self.b = Board(self.row, self.column, self.size_base)
        self.d = Disk(self.half_size_base, self.human_disk, self.computer_disk)

    def display(self):
        """Update game state on every frame"""
        self.check_game_status()
        if not self.is_game_over:
            self.draw_pre_to_drop_disk()
            self.draw_drop_disk()
            self.announce_whose_turn()
        self.d.display_played_disks()
        self.b.draw_board()
        if self.is_game_over:
            self.draw_result_text()
            print(self.result_text)

    def draw_pre_to_drop_disk(self):
        """Draw disk in the empty area above the board"""
        if (
              self.pre_to_drop
              and self.allow_pre
              and (0 <= mouseY <= self.size_base)):
            to_drop_column = mouseX // self.size_base
            disk_x = self.half_size_base + to_drop_column*self.size_base
            self.d.draw_disk(disk_x, self.start_y, self.human_disk)

    def draw_drop_disk(self):
        """Draw dropping disk"""
        DROP_SPEED = 20
        DELAY_TIME = 100

        # If it's human's turn and the human player played a legal disk,
        # calculate the coordinate, the row and column indexes of the disk
        if self.start_drop and self.is_human_turn:
            if mouseY > self.size_base or mouseY < 0:
                self.start_drop = False
                return
            self.allow_pre = False
            if self.start_y == self.half_size_base:
                self.column_index = mouseX // self.size_base
                self.row_index = self.b.get_row_index(self.column_index)
                self.disk_x = (self.half_size_base +
                               self.column_index*self.size_base)
                if self.row_index is not None:
                    self.disk_y = (self.size_base*(self.row_index + 1) +
                                   self.half_size_base)
                # If human player played an illegal move (the column is full)
                else:
                    self.start_drop = False
                    self.allow_pre = True
                    return

        # If it's computer's turn, calculate the coordinate, the row and column
        # indexes of the position that computer picked to play
        elif self.is_computer_turn:
            if self.start_y == self.half_size_base:
                comp = Computer(self.b, self.computer_disk, self.human_disk, int(self.computer_depth))
                move = comp.computer_move()
                self.row_index = move[0]
                self.column_index = move[1]
                self.disk_x = (self.half_size_base +
                               self.column_index*self.size_base)
                self.disk_y = (self.size_base*(self.row_index + 1) +
                               self.half_size_base)
                delay(DELAY_TIME)

        # If it's not computer's turn, or it's human player's turn but the
        # player doesn't release the mouse, then don't draw dropping disk
        else:
            return

        if self.is_human_turn:
            player = self.human_disk
        else:
            player = self.computer_disk

        # Draw the dropping animation
        if self.start_y < self.disk_y:
            self.d.draw_disk(self.disk_x, self.start_y, player)
            self.start_y += DROP_SPEED
        # After the disk landed, add the disk into the list of played disks
        # and the board, change the player's turn
        else:
            self.start_y = self.half_size_base
            self.d.add_played_disk(self.disk_x, self.disk_y, player)
            self.b.add_to_board(self.row_index,
                                self.column_index,
                                player)
            if self.is_human_turn:
                self.is_human_turn = False
                self.is_computer_turn = True
            else:
                self.is_computer_turn = False
                self.is_human_turn = True
                self.allow_pre = True
                self.start_drop = False

    def announce_whose_turn(self):
        """
        Announce whose turn it is each time over the empty area above the board
        """
        TEXT_SIZE = 20
        if self.is_human_turn:
            turn = "Human's turn"
        else:
            turn = "Computer's turn"
        fill(0)
        textSize(TEXT_SIZE)
        textAlign(CENTER)
        text(turn, self.column*self.half_size_base, self.half_size_base)

    def draw_result_text(self):
        """Draw message above the board when the game is over"""
        TEXT_SIZE = 40
        fill(0)
        textSize(TEXT_SIZE)
        textAlign(CENTER)
        text(self.result_text,
             self.column*self.half_size_base,
             self.half_size_base)

    def check_game_status(self):
        """Check if the game is over"""
        if not self.is_game_over:
            result = self.b.check_board_status()
            if result != 0:
                if result == self.human_disk:
                    self.result_text = "Game Over! Human Wins!"
                    self.is_human_win = True
                elif result == self.computer_disk:
                    self.result_text = "Game Over! Computer Wins!"
                else:
                    self.result_text = "Game Over! Board is Full."
                self.is_game_over = True

    def record_winner_name(self, name):
        """
        If human player wins, record the winner's winning time to scores.txt,
        and rank the winners from highest score to lowest score
        """
        winners = {}
        f = open('scores.txt', 'r+')
        for line in f:
            line_break = line.rstrip().rfind(" ")
            player_name = line[: line_break]
            count = int(float(line[line_break + 1:]))
            winners[player_name] = count
        if name in winners.keys():
            winners[name] += 1
        else:
            winners[name] = 1
        sorted_list = sorted(winners.items(),
                             key=lambda x: x[1],
                             reverse=True)
        f.seek(0)
        for i in range(len(sorted_list) - 1):
            to_write_text = sorted_list[i][0] + " " + str(sorted_list[i][1])
            f.write(to_write_text + "\n")
        to_write_text = sorted_list[-1][0] + " " + str(sorted_list[-1][1])
        f.write(to_write_text)
        f.close()

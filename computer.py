import copy
import random


class Computer:
    def __init__(self, board, computer_disk, human_disk, depth):
        """Initialize instance attributes"""
        self.b = copy.deepcopy(board)
        self.computer_disk = computer_disk
        self.human_disk = human_disk
        self.max_start_score = -1000
        self.mini_start_score = 1000
        self.depth = depth

    def computer_move(self):
        """Get the best move for computer"""
        # DEPTH = 4

        best_score = self.max_start_score
        best_move = None
        legal_moves = self.get_legal_moves(self.b)
        for move in legal_moves:
            temp_b = copy.deepcopy(self.b)
            x = move[0]
            y = move[1]
            temp_b.add_to_board(x, y, self.computer_disk)
            score = self.minimax(temp_b, self.depth, self.max_start_score,
                                 self.mini_start_score, False)
            if (score > best_score):
                best_score = score
                best_move = move
        return best_move

    def get_legal_moves(self, board):
        """
        Get legal moves for player
        Object -> List
        """
        # moves_1 is for the potential moves whose columns are close to the
        # disk that the other player just played
        moves_1 = []
        moves_2 = []
        for column_index, column in enumerate(board.columns_list):
            if len(column) < board.row:
                row_index = board.row - len(column) - 1
                move = (row_index, column_index)
                if abs(column_index - board.new_disk[1]) <= 1:
                    moves_1.append(move)
                else:
                    moves_2.append(move)
        random.shuffle(moves_1)
        random.shuffle(moves_2)
        legal_moves = moves_1 + moves_2
        return legal_moves

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm"""
        board_status = board.check_board_status()
        if board_status == self.human_disk:
            return -1*(depth + 1)
        elif board_status == self.computer_disk:
            return 1*(depth + 1)
        elif board_status == board.board_full:
            return 0

        if depth == 0:
            return 0

        if is_maximizing:
            best_score = self.max_start_score
            legal_moves = self.get_legal_moves(board)
            for move in legal_moves:
                temp_b = copy.deepcopy(board)
                x = move[0]
                y = move[1]
                temp_b.add_to_board(x, y, self.computer_disk)
                score = self.minimax(temp_b, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = self.mini_start_score
            legal_moves = self.get_legal_moves(board)
            for move in legal_moves:
                temp_b = copy.deepcopy(board)
                x = move[0]
                y = move[1]
                temp_b.add_to_board(x, y, self.human_disk)
                score = self.minimax(temp_b, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

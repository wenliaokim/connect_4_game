from computer import Computer
from board import Board

COMP_DISK = 2
HUMAN_DISK = 1
MAX_START_SCORE = -1000
MINI_START_SCORE = 1000
TEST_AGRU1 = (2, 5, 100)
MOVE1 = (1, 3)
TEST_AGRU2 = (3, 3, 100)
MOVE2 = (0, 2)
INDEX_TWO = 2
SCORE = 2


def test_constructor():
    """Test constructor of Computer class"""
    board = Board(0, 0, 0)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    assert isinstance(comp.b, Board)
    assert comp.computer_disk == COMP_DISK
    assert comp.human_disk == HUMAN_DISK
    assert comp.max_start_score == MAX_START_SCORE
    assert comp.mini_start_score == MINI_START_SCORE


def test_computer_move():
    """Test computer_move method in Computer class"""
    # Test if the computer will pick the move that will stop human player from
    # winning the game
    board = Board(*TEST_AGRU1)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    comp.b.board = [
                    [0, COMP_DISK, COMP_DISK, 0, 0],
                    [HUMAN_DISK, HUMAN_DISK, HUMAN_DISK, 0, 0],
                   ]
    comp.b.columns_list = [
                            [COMP_DISK, HUMAN_DISK],
                            [COMP_DISK, HUMAN_DISK],
                            [HUMAN_DISK],
                            [],
                            [],
                          ]
    comp.b.new_disk = (1, 0)
    assert comp.computer_move() == (MOVE1)

    # Test if the computer will pick the move that will make it win the game
    board = Board(*TEST_AGRU1)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    comp.b.board = [
                    [HUMAN_DISK, 0, HUMAN_DISK, HUMAN_DISK, 0],
                    [HUMAN_DISK, 0, COMP_DISK, COMP_DISK, COMP_DISK],
                   ]
    comp.b.columns_list = [
                            [HUMAN_DISK, HUMAN_DISK],
                            [],
                            [HUMAN_DISK, COMP_DISK],
                            [HUMAN_DISK, COMP_DISK],
                            [],
                          ]
    comp.b.new_disk = (MOVE2)
    assert comp.computer_move() == (1, 1)


def test_get_legal_moves():
    """Test get_legal_moves method in Computer class"""
    board = Board(*TEST_AGRU2)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    comp.b.columns_list = [
                            [HUMAN_DISK],
                            [HUMAN_DISK, HUMAN_DISK],
                            [HUMAN_DISK, HUMAN_DISK, HUMAN_DISK]
                          ]
    comp.b.new_disk = (MOVE2)
    assert set(comp.get_legal_moves(comp.b)) == {(1, 0), (0, 1)}


def test_minimax():
    """Test minimax method in Computer class"""
    board = Board(*TEST_AGRU1)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    comp.b.board = [
                    [COMP_DISK, COMP_DISK, 0, 0, 0],
                    [HUMAN_DISK, HUMAN_DISK, HUMAN_DISK, 0, 0],
                   ]
    comp.b.columns_list = [
                            [COMP_DISK, HUMAN_DISK],
                            [COMP_DISK, HUMAN_DISK],
                            [HUMAN_DISK],
                            [],
                            [],
                          ]
    comp.b.add_to_board(0, INDEX_TWO, COMP_DISK)
    assert comp.minimax(comp.b, 1, MAX_START_SCORE, MINI_START_SCORE, False) \
           == -1

    board = Board(*TEST_AGRU1)
    comp = Computer(board, COMP_DISK, HUMAN_DISK)
    comp.b.board = [
                    [HUMAN_DISK, 0, HUMAN_DISK, HUMAN_DISK, 0],
                    [HUMAN_DISK, 0, COMP_DISK, COMP_DISK, COMP_DISK],
                   ]
    comp.b.columns_list = [
                            [HUMAN_DISK, HUMAN_DISK],
                            [],
                            [HUMAN_DISK, COMP_DISK],
                            [HUMAN_DISK, COMP_DISK],
                            [],
                          ]
    comp.b.add_to_board(1, 1, COMP_DISK)
    assert comp.minimax(comp.b, 1, MAX_START_SCORE, MINI_START_SCORE, False) \
           == SCORE

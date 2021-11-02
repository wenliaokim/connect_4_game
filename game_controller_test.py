from game_controller import GameController
from board import Board
from disk import Disk

DIVISION = 2
TEST_ARGU1 = (4, 5, 200)
TEST_ARGU2 = (2, 2, 100)
TEST_ARGU3 = (1, 4, 100)
HUMAN_DISK = 1
COMPUTER_DISK = 2
INDEX_TWO = 2
INDEX_THREE = 3


def test_constructor():
    """Test constructor of the GameController class"""
    gc = GameController(*TEST_ARGU1)
    assert gc.DIVISION == DIVISION
    assert gc.row == TEST_ARGU1[0]
    assert gc.column == TEST_ARGU1[1]
    assert gc.size_base == TEST_ARGU1[INDEX_TWO]
    assert gc.half_size_base == TEST_ARGU1[INDEX_TWO] / DIVISION
    assert gc.start_y == TEST_ARGU1[INDEX_TWO] / DIVISION
    assert gc.disk_x == 0
    assert gc.disk_y == TEST_ARGU1[INDEX_TWO] / DIVISION
    assert gc.row_index == -1
    assert gc.column_index == -1
    assert gc.human_disk == HUMAN_DISK
    assert gc.computer_disk == COMPUTER_DISK
    assert gc.result_text == ""
    assert gc.pre_to_drop is False
    assert gc.allow_pre is True
    assert gc.start_drop is False
    assert gc.is_human_turn is True
    assert gc.is_computer_turn is False
    assert gc.is_game_over is False
    assert gc.is_human_win is False
    assert isinstance(gc.b, Board)
    assert isinstance(gc.d, Disk)


def test_check_game_status():
    """Test check_game_status method in GameController class"""
    # When the game is not over
    gc = GameController(*TEST_ARGU2)
    gc.check_game_status()
    assert gc.is_game_over is False
    assert gc.is_human_win is False

    # When the game is over and it's not human player win the game
    gc.b.add_to_board(1, 1, HUMAN_DISK)
    gc.b.add_to_board(1, 0, HUMAN_DISK)
    gc.b.add_to_board(0, 1, HUMAN_DISK)
    gc.b.add_to_board(0, 0, HUMAN_DISK)
    gc.check_game_status()
    assert gc.is_game_over is True
    assert gc.is_human_win is False

    # When the game is over and it's human player win the game
    gc = GameController(*TEST_ARGU3)
    gc.b.add_to_board(0, 0, HUMAN_DISK)
    gc.b.add_to_board(0, 1, HUMAN_DISK)
    gc.b.add_to_board(0, INDEX_TWO, HUMAN_DISK)
    gc.b.add_to_board(0, INDEX_THREE, HUMAN_DISK)
    gc.check_game_status()
    assert gc.is_game_over is True
    assert gc.is_human_win is True

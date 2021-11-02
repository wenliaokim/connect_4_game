from board import Board

PLAYER1 = 1
PLAYER2 = 2
INDEX_TWO = 2
DIVISION_FACTOR = 2
TEST_AGRU1 = (4, 6, 50)
ADD_DISK = (1, 3)
TEST_ARGU2 = (2, 2, 100)
TEST_ARGU3 = (5, 2, 100)
TEST_ARGU4 = (1, 5, 100)
TEST_ARGU5 = (4, 6, 100)
TEST_ARGU6 = (4, 4, 100)


def test_constructor():
    """Test constructor of the Board class"""
    board = Board(*TEST_AGRU1)
    assert board.row == TEST_AGRU1[0]
    assert board.column == TEST_AGRU1[1]
    assert board.size_base == TEST_AGRU1[INDEX_TWO]
    assert board.half_size_base == TEST_AGRU1[INDEX_TWO] / DIVISION_FACTOR
    assert board.board_limit == TEST_AGRU1[0]*TEST_AGRU1[1]
    assert board.played_disks == 0
    assert board.board == [
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                          ]
    assert board.columns_list == [[], [], [], [], [], []]
    assert board.new_disk == (-1, -1)
    assert board.board_full == -1

    board = Board(0, 0, 0)
    assert board.board == []
    assert board.columns_list == []

    board = Board(*TEST_ARGU2)
    assert board.board == [[0, 0], [0, 0]]
    assert board.columns_list == [[], []]


def test_add_to_board():
    """Test add_to_board method in Board class"""
    board = Board(*TEST_AGRU1)
    assert board.board[ADD_DISK[0]][ADD_DISK[1]] == 0
    assert board.columns_list[ADD_DISK[1]] == []
    assert board.played_disks == 0
    assert board.new_disk == (-1, -1)

    board.add_to_board(ADD_DISK[0], ADD_DISK[1], PLAYER1)
    assert board.board[ADD_DISK[0]][ADD_DISK[1]] == PLAYER1
    assert board.columns_list[ADD_DISK[1]] == [1]
    assert board.played_disks == 1
    assert board.new_disk == (ADD_DISK)


def test_get_row_index():
    """Test get_row_index method in Board class"""
    board = Board(*TEST_ARGU2)
    assert board.get_row_index(0) == 1

    board.add_to_board(1, 0, 1)
    assert board.get_row_index(0) == 0

    board.add_to_board(0, 0, 1)
    assert board.get_row_index(0) is None


def test_check_board_status():
    """Test check_board_status method in Board class"""
    board = Board(*TEST_ARGU3)
    assert board.check_board_status() == 0

    # Connect four in a row vertically
    board.columns_list = [[], [PLAYER1, PLAYER1, PLAYER1]]
    board.add_to_board(1, 1, PLAYER1)
    assert board.check_board_status() == PLAYER1

    # Doesn't connect four in a row vertically
    board.columns_list = [[], [PLAYER1, PLAYER1, PLAYER1]]
    board.add_to_board(1, 1, PLAYER2)
    assert board.check_board_status() == 0

    # Connect four in a row horizontally
    board = Board(*TEST_ARGU4)
    board.board = [[PLAYER1, PLAYER1, 0, PLAYER1, PLAYER1]]
    board.add_to_board(0, INDEX_TWO, PLAYER1)
    assert board.check_board_status() == PLAYER1

    # Doesn't connect four in a row horizontally
    board.board = [[PLAYER1, PLAYER1, 0, PLAYER1, PLAYER1]]
    board.add_to_board(0, INDEX_TWO, PLAYER2)
    assert board.check_board_status() == 0

    # Connect four in a row diagonally (from lower left to upper right)
    board = Board(*TEST_ARGU5)
    board.board = [
                    [0, 0, 0, PLAYER1, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, PLAYER1, 0, 0, 0, 0],
                    [PLAYER1, 0, 0, 0, 0, 0],
                  ]
    board.add_to_board(1, INDEX_TWO, PLAYER1)
    assert board.check_board_status() == PLAYER1

    # Doesn't connect four in a row diagonally
    board.board = [
                    [0, 0, 0, PLAYER1, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, PLAYER1, 0, 0, 0, 0],
                    [PLAYER1, 0, 0, 0, 0, 0],
                  ]
    board.add_to_board(1, INDEX_TWO, PLAYER2)
    assert board.check_board_status() == 0

    # Connect four in a row diagonally (from lower right to upper left)
    board.board = [
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, PLAYER2, 0, 0],
                    [0, 0, 0, 0, PLAYER2, 0],
                    [0, 0, 0, 0, 0, PLAYER2],
                  ]
    board.add_to_board(0, INDEX_TWO, PLAYER2)
    assert board.check_board_status() == PLAYER2

    # Doesn't connect four in a row diagonally
    board.board = [
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, PLAYER2, 0, 0],
                    [0, 0, 0, 0, PLAYER2, 0],
                    [0, 0, 0, 0, 0, PLAYER2],
                  ]
    board.add_to_board(0, INDEX_TWO, PLAYER1)
    assert board.check_board_status() == 0

    # When no player wins and the board is full
    board = Board(*TEST_ARGU6)
    board.board = [
                    [PLAYER1, PLAYER2, 0, PLAYER1],
                    [PLAYER2, PLAYER1, PLAYER2, PLAYER1],
                    [PLAYER1, PLAYER1, PLAYER2, PLAYER2],
                    [PLAYER1, PLAYER2, PLAYER2, PLAYER1],
                  ]
    board.played_disks = TEST_ARGU6[0]*TEST_ARGU6[1] - 1
    board.add_to_board(0, INDEX_TWO, PLAYER1)
    assert board.check_board_status() == board.board_full

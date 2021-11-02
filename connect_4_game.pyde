from game_controller import GameController

ROW = 6
COLUMN = 7
SIZE_BASE = 100
COLOR_GRAY = (0.8, 0.8, 0.8)
gc = GameController(ROW, COLUMN, SIZE_BASE)


def setup():
    """Defines initial enviroment properties"""
    size(COLUMN*SIZE_BASE, (ROW + 1)*SIZE_BASE)
    colorMode(RGB, 1)
    gc.computer_depth = input('input difficulity')


def draw():
    """Display the game"""
    background(*COLOR_GRAY)
    if gc.is_game_over:
        if gc.is_human_win:
            player_name = input('Enter your name')
            if player_name is not None:
                gc.record_winner_name(player_name)
        noLoop()
    gc.display()


def mousePressed():
    """Control the movement of disk in the empty area above the board"""
    gc.pre_to_drop = True


def mouseReleased():
    """Start disk's drop animation"""
    gc.pre_to_drop = False
    gc.start_drop = True


def input(self, message=''):
    """Define input function"""
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)

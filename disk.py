

class Disk:
    """A class for representing disk"""
    def __init__(self, radius, player1, player2):
        """Initialize instance attributes"""
        self.radius = radius
        self.played_disks = []
        self.first_player = player1
        self.second_player = player2

    def draw_disk(self, x, y, player):
        """Draw disk"""
        MULTIPLE = 2
        COLOR_RED = (1, 0, 0)
        COLOR_YELLOW = (1, 1, 0)
        noStroke()
        if player == self.first_player:
            fill(*COLOR_RED)
        else:
            fill(*COLOR_YELLOW)
        ellipse(x, y, self.radius*MULTIPLE, self.radius*MULTIPLE)

    def add_played_disk(self, x, y, player):
        """Add played disk to the list"""
        self.played_disks.append((x, y, player))

    def display_played_disks(self):
        """Display played disks"""
        for disk in self.played_disks:
            self.draw_disk(*disk)

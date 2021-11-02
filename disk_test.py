from disk import Disk

RADIUS = 50
FIRST_PLAYER = 1
SECOND_PLAYER = 2
TEST_ARGU = (100, 50, 1)


def test_constructor():
    """Test constructor of Disk class"""
    disk = Disk(RADIUS, FIRST_PLAYER, SECOND_PLAYER)
    assert disk.radius == RADIUS
    assert disk.first_player == FIRST_PLAYER
    assert disk.second_player == SECOND_PLAYER
    assert len(disk.played_disks) == 0


def test_add_played_disk():
    """Test add_player_disk() method in Disk class"""
    disk = Disk(RADIUS, FIRST_PLAYER, SECOND_PLAYER)
    assert len(disk.played_disks) == 0

    disk.add_played_disk(*TEST_ARGU)
    assert TEST_ARGU in disk.played_disks
    assert len(disk.played_disks) == 1

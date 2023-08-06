from roxbot.interfaces import Pose


def test_pose():
    p = Pose(1, 2, 3)

    assert p.xy == (1, 2)

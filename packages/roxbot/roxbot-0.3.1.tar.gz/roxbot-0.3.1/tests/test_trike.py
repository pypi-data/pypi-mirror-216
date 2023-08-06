""" test trike model

for interactive geometry see: https://www.geogebra.org/calculator/rea6w9a2

"""
from math import radians

from pytest import approx

from roxbot.models import TrikeModel


def test_curvature_calc():
    m = TrikeModel(-1.0, 1.0)

    # straight line
    m.steering_angle = 0.0
    assert m.curvature == 0.0

    # 45 deg turn
    m.steering_angle = radians(45)
    assert m.curvature == approx(-1)

    # -45 deg turn
    m.steering_angle = radians(-45)
    assert m.curvature == approx(1)


def test_velocity_calc():
    m = TrikeModel(-1.0, 1.0)

    # straight line
    m.steering_angle = 0.0
    m.velocity = 1.0
    assert m.velocity == 1.0

    vels = m.wheel_speeds
    assert vels[0] == approx(1.0)
    assert vels[1] == approx(1.0)

    # 45 deg turn
    m.steering_angle = radians(45)
    vl, vr = m.wheel_speeds
    assert vl == approx(1.5)
    assert vr == approx(0.5)

    # other angle
    m.steering_angle = radians(30.07)
    vl, vr = m.wheel_speeds
    assert vl == approx(1.289, abs=0.01)
    assert vr == approx(0.711, abs=0.01)

    # other angle
    m.steering_angle = radians(-20.025)
    vl, vr = m.wheel_speeds
    assert vl == approx(0.818, abs=0.01)
    assert vr == approx(1.182, abs=0.01)

    # slow down
    m.velocity = 0.5
    m.steering_angle = radians(-45)
    assert m.curvature == approx(1, abs=0.001)
    vl, vr = m.wheel_speeds
    assert vl == approx(0.25)
    assert vr == approx(0.75)


def test_steering_angle():
    m = TrikeModel(-1.0, 1.0)

    m.velocity = 1.0
    m.steering_angle = 0.5
    assert m.steering_angle == 0.5

#!/usr/bin/env python3
"""
 tests for trike simulator

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

from roxbot.simulators.trike import TrikeSimulator


def get_state(trike: TrikeSimulator):
    """get state of the trike"""
    return (
        trike.drive_wheels[0].velocity_ms,
        trike.drive_wheels[1].velocity_ms,
        trike.steering.val,
    )


def test_trike():
    """test initialization"""
    trike = TrikeSimulator()
    assert isinstance(trike, TrikeSimulator)

    trike.set_vels((1, 1))
    trike.set_steering(0.1)

    vl, vr, s = get_state(trike)
    assert vl == 0
    assert vr == 0
    assert s == 0

    trike.step(1)
    vl, vr, s = get_state(trike)
    assert vl == 1
    assert vr == 1
    assert s == 0.1

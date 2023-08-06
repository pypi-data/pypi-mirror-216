#!/usr/bin/env python3
"""
 common interface definitions

 Copyright (c) 2023 ROX Automation
"""

from typing import NamedTuple, Tuple


class Pose(NamedTuple):
    """2D pose interface"""

    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

#!/usr/bin/env python3
"""
 Kinematic for wheeled robots

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov

 ## References

* https://www.cs.columbia.edu/~allen/F19/NOTES/icckinematics.pdf

**units** All units are SI (meters, radians, seconds), unless otherwise noted in variable names,
for example `anggle_deg` is in degrees.

**coordinate system** : the coordinate system is right handed, with the x-axis pointing forward,
the y-axis pointing to the left and the z-axis pointing up.

"""

import math
from typing import Optional
from roxbot.utils import sign


class LinearModel:
    """Simple linear model for generating setpoints."""

    __slots__ = ("val", "roc", "setpoint", "min_val", "max_val")

    def __init__(
        self,
        roc: float,
        val: float = 0.0,
        setpoint: Optional[float] = None,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
    ):
        """
        Args:
            roc (float): rate of change / sec
            val (float): current value
            setpoint (float, optional): target value.
            max_val (float, optional): maximum value
            min_val (float, optional): minimum value
        """

        self.val = val
        self.roc = roc
        if setpoint is None:
            self.setpoint = val
        else:
            self.setpoint = setpoint

        self.min_val = min_val
        self.max_val = max_val

    def step(self, dt: float) -> None:
        """perform timestep"""

        if dt < 0:
            raise ValueError(f"dt must be positive, got {dt=} ")

        error = self.setpoint - self.val
        step = sign(error) * self.roc * dt

        if abs(step) > abs(error):
            self.val += error
        else:
            self.val += step

        if self.max_val is not None:
            self.val = min(self.val, self.max_val)

        if self.min_val is not None:
            self.val = max(self.val, self.min_val)


class Wheel:
    """simple wheel model with a linear speed profile"""

    def __init__(self, diameter: float, accel: float):
        """create a wheel wit LinearModel driver and a diameter"""
        self._diameter = diameter
        self._circumference = math.pi * self._diameter
        self.time = 0.0

        # angular velocity model
        self._model = LinearModel(roc=accel)

        self.revolutions = 0.0

    @property
    def rps(self) -> float:
        """revolutions per second"""
        return self._model.val

    @property
    def velocity_ms(self):
        return self._circumference * self.rps

    @property
    def distance(self) -> float:
        return self.revolutions * self._circumference

    def set_velocity_ms(self, v: float) -> None:
        self._model.setpoint = v / self._circumference

    def step(self, dt: float) -> None:
        self._model.step(dt)
        self.revolutions += self.rps * dt
        self.time += dt


class TrikeModel:
    """
    ## Kinematic model of a trike


    Trike model is a combination of a bycicle and and a differential drive kinematic models.

    Key features are:

    * the path curvature is governed by steering wheel
    * movement command interface is `(velocity,steering angle)`
    * differential speeds for the driving wheels are calculated from the driving curvature.


    !!! note
        The steering wheel axle can be behind driving wheels resulting in rear wheel steering
        To achieve this, use negative `L` value.


    ### Geometry

    !!! note
        Axes in Geogebra model are different from the ones used in this model.
        This model uses right handed coordinate system with x-axis pointing forward, y-axis pointing to the left and z-axis pointing up.

    <iframe src="https://www.geogebra.org/calculator/rea6w9a2?embed" width="800" height="800" allowfullscreen style="border: 1px solid #e4e4e4;border-radius: 4px;" frameborder="0"></iframe>


    """

    __slots__ = ("L", "B", "wheel_diameter", "_steering_angle", "_velocity")

    def __init__(
        self, L: float = 1.0, B: float = 0.8, wheel_diameter: float = 0.4
    ) -> None:
        """create kinematic model of a trike

        Args:
            L (float, optional): length, distance between front and back axles. Defaults to 1.0.
            B (float, optional): wheel base. Defaults to 0.8.
            wheel_diameter (float, optional): Driving wheel diameter. Defaults to 0.4.
        """

        self.L = L
        self.B = B
        self.wheel_diameter = wheel_diameter

        self._steering_angle = 0.0  # steering angle in radians
        self._velocity = 0.0

    @property
    def velocity(self) -> float:
        """velocity in m/s"""
        return self._velocity

    @velocity.setter
    def velocity(self, v: float) -> None:
        """set velocity in m/s"""
        self._velocity = v

    @property
    def steering_angle(self) -> float:
        """steering angle in radians"""
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, angle: float) -> None:
        """set steering angle in radians"""
        self._steering_angle = angle

    @property
    def curvature(self) -> float:
        """driving curvature"""
        return math.tan(self._steering_angle) / self.L

    @property
    def wheel_speeds(self) -> tuple[float, float]:
        """driving wheel speeds in m/s"""
        c = self.curvature

        return (
            self.velocity * (1 - c * self.B / 2),
            self.velocity * (1 + c * self.B / 2),
        )

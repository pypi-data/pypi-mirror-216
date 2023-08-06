#!/usr/bin/env python3
"""
 Simulator for a trike robot

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import pydantic

from roxbot.models import TrikeModel, Wheel, LinearModel


@pydantic.dataclasses.dataclass
class Config:
    """configuration for trike simulator"""

    L = -1.1  # length between the axles. Negative means rear wheel steering.
    B = 0.8  # width of the robot
    wheel_diameter = 0.4  # meters
    wheel_accel = 10  # revolutions per second squared

    steer_accel = 1.0  # radians per second squared


class TrikeSimulator:
    """simulate motion of a trike robot"""

    def __init__(self, config: Config = Config()):
        """initialize the simulator, provide a config object to change the default parameters"""
        self.config = config

        # create a kinematic model for internal calculations
        self._model = TrikeModel(
            L=config.L, B=config.B, wheel_diameter=config.wheel_diameter
        )

        # create 2 driving wheels
        self.drive_wheels = [
            Wheel(config.wheel_diameter, config.wheel_accel) for _ in range(2)
        ]

        # create a steering wheel
        self.steering = LinearModel(config.steer_accel)

    def set_vels(self, vels: tuple[float, float]) -> None:
        """set wheel velocities in m/s"""

        # set wheel velocities
        for wheel, vel in zip(self.drive_wheels, vels):
            wheel.set_velocity_ms(vel)

    def set_steering(self, angle: float) -> None:
        """set steering angle in radians"""
        self.steering.setpoint = angle

    def step(self, dt: float) -> None:
        """step the simulation by dt seconds"""

        # step the wheels
        for wheel in self.drive_wheels:
            wheel.step(dt)

        # step the steering
        self.steering.step(dt)

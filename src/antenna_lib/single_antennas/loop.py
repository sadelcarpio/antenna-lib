import numpy as np

from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna
from scipy.special import jv


class LoopAntenna(SingleAntenna):

    def __init__(self, radius: float, polarization: str = 'linear@90.0', amplitude: float = 1.0):
        self.radius = radius
        super().__init__(polarization, amplitude)

    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        if self.radius <= 1 / (6 * np.pi):
            return np.sin(theta)
        return jv(1, 2 * np.pi * self.radius * np.sin(theta))

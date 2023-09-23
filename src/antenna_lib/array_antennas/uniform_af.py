import numpy as np

from antenna_lib.array_antennas.af_strategy import AFStrategy


class UniformAFStrategy(AFStrategy):

    def __init__(self, n_elements: int, spacing: float, phase_progression: float):
        self.n_elements = n_elements
        self.spacing = spacing
        self.phase_progression = phase_progression * np.pi / 180

    def af(self, theta, phi):
        kd = 2 * np.pi * self.spacing
        return sum(np.exp(1j * n * (kd * np.cos(theta) + self.phase_progression)) for n in range(self.n_elements))

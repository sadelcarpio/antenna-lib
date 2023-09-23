import numpy as np

from antenna_lib.array_antennas.af_strategy import AFStrategy


class NonUniformAFStrategy(AFStrategy):

    def __init__(self, amplitudes: list, spacing: float, phase_progression: float):
        self.amplitudes = amplitudes
        self.spacing = spacing
        self.phase_progression = phase_progression * np.pi / 180

    def af(self, theta, phi):
        kd = 2 * np.pi * self.spacing
        psi = kd * np.cos(theta) + self.phase_progression
        return sum(amplitude * np.exp(1j * n * psi) for n, amplitude in enumerate(self.amplitudes))

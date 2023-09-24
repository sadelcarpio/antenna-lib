import numpy as np

from antenna_lib.antenna_parameters import Polarization
from antenna_lib.array_antennas.array import AntennaArray
from antenna_lib.single_antennas import SingleAntenna


class NonUniformAntennaArray(AntennaArray):

    def __init__(self, antenna: SingleAntenna, amplitudes: list[float], spacing: float = 0.5,
                 phase_progression: float = 0.0):
        super().__init__(antenna, spacing, phase_progression)
        self.amplitudes = amplitudes
        self.n_elements = len(amplitudes)

    @property
    def polarization(self) -> Polarization:
        if self._polarization is None:
            pol = sum(
                [(amplitude * self.antenna.polarization) * np.exp(1j * k * self.phase_progression)
                 for k, amplitude in enumerate(self.amplitudes)])
            self._polarization = Polarization(pol / np.linalg.norm(pol))
            return self._polarization
        return self._polarization

    def array_factor(self, theta: float, phi: float) -> float:
        kd = 2 * np.pi * self.spacing
        psi = kd * np.cos(theta) + self.phase_progression
        return np.abs(sum(amplitude * np.exp(1j * n * psi) for n, amplitude in enumerate(self.amplitudes)))

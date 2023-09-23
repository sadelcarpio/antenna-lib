import numpy as np

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import Polarization
from antenna_lib.array_antennas.af_strategy import AFStrategy
from antenna_lib.single_antennas import SingleAntenna


class AntennaArray(Antenna):
    def __init__(self,
                 antenna: SingleAntenna,
                 n_elements: int,
                 spacing: float = 0.5,
                 phase_progression: float = 0.0,
                 array_factor_strategy: AFStrategy = None):
        super().__init__()
        self.antenna = antenna
        self.n_elements = n_elements
        self.spacing = spacing
        self.phase_progression = phase_progression
        self._array_factor_strategy = array_factor_strategy
        self._polarization = None

    @property
    def polarization(self):
        """Calcular la polarización resultante a partir de las antenas que conforman el array"""
        if self._polarization is None:
            pol = sum(
                [self.antenna.amplitude * self.antenna.polarization.pol_vector * np.exp(1j * k * self.phase_progression)
                 for k in range(self.n_elements)])
            self._polarization = Polarization(pol / np.linalg.norm(pol))
            return self._polarization
        return self._polarization

    def array_factor(self, theta, phi):
        return self._array_factor_strategy.af(theta, phi)

    def field_pattern(self, theta, phi):
        return self.antenna.field_pattern(theta, phi) * self.array_factor(theta, phi)

    def directivity(self, theta: float, phi: float):
        """Implementation for this antenna type"""

    def max_directivity(self):
        """Implementation for this antenna type"""

    def plot_radiation_pattern(self, polar=True, field=False, log_scale=False):
        """Implementation for this antenna type"""

    def play_wave_animation(self):
        """Implementation for this antenna type"""

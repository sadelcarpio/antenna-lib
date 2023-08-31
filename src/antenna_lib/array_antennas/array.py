import numpy as np

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import Polarization


class AntennaArray(Antenna):
    def __init__(self, antennas: list[Antenna]):
        super().__init__()
        self.antennas = antennas
        self._polarization = None

    @property
    def polarization(self):
        """Calcular la polarización resultante a partir de las antenas que conforman el array"""
        if self._polarization is None:
            pol = sum([antenna.amplitude * antenna.polarization.pol_vector for antenna in self.antennas])
            self._polarization = Polarization(pol / np.linalg.norm(pol))
            return self._polarization
        return self._polarization

    def directivity(self, theta, phi):
        """Implementation for this antenna type"""

    def plot_radiation_pattern(self, plot_type='polar', field=False):
        """Implementation for this antenna type"""

    def play_wave_animation(self):
        """Implementation for this antenna type"""

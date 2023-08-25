import numpy as np

from src.antenna_parameters import Polarization
from src.antenna import Antenna


class AntennaArray(Antenna):
    def __init__(self, antennas: list[Antenna] = None):
        super().__init__()
        if antennas is None:
            antennas = []
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

    def directivity(self, angle):
        # Implementation for this antenna type
        pass

    def plot_radiation_pattern(self):
        # Implementation for this antenna type
        pass

    def play_wave_animation(self):
        # Implementation for this antenna type
        pass

from abc import abstractmethod, ABC

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import Polarization
from antenna_lib.single_antennas import SingleAntenna


class AntennaArray(Antenna):
    def __init__(self,
                 antenna: SingleAntenna,
                 spacing: float = 0.5,
                 phase_progression: float = 0.0):
        super().__init__()
        self.antenna = antenna
        self.spacing = spacing
        self.phase_progression = phase_progression
        self.n_elements = None
        self.amplitudes = None
        self._polarization = None

    def field_pattern(self, theta, phi):
        return self.antenna.field_pattern(theta, phi) * self.array_factor(theta, phi)

    @abstractmethod
    def array_factor(self, theta: float, phi: float) -> float:
        pass

    @property
    @abstractmethod
    def polarization(self) -> Polarization:
        """Calcular la polarización resultante a partir de las antenas que conforman el array"""
        pass

    def play_wave_animation(self):
        """Implementation for this antenna type"""

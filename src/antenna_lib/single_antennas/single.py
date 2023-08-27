from abc import ABC

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import PolarizationFactory


class SingleAntenna(Antenna, ABC):

    def __init__(self, polarization: str, amplitude: float):
        super().__init__()
        self.amplitude = amplitude
        self.polarization = PolarizationFactory.create_polarization(polarization)

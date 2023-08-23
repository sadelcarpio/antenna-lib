from abc import ABC

from src.antenna import Antenna
from src.antenna_parameters.polarization import PolarizationFactory


class SingleAntenna(Antenna, ABC):
    def __init__(self, polarization: str):
        super().__init__()
        self.polarization = PolarizationFactory.create_polarization(polarization)

from src.antenna_parameters.params import Polarization
from src.antenna import Antenna


class SingleAntenna(Antenna):
    def __init__(self, polarization: Polarization = None):
        super().__init__()
        self.polarization = polarization

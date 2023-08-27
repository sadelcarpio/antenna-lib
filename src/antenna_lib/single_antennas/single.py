from antenna_lib.antenna_parameters.params import Polarization
from antenna_lib.antenna import Antenna


class SingleAntenna(Antenna):
    def __init__(self, polarization: Polarization = None):
        super().__init__()
        self.polarization = polarization

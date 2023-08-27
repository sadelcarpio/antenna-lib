from antenna_lib.antenna_parameters.params import Polarization
from antenna_lib.single_antennas.single import SingleAntenna


class DipoleAntenna(SingleAntenna):
    def __init__(self, length: float, polarization: Polarization = None):
        super().__init__(polarization)
        self.length = length

    def directivity(self, angle):
        # Implementation for this antenna type
        pass

    def plot_radiation_pattern(self):
        # Implementation for this antenna type
        pass

    def play_wave_animation(self):
        # Implementation for this antenna type
        pass

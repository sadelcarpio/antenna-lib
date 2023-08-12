from src.antenna_parameters.params import Polarization
from src.single_antennas.single import SingleAntenna


class LoopAntenna(SingleAntenna):
    def __init__(self, radius: float, polarization: Polarization = None):
        super().__init__(polarization)
        self.radius = radius

    def directivity(self, angle):
        # Implementation for this antenna type
        pass

    def plot_radiation_pattern(self):
        # Implementation for this antenna type
        pass

    def play_wave_animation(self):
        # Implementation for this antenna type
        pass

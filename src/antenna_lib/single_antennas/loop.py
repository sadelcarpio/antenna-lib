from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna


class LoopAntenna(SingleAntenna):

    def __init__(self, radius: float, polarization: str = 'linear@0', amplitude: float = 1.0):
        super().__init__(amplitude)
        self.radius = radius
        self.polarization = PolarizationFactory.create_polarization(polarization)

    def directivity(self, theta, phi):
        """Implementation for this antenna type"""

    def plot_radiation_pattern(self, plot_type='polar', field=False):
        """Implementation for this antenna type"""

    def play_wave_animation(self):
        """Implementation for this antenna type"""

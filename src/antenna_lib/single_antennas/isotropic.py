from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna


class IsotropicAntenna(SingleAntenna):

    """Antena isotropica. Puede tener cualquier polarización. Su patrón es siempre omnidireccional"""

    def __init__(self, polarization: str = 'linear@0.0', amplitude: float = 1.0):
        super().__init__(amplitude)
        self.polarization = PolarizationFactory.create_polarization(polarization)

    @property
    def max_directivity(self):
        return 1.0

    def directivity(self, theta, phi):
        return 1.0

    def play_wave_animation(self):
        """Implementation for this antenna type"""

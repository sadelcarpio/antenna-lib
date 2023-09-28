from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna


class IsotropicAntenna(SingleAntenna):

    """Antena isotropica. Puede tener cualquier polarización. Su patrón es siempre omnidireccional"""

    def __init__(self,
                 polarization: str = 'linear@0.0',
                 amplitude: float = 1.0):
        self.polarization = PolarizationFactory.create_polarization(polarization)
        super().__init__(amplitude)

    @property
    def max_directivity(self) -> float:
        return 1.0

    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        """Patrón de campo de antena insotropica."""
        return 1.0

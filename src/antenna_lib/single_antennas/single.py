from __future__ import annotations

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.exceptions import FieldPatternNotImplementedException


class SingleAntenna(Antenna):

    def __init__(self,
                 pol: str | float = 'linear@0.0',
                 amplitude: float = 1.0):
        super().__init__()
        self.amplitude = amplitude
        if self.polarization is None:
            self.polarization = PolarizationFactory.create_polarization(pol)
        self._radiated_power = None

    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        """Patrón de campo. Propiedad a partir de la cual se obtienen muchas de las características de la antena"""
        raise FieldPatternNotImplementedException('The antenna does not have a `field_pattern`'
                                                  ' method implemented')

    def __repr__(self):
        return f'<{self.__class__.__name__} with polarization:\n{self.polarization}'

from __future__ import annotations

from abc import ABC
from functools import partial

import numpy as np
from scipy.integrate import dblquad
from matplotlib import pyplot as plt

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.utils.decorators import rotatory


class SingleAntenna(Antenna, ABC):

    def __init__(self, pol: str | float = 0.0, amplitude: float = 1.0):
        super().__init__()
        self.amplitude = amplitude
        if isinstance(pol, str):
            if pol == 'horizontal':
                pol = 90.0
            elif pol == 'vertical':
                pol = 0.0
            else:
                raise ValueError('Invalid polarization string')
        self.angle = pol * np.pi / 180
        self.polarization = PolarizationFactory.create_polarization(f'linear@{pol}')
        self._radiated_power = None

    def field_pattern(self, theta: float, phi: float) -> float:
        """Patrón de campo. Propiedad a partir de la cual se obtienen muchas de las características de la antena"""
        pass

    @rotatory
    def _field_pattern(self, theta: float, phi: float) -> float:
        """Patrón de campo con posibilidad de rotar debdo al decorador `@rotatory`"""
        return self.amplitude * self.field_pattern(theta, phi)

    def power_pattern(self, theta: float, phi: float = 0.0) -> float:
        """Patrón de potencia, cuadrado del patrón de campo"""
        return self._field_pattern(theta, phi) ** 2

    @property
    def radiated_power(self):
        """Potencia radiada en todas las direcciones"""
        if self._radiated_power is None:
            f = lambda t, p: (self.field_pattern(t, p) ** 2) * np.sin(t)
            d_0 = dblquad(f, 0, 2 * np.pi, 0, np.pi)[0]
            return d_0
        return self._radiated_power

    def directivity(self, theta: float, phi: float = 0.0) -> float:
        """Función directividad calculada a partir del patrón de potencia y la potencia radiada"""
        return 4 * np.pi * self.power_pattern(theta, phi) / self.radiated_power

    @property
    def max_directivity(self):
        """Implementación por defecto de la directividad máxima"""
        phi = np.linspace(0, 2 * np.pi, 1000)
        theta = np.linspace(0, 2 * np.pi, 1000)
        return np.max(self._horizontal_vertical_patterns(theta, phi))

    def _horizontal_vertical_patterns(self, theta: np.ndarray, phi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        horizontal = np.array(list(map(partial(self.power_pattern, np.pi / 2), phi)))
        vertical = np.array(list(map(partial(self.power_pattern, phi=0.0), theta[:500])) +
                            list(map(partial(self.power_pattern, phi=np.pi), theta[500:])))
        return horizontal, vertical

    def plot_radiation_pattern(self, plot_type='polar', field=False):
        phi = np.linspace(0, 2 * np.pi, 1000)
        theta = np.linspace(0, 2 * np.pi, 1000)
        horizontal, vertical = self._horizontal_vertical_patterns(theta, phi)
        if field:
            horizontal, vertical = np.sqrt(horizontal), np.sqrt(vertical)
        horizontal /= np.max(horizontal)
        vertical /= np.max(vertical)
        h_plane = plt.subplot(1, 2, 1, projection='polar')
        h_plane.set_theta_zero_location('N')
        h_plane.set_theta_direction(-1)
        plt.polar(phi, horizontal)
        v_plane = plt.subplot(1, 2, 2, projection='polar')
        v_plane.set_theta_zero_location('N')
        v_plane.set_theta_direction(-1)
        plt.polar(theta, vertical)
        plt.show()

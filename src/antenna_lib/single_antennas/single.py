from __future__ import annotations

from functools import partial

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import dblquad

from antenna_lib.antenna import Antenna
from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.exceptions import FieldPatternNotImplementedException
from antenna_lib.utils.decorators import rotatory


class SingleAntenna(Antenna):

    def __init__(self, pol: str | float = 0.0, amplitude: float = 1.0):
        super().__init__()
        self.amplitude = amplitude
        self.polarization = PolarizationFactory.create_polarization(f'linear@{pol}')
        self._radiated_power = None

    def field_pattern(self, theta: float, phi: float) -> float:
        """Patrón de campo. Propiedad a partir de la cual se obtienen muchas de las características de la antena"""
        raise NotImplementedError()

    @rotatory
    def _field_pattern(self, theta: float, phi: float) -> float:
        """Patrón de campo con posibilidad de rotar debdo al decorador `@rotatory`"""
        try:
            return self.amplitude * self.field_pattern(theta, phi)
        except NotImplementedError:
            raise FieldPatternNotImplementedException('The antenna does not have a `field_pattern`'
                                                      ' method implemented')

    def power_pattern(self, theta: float, phi: float) -> float:
        """Patrón de potencia, cuadrado del patrón de campo"""
        return self._field_pattern(theta, phi) ** 2

    @property
    def radiated_power(self):
        """Potencia radiada en todas las direcciones"""
        if self._radiated_power is None:
            f = lambda t, p: (self.field_pattern(t, p) ** 2) * np.sin(t)
            self._radiated_power = dblquad(f, 0, 2 * np.pi, 0, np.pi)[0]
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
        horizontal = np.array(list(map(partial(self.directivity, np.pi / 2), phi)))
        vertical = np.array(list(map(partial(self.directivity, phi=np.pi / 2), theta[:500])) +
                            list(map(partial(self.directivity, phi=3 * np.pi / 2), theta[500:])))
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

    def plot_3d_pattern(self, field=False):
        """Gráfico 3d del patrón de radiación."""
        theta, phi = np.meshgrid(np.linspace(0, np.pi, 100), np.linspace(0, 2 * np.pi, 100))
        r_prime = np.vectorize(self.field_pattern)(theta, phi) ** (1 if field else 2)
        X_prime = r_prime * np.sin(theta) * np.cos(phi)
        Y_prime = r_prime * np.sin(theta) * np.sin(phi)
        Z_prime = r_prime * np.cos(theta)
        X = X_prime
        Y = Y_prime * np.cos(self.angle) - Z_prime * np.sin(self.angle)
        Z = Z_prime * np.cos(self.angle) + Y_prime * np.sin(self.angle)
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        ax.plot_surface(X, Y, Z, alpha=0.8, rstride=1, cstride=1, linewidth=0)
        plt.show()

    def play_wave_animation(self):
        pass

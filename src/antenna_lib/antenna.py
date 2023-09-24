import warnings
from abc import abstractmethod, ABC
from functools import partial

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import dblquad


class Antenna(ABC):
    polarization = None
    amplitude = None
    _radiated_power = None

    @abstractmethod
    def field_pattern(self, theta, phi):
        """Patrón de campo de la antena"""

    def power_pattern(self, theta: float, phi: float) -> float:
        """Patrón de potencia, cuadrado del patrón de campo"""
        return self.field_pattern(theta, phi) ** 2

    @property
    def radiated_power(self) -> float:
        """Potencia radiada en todas las direcciones"""
        if self._radiated_power is None:
            f = lambda t, p: (self.field_pattern(t, p) ** 2) * np.sin(t)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self._radiated_power = dblquad(f, 0, 2 * np.pi, 0, np.pi)[0]
        return self._radiated_power

    def directivity(self, theta: float, phi: float) -> float:
        """Función directividad calculada a partir del patrón de potencia y la potencia radiada"""
        return 4 * np.pi * self.power_pattern(theta, phi) / self.radiated_power

    @property
    def max_directivity(self) -> float:
        """Implementación por defecto de la directividad máxima"""
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2 * np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)
        r = np.vectorize(self.directivity)(theta, phi)
        return np.max(r)

    def _horizontal_vertical_patterns(self, theta: np.ndarray, phi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        horizontal = np.array(list(map(partial(self.power_pattern, np.pi / 2), phi)))
        vertical = np.array(list(map(partial(self.power_pattern, phi=np.pi / 2), theta)) +
                            list(map(partial(self.power_pattern, phi=3 * np.pi / 2), np.flip(theta))))
        return horizontal, vertical

    def plot_radiation_pattern(self, polar=True, field=False, log_scale=False):
        phi = np.linspace(0, 2 * np.pi, 200)
        theta_pattern = np.linspace(0, np.pi, 100)
        horizontal, vertical = self._horizontal_vertical_patterns(theta_pattern, phi)
        theta = np.linspace(0, 2 * np.pi, 200)
        if field:
            horizontal, vertical = np.sqrt(horizontal), np.sqrt(vertical)
        horizontal /= np.max(horizontal)
        vertical /= np.max(vertical)
        plt.subplots_adjust(wspace=0.4)
        h_plane = plt.subplot(1, 2, 1, projection='polar')
        v_plane = plt.subplot(1, 2, 2, projection='polar')
        if log_scale:
            horizontal = 10 * np.log10(1e-4 + horizontal)
            vertical = 10 * np.log10(1e-4 + vertical)
            h_plane.set_rlim(-40)
            v_plane.set_rlim(-40)
        h_plane.set_theta_zero_location('N')
        h_plane.set_theta_direction(-1)
        h_plane.plot(phi, horizontal)
        v_plane.set_theta_zero_location('N')
        v_plane.set_theta_direction(-1)
        v_plane.plot(theta, vertical)
        plt.show()

    def plot_3d_pattern(self, field=False):
        """Gráfico 3d del patrón de radiación."""
        theta, phi = np.meshgrid(np.linspace(0, np.pi, 100), np.linspace(0, 2 * np.pi, 100))
        r = np.vectorize(self.field_pattern)(theta, phi) ** (1 if field else 2)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        # to have same length in all axes
        max_range = np.array([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()]).max() / 2.0
        mid_x = (x.max() + x.min()) * 0.5
        mid_y = (y.max() + y.min()) * 0.5
        mid_z = (z.max() + z.min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        # cmap according to r value
        norm = plt.Normalize(0, np.max(r))
        colors = norm(r)
        cmap = plt.cm.get_cmap('jet')
        ax.plot_surface(x, y, z, alpha=0.8, rstride=1, cstride=1, cmap='jet', facecolors=cmap(colors),
                        linewidth=0, shade=True)
        plt.show()

    @abstractmethod
    def play_wave_animation(self):
        """Reproducir una animación de la onda"""

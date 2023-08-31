from abc import ABC
from functools import partial

import numpy as np
from matplotlib import pyplot as plt

from antenna_lib.antenna import Antenna


class SingleAntenna(Antenna, ABC):

    def __init__(self, amplitude: float):
        super().__init__()
        self.amplitude = amplitude

    def _horizontal_vertical_patterns(self, theta: np.ndarray, phi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        horizontal = np.array(list(map(partial(self.directivity, np.pi / 2), phi)))
        vertical = np.array(list(map(partial(self.directivity, phi=0.0), theta[:500])) +
                            list(map(partial(self.directivity, phi=np.pi), theta[500:])))
        horizontal[np.isnan(horizontal)] = 0.0
        vertical[np.isnan(vertical)] = 0.0
        return horizontal, vertical

    def plot_radiation_pattern(self, plot_type='polar', field=False):
        phi = np.linspace(0, 2 * np.pi, 1000)
        theta = np.linspace(0, 2 * np.pi, 1000)
        horizontal, vertical = self._horizontal_vertical_patterns(theta, phi)
        h_plane = plt.subplot(1, 2, 1, projection='polar')
        h_plane.set_theta_zero_location('N')
        h_plane.set_theta_direction(-1)
        plt.polar(phi, horizontal)
        v_plane = plt.subplot(1, 2, 2, projection='polar')
        v_plane.set_theta_zero_location('N')
        v_plane.set_theta_direction(-1)
        plt.polar(theta, vertical)
        plt.show()

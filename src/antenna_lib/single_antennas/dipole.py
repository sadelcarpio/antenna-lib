from __future__ import annotations

import numpy as np

from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna
from antenna_lib.utils.decorators import rotable


class DipoleAntenna(SingleAntenna):

    def __init__(self, length: float, pol: float | str = 0.0, amplitude: float = 1.0):
        super().__init__(amplitude)
        self.length = length
        if isinstance(pol, str):
            if pol == 'horizontal':
                pol = 90.0
            elif pol == 'vertical':
                pol = 0.0
            else:
                raise ValueError('Invalid polarization string')
        self.angle = pol * np.pi / 180
        self.polarization = PolarizationFactory.create_polarization(f'linear@{pol}')

    @property
    def max_directivity(self):
        """Calculate max directivity"""
        if self.length <= 0.1:
            return 1.5
        elif self.length >= 1.0:
            phi = np.linspace(0, 2 * np.pi, 1000)
            theta = np.linspace(0, 2 * np.pi, 1000)
            return np.max(self._horizontal_vertical_patterns(theta, phi)[1])
        else:
            return self.directivity(np.pi / 2 - self.angle)

    @rotable
    def directivity(self, theta, phi=0.0):
        """Implementation for this antenna type"""
        kl = 2 * self.length
        # Falta la superconstante D0
        if self.length <= 0.1:
            return 1.5 * np.sin(theta) ** 2
        return ((np.cos(np.pi * kl / 2 * np.cos(theta)) - np.cos(
            np.pi * kl / 2)) / np.sin(theta)) ** 2

    def play_wave_animation(self):
        """Implementation for this antenna type"""

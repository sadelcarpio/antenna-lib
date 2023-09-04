from __future__ import annotations

import numpy as np

from antenna_lib.single_antennas.single import SingleAntenna


class DipoleAntenna(SingleAntenna):

    def __init__(self, length: float, pol: float | str = 0.0, amplitude: float = 1.0):
        super().__init__(pol=pol, amplitude=amplitude)
        if length <= 0:
            raise ValueError('Dipole length must be greater than zero.')
        self.length = length

    @property
    def max_directivity(self):
        """Calculate max directivity"""
        if self.length <= 0.1:
            return 1.5
        elif self.length >= 1.0:
            return super().max_directivity
        else:
            return self.directivity(np.pi / 2 - self.angle, 0.0)

    def field_pattern(self, theta, phi=0.0):
        kl = 2 * self.length
        if self.length <= 0.1:
            return np.sin(theta)
        e = ((np.cos(np.pi * kl / 2 * np.cos(theta)) - np.cos(np.pi * kl / 2)) / np.sin(theta))
        return 0.0 if np.isnan(e) else e

    def play_wave_animation(self):
        """Implementation for this antenna type"""

    def __repr__(self):
        return f'<Dipole antenna with polarization:\n{self.polarization}>'

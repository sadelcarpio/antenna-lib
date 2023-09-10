from __future__ import annotations

import numpy as np

from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna
from antenna_lib.utils.decorators import rotatory


class DipoleAntenna(SingleAntenna):

    def __init__(self, length: float, pol: str | float = 0.0, amplitude: float = 1.0):
        if length <= 0:
            raise ValueError('Dipole length must be greater than zero.')
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
        super().__init__(amplitude=amplitude)

    @property
    def max_directivity(self):
        """Calculate max directivity"""
        if self.length <= 0.1:
            return 1.5
        elif self.length >= 1.0:
            return super().max_directivity
        else:
            return self.directivity(np.pi / 2 - self.angle, 0.0)

    @rotatory
    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        kl = 2 * self.length
        if self.length <= 0.1:
            return np.sin(theta)
        e = ((np.cos(np.pi * kl / 2 * np.cos(theta)) - np.cos(np.pi * kl / 2)) / np.sin(theta))
        return 0.0 if np.isnan(e) else e

    def __repr__(self):
        return f'<Dipole antenna with polarization:\n{self.polarization}>'

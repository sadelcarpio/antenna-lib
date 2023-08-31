import matplotlib.pyplot as plt
import numpy as np
from functools import partial

from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.single_antennas.single import SingleAntenna


class DipoleAntenna(SingleAntenna):

    def __init__(self, length: float, angle: float = 0.0, amplitude: float = 1.0):
        super().__init__(amplitude)
        self.length = length
        self.angle = angle * np.pi / 180
        self.polarization = PolarizationFactory.create_polarization(f'linear@{angle}')

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

    def directivity(self, theta, phi=0.0):
        """Implementation for this antenna type"""
        tilt = self.angle
        kl = 2 * self.length
        # Falta la superconstante D0
        if self.length <= 0.1:
            r = lambda theta, phi: 1.5 * np.sin(theta) ** 2
        else:
            r = lambda theta, phi: ((np.cos(np.pi * kl / 2 * np.cos(theta)) - np.cos(
                np.pi * kl / 2)) / np.sin(theta)) ** 2
        r_prime = lambda theta, phi: r(theta + tilt, phi)
        x_prime = lambda theta, phi: r_prime(theta, phi) * np.sin(theta) * np.cos(phi)
        y_prime = lambda theta, phi: r_prime(theta, phi) * np.sin(theta) * np.sin(phi)
        z_prime = lambda theta, phi: r_prime(theta, phi) * np.cos(theta)
        x = x_prime
        y = lambda theta, phi: y_prime(theta, phi) * np.cos(tilt) - z_prime(theta, phi) * np.sin(tilt)
        z = lambda theta, phi: z_prime(theta, phi) * np.cos(tilt) + y_prime(theta, phi) * np.sin(tilt)
        return np.linalg.norm(np.array([x(theta, phi), y(theta, phi), z(theta, phi)]))

    def play_wave_animation(self):
        """Implementation for this antenna type"""

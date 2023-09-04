from functools import wraps

import numpy as np


def rotatory(r):
    """
    Decorador que permite rotar cualquier patron de radiación sobre el eje x.
    :param r: directivity method
    :return: rotated function
    """
    @wraps(r)
    def wrapper(self, theta, phi):
        r_prime = lambda theta, phi: r(self, theta + self.angle, phi)
        x_prime = lambda theta, phi: r_prime(theta, phi) * np.sin(theta) * np.cos(phi)
        y_prime = lambda theta, phi: r_prime(theta, phi) * np.sin(theta) * np.sin(phi)
        z_prime = lambda theta, phi: r_prime(theta, phi) * np.cos(theta)
        x = x_prime(theta, phi)
        y = y_prime(theta, phi) * np.cos(self.angle) - z_prime(theta, phi) * np.sin(self.angle)
        z = z_prime(theta, phi) * np.cos(self.angle) + y_prime(theta, phi) * np.sin(self.angle)
        return np.linalg.norm([x, y, z])
    return wrapper

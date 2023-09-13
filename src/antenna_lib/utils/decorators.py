from functools import wraps

import numpy as np


def rotatory(r):
    """
    Decorador que permite rotar cualquier patron de radiación sobre el eje x.
    :param r: directivity method
    :return: rotated function
    """
    @wraps(r)
    def wrapper(self, theta: float, phi: float = 0.0):
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        x_prime = np.round(x, 10)
        y_prime = np.round(y * np.cos(self.angle) + z * np.sin(self.angle), 10)
        z_prime = np.round(z * np.cos(self.angle) - y * np.sin(self.angle), 10)
        theta_prime = np.arccos(z_prime)
        phi_prime = np.arctan2(y_prime, x_prime)
        return r(self, theta_prime, phi_prime)
    return wrapper

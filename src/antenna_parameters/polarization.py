import numpy as np

from src.exceptions import InvalidPolarizationException


class PolarizationFactory:

    @classmethod
    def create_polarization(cls, polarization: str):
        pol_vector = cls.parse_pol_vector(polarization)
        return Polarization(pol_vector)

    @classmethod
    def parse_pol_vector(cls, polarization) -> np.ndarray:
        if polarization.startswith('linear'):
            try:
                polarization_angle = float(polarization.split('@')[1]) * np.pi / 180
            except IndexError:
                raise IndexError('Invalid parameter for linear polarization angle. Format is "linear@{angle}"')
            except ValueError:
                raise ValueError('Please specify a valid float number as an angle')
            return np.array([1 * np.cos(polarization_angle), 1 * np.sin(polarization_angle)])
        elif polarization.startswith('circular'):
            try:
                polarization_orientation = polarization.split('@')[1]
                if polarization_orientation == 'lcp':
                    return np.array([1, -1j]) / np.sqrt(2)
                elif polarization_orientation == 'rcp':
                    return np.array([1, 1j]) / np.sqrt(2)
                else:
                    raise InvalidPolarizationException('No valid Polarization. Valid parameters are '
                                                       '"rcp", "lcp"')
            except IndexError:
                raise IndexError('Invalid parameter for circular polarization orientation. Format is '
                                 'circular@{orientation}')
        elif polarization.startswith('elliptical'):
            try:
                polarization_orientation = polarization.split('@')[1]
                polarization_angle = float(polarization.split('@')[2]) * np.pi / 180
                # define a vector, not unitary but easy to calculate for angle/orientation
                if polarization_orientation == 'lcp':
                    base_pol = np.array([1, np.exp(-1j * polarization_angle)])
                elif polarization_orientation == 'rcp':
                    base_pol = np.array([1, np.exp(1j * polarization_angle)])
                else:
                    raise InvalidPolarizationException('No valid Polarization. Valid parameters are '
                                                       '"rcp", "lcp"')
                return base_pol / np.linalg.norm(base_pol)  # normalize to get the unit vector
            except IndexError:
                raise IndexError('Invalid parameters for elliptical polarization. Format is '
                                 'elliptical@{orientation}@{angle}')
        else:
            raise InvalidPolarizationException("No valid polarization")


class Polarization:
    def __init__(self, pol_vector: np.ndarray):
        self.pol_vector = pol_vector

    @property
    def polarization_type(self):
        """Logica para detectar el tipo de polarización basado en el vector de polarización"""
        return

    def __add__(self, other):
        pol_vector = self.pol_vector + other.pol_vector
        return Polarization(pol_vector)

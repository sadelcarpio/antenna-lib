import numpy as np

from src.exceptions import InvalidPolarizationException


class PolarizationFactory:

    @classmethod
    def create_polarization(cls, polarization: str):
        # logic is very bloated here
        if polarization.startswith('linear'):
            try:
                polarization_angle = float(polarization.split('@')[1]) * np.pi / 180
            except IndexError:
                raise IndexError('Invalid parameter for linear polarization angle')
            except ValueError:
                raise ValueError('Please specify a valid float number as an angle')
            pol_vector = np.array([1 * np.cos(polarization_angle), 1 * np.sin(polarization_angle)])
            return Polarization(pol_vector)
        elif polarization == 'circular':
            pol_vector = np.array([1, -1j])  # [1, ij] for rcp
            return Polarization(pol_vector)
        elif polarization == 'elliptical':
            pol_vector = np.array([1 + 1j, 1 - 1j])  # not really but let's pretend
            return Polarization(pol_vector)
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

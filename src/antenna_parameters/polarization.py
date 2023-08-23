from src.exceptions import InvalidPolarizationException


class PolarizationFactory:
    @classmethod
    def create_polarization(cls, polarization: str):
        if polarization.startswith('linear'):
            try:
                polarization_angle = polarization.split('@')[1]
            except IndexError:
                raise IndexError('Invalid parameter for linear polarization angle')
            pol_vector = f'â<{polarization_angle}'  # should really be a numpy complex vector
            return Polarization(pol_vector)
        elif polarization == 'circular':
            pol_vector = 'x +- iy'  # should really be a numpy complex vector
            return Polarization(pol_vector)
        elif polarization == 'elliptical':
            pol_vector = 'J_x x + J_y y'  # should really be a numpy complex vector
            return Polarization(pol_vector)
        else:
            raise InvalidPolarizationException("No valid polarization")


class Polarization:
    def __init__(self, pol_vector: str = None):
        self.pol_vector = pol_vector

    @property
    def polarization_type(self):
        """Logica para detectar el tipo de polarización basado en el vector de polarización"""
        return

    def __add__(self, other):
        pol_vector = self.pol_vector + other.pol_vector
        return Polarization(pol_vector)

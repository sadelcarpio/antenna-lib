import numpy as np

from src.exceptions import InvalidPolarizationException


class PolarizationFactory:
    """Clase encargada de crear objetos de tipo Polarization"""

    @classmethod
    def create_polarization(cls, polarization_str: str):
        pol_vector = cls.parse_pol_vector(polarization_str)
        return Polarization(pol_vector, polarization_str)

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
    def __init__(self, pol_vector: np.ndarray, polarization_str: str = None):
        """
        Inicializa la clase Polarization, con un vector de polarización (unitario) y una representación
        en string de su polarización.
        :param pol_vector: Vector complejo unitario que representa la polarización de la onda transmitida de la antena.
        :param polarization_str: Representación en string.
        """
        self.pol_vector = pol_vector
        self._polarization_str = polarization_str

    @property
    def polarization_str(self):
        """Lógica para detectar el tipo de polarización basado en el vector de polarización.
        Necesario para el uso con arreglos de antenas."""
        if self._polarization_str is None:
            if np.all(np.isreal(self.pol_vector)):
                pol_type_str = 'linear'
                pol_angle = round(float(np.arctan2(self.pol_vector[1], self.pol_vector[0]) * 180 / np.pi), 2)
                self._polarization_str = f'{pol_type_str}@{pol_angle}'
                return self._polarization_str
        return self._polarization_str

    def __str__(self):
        return f'<{self.polarization_str}, Polarization vector: {self.pol_vector.round(2)}>'

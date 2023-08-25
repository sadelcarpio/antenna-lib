import numpy as np

from src.exceptions import InvalidPolarizationException


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
        # TODO: establecer lógica para implementar
        return self._polarization_str

    def __str__(self):
        return f'<{self.polarization_str}, Polarization vector: {self.pol_vector.round(2)}>'


class PolarizationFactory:
    """Clase encargada de crear objetos de tipo Polarization"""

    @classmethod
    def create_polarization(cls, polarization_str: str) -> Polarization:
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
            return np.array([np.cos(polarization_angle), np.sin(polarization_angle)])
        elif polarization.startswith('circular'):
            try:
                polarization_orientation = polarization.split('@')[1]
                if polarization_orientation not in ['lcp', 'rcp']:
                    raise InvalidPolarizationException('No valid polarization orientation. Valid parameters are '
                                                       '"rcp", "lcp"')
                return np.array([1, 1j if polarization_orientation == 'rcp' else -1j]) / np.sqrt(2)
            except IndexError:
                raise IndexError('Invalid parameter for circular polarization orientation. Format is '
                                 'circular@{orientation}')
        elif polarization.startswith('elliptical'):
            try:
                orientation = polarization.split('@')[1]
                ar = float(polarization.split('@')[2])
                tau = float(polarization.split('@')[3])
                if orientation not in ['rcp', 'lcp']:
                    raise InvalidPolarizationException('No valid Polarization orientation. Valid parameters are '
                                                       '"rcp", "lcp"')
                # calculate delta
                epsilon = np.arctan(1 / ar if orientation == 'rcp' else 1 / -ar)
                delta = np.arctan2(np.tan(2 * epsilon), np.sin(2 * tau))
                # calculate E_y / E_x
                cos_2gamma = np.cos(2 * epsilon) * np.cos(2 * tau)
                gamma = np.arccos(cos_2gamma) / 2
                ey_ex = np.tan(gamma)
                pol = np.array([1, ey_ex * np.exp(1j * delta if orientation == 'rcp' else -1j * delta)])
                return pol / np.linalg.norm(pol)
            except IndexError:
                raise IndexError('Invalid parameter for elliptical polarization. Format is '
                                 'elliptical@{orientation}@{axial_ratio}@{tau}')
            except ValueError:
                raise ValueError('Please specify a valid float number')
        else:
            raise InvalidPolarizationException("No valid polarization")

import numpy as np

from antenna_lib.exceptions import InvalidPolarizationException


class Polarization:
    def __init__(self,
                 pol_vector: np.ndarray,
                 polarization_str: str = None):
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
            # Remember pol_vector has the form: x * E_x * exp(j * phi_x) + y * E_y * exp(j * phi_y)
            y_over_x = self.pol_vector[1] / self.pol_vector[0]
            if np.isreal(y_over_x) or np.isclose(self.pol_vector[0], 0.0 + 0.0j):
                # it's linear
                y_over_x = np.real(y_over_x)  # for the case of getting 0j
                return f'linear@{np.arctan(y_over_x) * 180 / np.pi}'
            elif np.isclose(y_over_x, 1j) or np.isclose(y_over_x, -1j):
                # it's circular
                return f'circular@{"rcp" if np.isclose(y_over_x, 1j) else "lcp"}'
            else:
                # it's elliptical
                gamma = np.arctan(np.abs(y_over_x))
                delta = np.angle(y_over_x)
                epsilon = np.arcsin(np.sin(2 * gamma) * np.sin(delta)) / 2
                ar = (1 if delta > 0 else -1) / np.tan(epsilon)
                tau = np.arctan(np.tan(2 * gamma) * np.cos(delta)) / 2
                return f'elliptical@{"rcp" if delta > 0 else "lcp"}@{round(ar, 2)}@{round(tau * 180 / np.pi, 2)}'
        return self._polarization_str

    def __rmul__(self, other):
        return other * self.pol_vector

    def __repr__(self):
        return f'<{self.polarization_str}, Polarization vector: {self.pol_vector.round(2)}>'


class PolarizationFactory:
    """Clase encargada de crear objetos de tipo Polarization"""

    @classmethod
    def create_polarization(cls, polarization_str: str) -> Polarization:
        pol_vector = cls.parse_pol_vector(polarization_str)
        return Polarization(pol_vector, polarization_str)

    @classmethod
    def parse_pol_vector(cls, polarization_str: str) -> np.ndarray:
        if polarization_str.startswith('linear'):
            try:
                polarization_angle = float(polarization_str.split('@')[1]) * np.pi / 180
            except IndexError:
                raise IndexError('Invalid parameter for linear polarization angle. Format is "linear@{angle}"')
            except ValueError:
                raise ValueError('Please specify a valid float number as an angle')
            return np.array([np.cos(polarization_angle), np.sin(polarization_angle)])
        elif polarization_str.startswith('circular'):
            try:
                polarization_orientation = polarization_str.split('@')[1]
                if polarization_orientation not in ['lcp', 'rcp']:
                    raise InvalidPolarizationException('No valid polarization orientation. Valid parameters are '
                                                       '"rcp", "lcp"')
                return np.array([1, 1j if polarization_orientation == 'rcp' else -1j]) / np.sqrt(2)
            except IndexError:
                raise IndexError('Invalid parameter for circular polarization orientation. Format is '
                                 'circular@{orientation}')
        elif polarization_str.startswith('elliptical'):
            try:
                orientation = polarization_str.split('@')[1]
                ar = float(polarization_str.split('@')[2])
                tau = float(polarization_str.split('@')[3]) * np.pi / 180

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
                pol = np.array([1, ey_ex * np.exp(1j * delta)])
                return pol / np.linalg.norm(pol)
            except IndexError:
                raise IndexError('Invalid parameter for elliptical polarization. Format is '
                                 'elliptical@{orientation}@{axial_ratio}@{tau}')
            except ValueError:
                raise ValueError('Please specify a valid float number')
        else:
            raise InvalidPolarizationException("No valid polarization")

from abc import abstractmethod, ABC


class Antenna(ABC):

    polarization = None
    amplitude = None

    @property
    def max_directivity(self):
        """Calcular directividad"""
        return

    @property
    def ftb(self):
        """Calcula la relación FTB de la antena"""
        return

    @abstractmethod
    def directivity(self, theta: float, phi: float):
        """Calcula la directividad para un ángulo determinado"""

    @abstractmethod
    def plot_radiation_pattern(self, plot_type='polar', field=False):
        """Plotear el patrón de radiación, sea de campo o de potencia"""

    @abstractmethod
    def play_wave_animation(self):
        """Reproducir una animación de la onda"""

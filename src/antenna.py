from abc import abstractmethod, ABC


class Antenna(ABC):
    def __init__(self):
        pass

    @property
    def max_directivity(self):
        """Calcular directividad"""
        return

    @property
    def fdp(self):
        """Calcula la relación FTB de la antena"""
        return

    @abstractmethod
    def directivity(self, angle):
        """Calcula la directividad para un ángulo determinado"""
        pass

    @abstractmethod
    def plot_radiation_pattern(self):
        """Plotear el patrón de radiación, sea de campo o de potencia"""
        pass

    @abstractmethod
    def play_wave_animation(self):
        """Reproducir una animación de la onda"""
        pass

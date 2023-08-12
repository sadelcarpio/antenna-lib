from abc import abstractmethod, ABC


class Polarization:
    def __init__(self):
        pass


class Antenna(ABC):
    def __init__(self, polarization: Polarization = None):
        self.polarization = polarization

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


class SingleAntenna(Antenna):
    def __init__(self, pol: Polarization = None):
        super().__init__(pol)


class DipoleAntenna(SingleAntenna):
    def __init__(self, length: float, pol: Polarization = None):
        super().__init__(pol)
        self.length = length


class LoopAntenna(SingleAntenna):
    def __init__(self, radius: float, pol: Polarization = None):
        super().__init__(pol)
        self.radius = radius


class AntennaArray(Antenna):
    def __init__(self, antennas: list[Antenna] = None):
        super().__init__()
        if antennas is None:
            antennas = []
        self.antennas = antennas

    @property
    def polarization(self):
        """Calcular la polarización resultante a partir de las antenas que conforman el array"""
        return


class AntennaFactory:
    @classmethod
    def create_antenna(cls, antenna_type: str, **kwargs) -> Antenna:  # TODO: aprovechar el typing en vez de kwargs
        """Factory method"""
        match antenna_type:
            case 'dipole':
                return DipoleAntenna(**kwargs)
            case 'loop':
                return LoopAntenna(**kwargs)


if __name__ == '__main__':
    dipole_antenna = AntennaFactory.create_antenna(antenna_type='dipole', length=0.5)
    print(dipole_antenna)

from src.antenna import Antenna


class AntennaArray(Antenna):
    def __init__(self, antennas: list[Antenna] = None):  # TODO: consider geometric arrangement
        super().__init__()
        if antennas is None:
            antennas = []
        self.antennas = antennas

    @property
    def polarization(self):
        """Calcular la polarización resultante a partir de las antenas que conforman el array"""
        return

    def directivity(self, angle):
        # Implementation for this antenna type
        pass

    def plot_radiation_pattern(self):
        # Implementation for this antenna type
        pass

    def play_wave_animation(self):
        # Implementation for this antenna type
        pass
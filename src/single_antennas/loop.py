from src.single_antennas.single import SingleAntenna


class LoopAntenna(SingleAntenna):

    def __init__(self, radius: float, polarization: str = 'linear@0', amplitude: float = 1.0):
        super().__init__(polarization, amplitude)
        self.radius = radius

    def directivity(self, angle):
        # Implementation for this antenna type
        pass

    def plot_radiation_pattern(self):
        # Implementation for this antenna type
        pass

    def play_wave_animation(self):
        # Implementation for this antenna type
        pass

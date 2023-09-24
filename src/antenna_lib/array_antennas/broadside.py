from antenna_lib.array_antennas.uniform_af import UniformAntennaArray
from antenna_lib.single_antennas import SingleAntenna


class BroadSideArray(UniformAntennaArray):

    def __init__(self, antenna: SingleAntenna, n_elements: int, spacing: float = 0.5):
        super().__init__(antenna, n_elements, spacing)
        self.phase_progression = 0.0

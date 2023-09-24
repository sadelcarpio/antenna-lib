import numpy as np

from antenna_lib.array_antennas.uniform_af import UniformAntennaArray
from antenna_lib.single_antennas import SingleAntenna


class OrdinaryEndFireArray(UniformAntennaArray):

    def __init__(self, antenna: SingleAntenna, n_elements: int, spacing: float = 0.5, angle: float = 0.0):
        super().__init__(antenna, n_elements, spacing)
        self.phase_progression = - 2 * np.pi * spacing * np.cos(angle * np.pi / 180)

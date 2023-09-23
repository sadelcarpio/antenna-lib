from __future__ import annotations

from antenna_lib.array_antennas import AntennaArray
from antenna_lib.array_antennas.nonuniform_af import NonUniformAFStrategy
from antenna_lib.array_antennas.uniform_af import UniformAFStrategy
from antenna_lib.single_antennas import SingleAntenna


class AntennaArrayFactory:
    @classmethod
    def create_array(cls,
                     antenna_elem: SingleAntenna,
                     n_elements: int,
                     spacing: float,
                     phase_progression: float,
                     amplitudes: float | list[float]) -> AntennaArray:
        if isinstance(amplitudes, float):
            strategy = UniformAFStrategy(n_elements, spacing, phase_progression)
        elif isinstance(amplitudes, list):
            if len(amplitudes) != n_elements:
                raise ValueError("List of amplitudes specified is not the same length of the number of antenna "
                                 "elements.")
            strategy = NonUniformAFStrategy(amplitudes, spacing, phase_progression)
        else:
            raise TypeError("Amplitude parameter is needed. It can be `float` or `list` type")
        return AntennaArray(antenna_elem, n_elements, spacing, phase_progression, strategy)

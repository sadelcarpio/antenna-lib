from __future__ import annotations

from antenna_lib.array_antennas import AntennaArray
from antenna_lib.single_antennas import SingleAntenna


class AntennaArrayFactory:
    @classmethod
    def create_array(cls,
                     antenna_elem: SingleAntenna,
                     n_elements: int,
                     spacing: int,
                     phase_progression: float,
                     amplitudes: float | list[float]):
        if isinstance(amplitudes, float):
            antennas = [amplitudes * antenna_elem for _ in range(n_elements)]
        elif isinstance(amplitudes, list):
            if len(amplitudes) != n_elements:
                raise ValueError("List of amplitudes specified is not the same length of the number of antenna "
                                 "elements.")
            antennas = [amplitude * antenna_elem for amplitude, _ in zip(amplitudes, range(n_elements))]
        else:
            raise TypeError("Amplitude parameter is needed. It can be `float` or `list` type")
        # Here a difference can be made between:
        # 1. Same amplitude, same spacing
        # 2. Different amplitude, same spacing
        # 3. Different amplitude, different spacing
        return AntennaArray(antennas, spacing, phase_progression)

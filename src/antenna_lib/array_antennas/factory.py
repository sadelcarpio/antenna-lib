from __future__ import annotations

from antenna_lib.array_antennas import AntennaArray
from antenna_lib.array_antennas.nonuniform_af import NonUniformAFAntennaArray
from antenna_lib.array_antennas.uniform_af import UniformAFAntennaArray
from antenna_lib.single_antennas import SingleAntenna


class AntennaArrayFactory:
    @classmethod
    def create_array(cls,
                     antenna_elem: SingleAntenna,
                     spacing: float = 0.5,
                     phase_progression: float = 0.0,
                     n_elements: None | int = None,
                     amplitudes: None | list[float] = None) -> AntennaArray:
        if n_elements:
            return UniformAFAntennaArray(antenna_elem, n_elements, spacing, phase_progression)
        elif amplitudes and not n_elements:
            return NonUniformAFAntennaArray(antenna_elem, amplitudes, spacing, phase_progression)
        else:
            raise ValueError("Need to specify either `amplitudes` or `n_elements`")

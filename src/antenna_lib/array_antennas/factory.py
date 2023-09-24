from __future__ import annotations

import re

from antenna_lib.array_antennas.array import AntennaArray
from antenna_lib.array_antennas.broadside import BroadSideArray
from antenna_lib.array_antennas.hansen_woodyard import HansenWoodyardArray
from antenna_lib.array_antennas.nonuniform_af import NonUniformAntennaArray
from antenna_lib.array_antennas.ordinary_endfire import OrdinaryEndFireArray
from antenna_lib.array_antennas.uniform_af import UniformAntennaArray
from antenna_lib.single_antennas import SingleAntenna


class AntennaArrayFactory:
    @classmethod
    def create_array(cls,
                     antenna_elem: SingleAntenna,
                     spacing: float = 0.5,
                     array_type: str | None = None,
                     phase_progression: float = 0.0,
                     n_elements: None | int = None,
                     amplitudes: None | list[float] = None) -> AntennaArray:
        if amplitudes:
            return NonUniformAntennaArray(antenna_elem, amplitudes, spacing, phase_progression)
        elif n_elements and not amplitudes:
            if array_type:
                if match := re.match(r'endfire-(\d{1,3})', array_type):
                    return OrdinaryEndFireArray(antenna_elem, n_elements, spacing, float(match.group(1)))
                elif 'broadside' == array_type:
                    return BroadSideArray(antenna_elem, n_elements, spacing)
                elif match := re.match(r'hansen-woodyard-(0|180)$', array_type):
                    return HansenWoodyardArray(antenna_elem, n_elements, spacing, match.group(1))
                else:
                    raise ValueError("the array type can be `endfire-{angle}`, `broadside`,"
                                     " or `hansen-woodyard-{0-180}`")
            return UniformAntennaArray(antenna_elem, n_elements, spacing, phase_progression)
        else:
            raise ValueError("Need to specify either `amplitudes: list` or `n_elements: int`")

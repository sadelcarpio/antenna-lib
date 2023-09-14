import pytest

from antenna_lib.array_antennas.factory import AntennaArrayFactory
from antenna_lib.single_antennas import IsotropicAntenna


def test_array_factory():
    # define antenna
    antenna = IsotropicAntenna()
    antenna_array = AntennaArrayFactory.create_array(antenna_elem=antenna,
                                                     n_elements=2,
                                                     spacing=3,
                                                     phase_progression=0.0,
                                                     amplitudes=[0.5, 1.5])
    assert len(antenna_array.antennas) == 2
    assert pytest.approx(antenna_array.spacing) == 3
    assert hasattr(antenna_array, 'phase_progression')


def test_polarization_phase_progression():
    pass

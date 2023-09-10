import numpy as np
import pytest

from antenna_lib.single_antennas import SingleAntenna


class MyTestAntenna(SingleAntenna):
    """A super special antenna with a defined field pattern for testing"""
    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        if theta <= np.pi / 2:
            return np.cos(theta) ** 2
        return 0


def test_single_antenna_init():
    antenna = MyTestAntenna()
    assert antenna.polarization.polarization_str == 'linear@0.0'
    assert pytest.approx(antenna.amplitude) == 1.0


def test_single_antenna_directivity():
    antenna = MyTestAntenna()
    assert pytest.approx(antenna.max_directivity) == 10.0
    assert pytest.approx(antenna.directivity(0.0, 0.0)) == 10.0
    assert pytest.approx(antenna.directivity(np.pi / 2, 0.0)) == 0.0
    assert pytest.approx(antenna.directivity(np.pi, 0.0)) == 0.0

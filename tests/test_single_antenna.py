import numpy as np
import pytest

from antenna_lib.single_antennas import SingleAntenna


class MyTestAntenna(SingleAntenna):
    """A super special antenna with a defined field pattern for testing"""
    def field_pattern(self, theta: float, phi: float) -> float:
        return np.sin(theta) * np.cos(phi)


def test_single_antenna_init():
    antenna = MyTestAntenna(pol=0.0)
    assert antenna.polarization.polarization_str == 'linear@0.0'
    assert pytest.approx(antenna.amplitude) == 1.0


# def test_single_antenna_directivity():
#     antenna = MyTestAntenna(pol='vertical')
#     assert pytest.approx(antenna.max_directivity) == 3
#     assert pytest.approx(antenna.directivity(np.pi / 2, 0.0)) == 3.0
#     assert pytest.approx(antenna.directivity(np.pi / 4, 0.0)) == 1.5
#     antenna = MyTestAntenna(pol='horizontal')
#     assert pytest.approx(antenna.max_directivity) == 3
#     assert pytest.approx(antenna.directivity(np.pi / 2, 0.0)) == 3.0
#     assert pytest.approx(antenna.directivity(np.pi / 4, 0.0)) == 1.5

from unittest.mock import patch, MagicMock, call

import numpy as np
import pytest

from antenna_lib.exceptions import FieldPatternNotImplementedException
from antenna_lib.single_antennas import SingleAntenna


class MyTestAntenna(SingleAntenna):
    """A super special antenna with a defined field pattern for testing"""
    def field_pattern(self, theta: float, phi: float = 0.0) -> float:
        if theta <= np.pi / 2:
            return np.cos(theta) ** 2
        return 0


class MyInvalidAntenna(SingleAntenna):
    """Doesn't implement field pattern method"""
    pass


def test_single_antenna_init():
    antenna = MyTestAntenna()
    assert antenna.polarization.polarization_str == 'linear@0.0'
    assert pytest.approx(antenna.amplitude) == 1.0
    unimp_antenna = MyInvalidAntenna()
    with pytest.raises(FieldPatternNotImplementedException):
        unimp_antenna.field_pattern(0.0)


def test_single_antenna_directivity():
    antenna = MyTestAntenna()
    assert pytest.approx(antenna.max_directivity) == 10.0
    assert pytest.approx(antenna.directivity(0.0, 0.0)) == 10.0
    assert pytest.approx(antenna.directivity(np.pi / 2, 0.0)) == 0.0
    assert pytest.approx(antenna.directivity(np.pi, 0.0)) == 0.0


@patch('antenna_lib.antenna.plt')
@patch('antenna_lib.antenna.np')
def test_single_antenna_plot_radiation_pattern(mock_numpy: MagicMock, mock_pyplot: MagicMock):
    antenna = MyTestAntenna()
    antenna.plot_radiation_pattern()
    mock_pyplot.title.assert_not_called()
    mock_pyplot.subplot.assert_has_calls([call(1, 2, 1, projection='polar'), call(1, 2, 2, projection='polar')])
    mock_pyplot.subplot().set_theta_zero_location.assert_has_calls([call('N'), call('N')])
    mock_pyplot.subplot().set_theta_direction.assert_has_calls([call(-1), call(-1)])
    mock_pyplot.show.assert_called_once()
    # test with field
    antenna.plot_radiation_pattern(field=True)
    assert len(mock_numpy.sqrt.call_args_list) == 2

    # test with log_scale
    antenna.plot_radiation_pattern(log_scale=True)
    assert len(mock_numpy.log10.call_args_list) == 2
    mock_pyplot.subplot().set_rlim.assert_has_calls([call(-40), call(-40)])


@patch('antenna_lib.antenna.plt')
@patch('antenna_lib.antenna.np')
def test_single_antenna_plot_3d_pattern(mock_numpy: MagicMock, mock_pyplot: MagicMock):
    mock_numpy.meshgrid.return_value = MagicMock(), MagicMock()
    mock_pyplot.subplots.return_value = MagicMock(), MagicMock()
    antenna = MyTestAntenna()
    antenna.plot_3d_pattern()
    mock_pyplot.subplots.assert_called_with(subplot_kw={'projection': '3d'})
    mock_pyplot.subplots()[1].plot_surface.assert_called_once()
    mock_pyplot.show.assert_called_once()

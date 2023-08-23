import numpy as np
import pytest

from src.antenna_parameters.polarization import PolarizationFactory
from src.exceptions import InvalidPolarizationException


def test_polarization_factory():
    linear_pol = PolarizationFactory.create_polarization('linear@90')
    assert np.allclose(linear_pol.pol_vector, np.array([0, 1]), 1e-6)
    circular_pol = PolarizationFactory.create_polarization('circular')
    assert np.allclose(circular_pol.pol_vector, np.array([1, -1j]), 1e-6)
    ellip_pol = PolarizationFactory.create_polarization('elliptical')
    assert np.allclose(ellip_pol.pol_vector, np.array([1 + 1j, 1 - 1j]), 1e-6)
    with pytest.raises(IndexError) as error_info:
        invalid_angle = PolarizationFactory.create_polarization('linear')
    assert str(error_info.value) == 'Invalid parameter for linear polarization angle'
    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_pol = PolarizationFactory.create_polarization('poly')
    assert str(error_info.value) == 'No valid polarization'

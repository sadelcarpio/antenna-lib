import numpy as np
import pytest

from src.antenna_parameters import PolarizationFactory
from src.exceptions import InvalidPolarizationException


def test_polarization_factory():
    linear_pol = PolarizationFactory.create_polarization('linear@90')
    assert np.allclose(linear_pol.pol_vector, np.array([0, 1]), 1e-6)
    assert str(linear_pol) == '<linear@90, Polarization vector: [0. 1.]>'
    circular_pol = PolarizationFactory.create_polarization('circular@lcp')
    assert np.allclose(circular_pol.pol_vector, np.array([1, -1j]) / np.sqrt(2), 1e-6)
    assert str(circular_pol) == '<circular@lcp, Polarization vector: [ 0.71+0.j   -0.  -0.71j]>'
    # ellip_pol = PolarizationFactory.create_polarization('elliptical@lcp@45')
    # assert np.allclose(ellip_pol.pol_vector, np.array([0.70710678, 0.5 - 0.5j]), 1e-6)
    # assert str(ellip_pol) == '<elliptical@lcp@45, Polarization vector: [0.71+0.j  0.5 -0.5j]>'
    with pytest.raises(IndexError) as error_info:
        invalid_angle = PolarizationFactory.create_polarization('linear')
    assert str(error_info.value) == 'Invalid parameter for linear polarization angle. Format is "linear@{angle}"'
    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_pol = PolarizationFactory.create_polarization('poly')
    assert str(error_info.value) == 'No valid polarization'

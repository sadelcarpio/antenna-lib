import numpy as np
import pytest

from antenna_lib.antenna_parameters import PolarizationFactory
from antenna_lib.exceptions import InvalidPolarizationException


def test_polarization_factory():
    linear_pol = PolarizationFactory.create_polarization('linear@90')
    assert np.allclose(linear_pol.pol_vector, np.array([0, 1]), 1e-6)
    assert str(linear_pol) == '<linear@90, Polarization vector: [0. 1.]>'

    circular_pol = PolarizationFactory.create_polarization('circular@lcp')
    assert np.allclose(circular_pol.pol_vector, np.array([1, -1j]) / np.sqrt(2), 1e-6)
    assert str(circular_pol) == '<circular@lcp, Polarization vector: [ 0.71+0.j   -0.  -0.71j]>'

    ellip_pol = PolarizationFactory.create_polarization('elliptical@lcp@1.5@45')
    assert np.allclose(ellip_pol.pol_vector, np.array([0.64329775, 0.26725173 + 0.71745698j]), 1e-6)
    assert str(ellip_pol) == '<elliptical@lcp@1.5@45, Polarization vector: [0.64+0.j   0.27+0.72j]>'


def test_invalid_polarizations_linear():
    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_pol = PolarizationFactory.create_polarization('poly')
    assert str(error_info.value) == 'No valid polarization'

    with pytest.raises(IndexError) as error_info:
        invalid_format = PolarizationFactory.create_polarization('linear')
    assert str(error_info.value) == 'Invalid parameter for linear polarization angle. Format is "linear@{angle}"'

    with pytest.raises(ValueError) as error_info:
        invalid_angle = PolarizationFactory.create_polarization('linear@pi/2')
    assert str(error_info.value) == 'Please specify a valid float number as an angle'


def test_invalid_polarizations_circular():
    with pytest.raises(IndexError) as error_info:
        invalid_format = PolarizationFactory.create_polarization('circular')
    assert str(error_info.value) == ('Invalid parameter for circular polarization orientation. Format is '
                                     'circular@{orientation}')

    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_rotation = PolarizationFactory.create_polarization('circular@50')
    assert str(error_info.value) == 'No valid polarization orientation. Valid parameters are "rcp", "lcp"'


def test_invalid_polarizations_elliptical():
    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_rotation = PolarizationFactory.create_polarization('elliptical@lhcp@3@45')
    assert str(error_info.value) == 'No valid Polarization orientation. Valid parameters are "rcp", "lcp"'

    with pytest.raises(IndexError) as error_info:
        invalid_format = PolarizationFactory.create_polarization('elliptical@rcp@50')
    assert str(error_info.value) == ('Invalid parameter for elliptical polarization. Format is '
                                     'elliptical@{orientation}@{axial_ratio}@{tau}')

    with pytest.raises(ValueError) as error_info:
        invalid_values = PolarizationFactory.create_polarization('elliptical@rcp@p10@pi')
    assert str(error_info.value) == 'Please specify a valid float number'

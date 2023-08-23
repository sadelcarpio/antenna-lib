import pytest

from src.exceptions import InvalidPolarizationException
from src.antenna_parameters.polarization import PolarizationFactory


def test_polarization_factory():
    linear_pol = PolarizationFactory.create_polarization('linear@30')
    assert linear_pol.pol_vector == 'â<30'
    circular_pol = PolarizationFactory.create_polarization('circular')
    assert circular_pol.pol_vector == 'x +- iy'
    ellip_pol = PolarizationFactory.create_polarization('elliptical')
    assert ellip_pol.pol_vector == 'J_x x + J_y y'
    with pytest.raises(IndexError) as error_info:
        invalid_angle = PolarizationFactory.create_polarization('linear')
    assert str(error_info.value) == 'Invalid parameter for linear polarization angle'
    with pytest.raises(InvalidPolarizationException) as error_info:
        invalid_pol = PolarizationFactory.create_polarization('poly')
    assert str(error_info.value) == 'No valid polarization'

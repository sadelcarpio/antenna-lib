import numpy as np

from antenna_lib.single_antennas import DipoleAntenna
import pytest


def test_dipole_init():
    dip = DipoleAntenna(length=0.5)
    assert hasattr(dip, 'polarization')
    assert hasattr(dip, 'amplitude')
    assert pytest.approx(dip.length) == 0.5
    with pytest.raises(ValueError) as error_info:
        dip2 = DipoleAntenna(length=-0.5)
    assert str(error_info.value) == 'Dipole length must be greater than zero.'


@pytest.mark.parametrize('pol, angle', [('horizontal', 90.0), ('vertical', 0.0), ('linear', None), (45.0, 45.0)])
def test_dipole_multiple_init_pols(pol, angle):
    if pol == 'linear':
        with pytest.raises(ValueError):
            dip = DipoleAntenna(length=0.5, pol=pol)
    else:
        dip = DipoleAntenna(length=0.5, pol=pol)
        assert pytest.approx(dip.angle) == angle * np.pi / 180


def test_dipole_repr():
    dip = DipoleAntenna(length=0.5)
    assert str(dip).startswith('<DipoleAntenna with polarization:')


@pytest.mark.parametrize('dip_length, max_directivity', [(0.05, 1.5), (1.5, 2.226), (0.5, 1.641)])
def test_dipole_max_directivity(dip_length, max_directivity):
    dip = DipoleAntenna(length=dip_length)
    assert pytest.approx(dip.max_directivity, 1e-2) == max_directivity
    with pytest.raises(AttributeError):
        # noinspection PyPropertyAccess
        dip.max_directivity = 1.0


def test_dipole_field_pattern():
    shortwave_dipole = DipoleAntenna(0.01)
    for theta in np.linspace(0, np.pi, 10):
        assert pytest.approx(shortwave_dipole.field_pattern(theta), 1e-4) == np.sin(theta)
    halfwave_dipole = DipoleAntenna(0.5)
    assert pytest.approx(halfwave_dipole.field_pattern(0.0)) == 0.0
    assert pytest.approx(halfwave_dipole.field_pattern(np.pi / 2)) == 1.0

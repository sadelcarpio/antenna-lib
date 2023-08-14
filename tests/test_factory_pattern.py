import pytest

from src.antenna_factory import AntennaFactory
from src.array_antennas.array import AntennaArray
from src.single_antennas.dipole import DipoleAntenna


def test_create_antenna_method():
    dipole = AntennaFactory.create_antenna(antenna_type='dipole', length=0.5)
    assert isinstance(dipole, DipoleAntenna)
    assert dipole.length == 0.5
    assert dipole.polarization is None  # Later replace with default value


def test_create_array_antenna():
    dipoles = [AntennaFactory.create_antenna(antenna_type='loop', radius=0.5) for _ in range(3)]
    arr_antenna = AntennaFactory.create_antenna_array(dipoles)
    assert isinstance(arr_antenna, AntennaArray)
    assert len(arr_antenna.antennas) == 3
    assert hasattr(arr_antenna, 'polarization')


def test_not_valid_antenna_type():
    with pytest.raises(Exception) as error_info:
        invalid_antenna = AntennaFactory.create_antenna(antenna_type='not_valid')
    assert str(error_info.value) == 'Tipo de antena no válido.'

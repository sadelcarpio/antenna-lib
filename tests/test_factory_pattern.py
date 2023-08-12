from src.array_antennas.array import AntennaArray
from src.single_antennas.dipole import DipoleAntenna
from src.antenna_factory import AntennaFactory


def test_create_antenna_method():
    dipole = AntennaFactory.create_antenna(antenna_type='dipole', length=0.5)
    assert isinstance(dipole, DipoleAntenna)
    assert dipole.length == 0.5
    assert dipole.polarization is None  # Later replace with default value


def test_create_array_antenna():
    dipoles = [AntennaFactory.create_antenna(antenna_type='dipole', length=0.5) for _ in range(3)]
    arr_antenna = AntennaFactory.create_antenna_array(dipoles)
    assert isinstance(arr_antenna, AntennaArray)
    assert len(arr_antenna.antennas) == 3
    assert hasattr(arr_antenna, 'polarization')

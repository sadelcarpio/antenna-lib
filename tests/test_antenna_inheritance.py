from antenna_lib.antenna import Antenna
from antenna_lib.array_antennas import AntennaArray
from antenna_lib.single_antennas import DipoleAntenna, LoopAntenna, SingleAntenna


def test_create_single_antenna():
    dipole = DipoleAntenna(length=0.5)
    assert isinstance(dipole, DipoleAntenna)
    assert isinstance(dipole, SingleAntenna)
    assert isinstance(dipole, Antenna)
    assert dipole.length == 0.5
    assert dipole.polarization is None  # Later replace with default value


def test_create_array_antenna():
    dipoles = [LoopAntenna(radius=1.2) for _ in range(3)]
    arr_antenna = AntennaArray(dipoles)
    assert isinstance(arr_antenna, AntennaArray)
    assert isinstance(arr_antenna, Antenna)
    assert len(arr_antenna.antennas) == 3
    assert hasattr(arr_antenna, 'polarization')

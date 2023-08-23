from src.antenna import Antenna
from src.array_antennas import AntennaArray
from src.single_antennas import DipoleAntenna, LoopAntenna, SingleAntenna


def test_create_single_antenna():
    dipole = DipoleAntenna(length=0.5, polarization='linear@0')
    assert isinstance(dipole, DipoleAntenna)
    assert isinstance(dipole, SingleAntenna)
    assert isinstance(dipole, Antenna)
    assert dipole.length == 0.5
    assert hasattr(dipole, 'polarization')


def test_create_array_antenna():
    dipoles = [LoopAntenna(radius=1.2) for _ in range(3)]
    arr_antenna = AntennaArray(dipoles)
    assert isinstance(arr_antenna, AntennaArray)
    assert isinstance(arr_antenna, Antenna)
    assert len(arr_antenna.antennas) == 3
    assert hasattr(arr_antenna, 'polarization')
    assert arr_antenna.polarization.pol_vector == 'â<0â<0â<0'

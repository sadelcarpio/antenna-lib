import numpy as np

from antenna_lib.antenna import Antenna
from antenna_lib.array_antennas import AntennaArray
from antenna_lib.array_antennas.uniform_af import UniformAFAntennaArray
from antenna_lib.single_antennas import DipoleAntenna, LoopAntenna, SingleAntenna


def test_create_single_antenna():
    dipole = DipoleAntenna(length=0.5, pol=0.0)
    assert isinstance(dipole, DipoleAntenna)
    assert isinstance(dipole, SingleAntenna)
    assert isinstance(dipole, Antenna)
    assert dipole.length == 0.5
    assert hasattr(dipole, 'polarization')


def test_create_array_antenna():
    loop = LoopAntenna(radius=1.2)
    arr_antenna = UniformAFAntennaArray(loop, n_elements=3)
    assert isinstance(arr_antenna, AntennaArray)
    assert isinstance(arr_antenna, Antenna)
    assert arr_antenna.n_elements == 3
    assert hasattr(arr_antenna, 'polarization')
    assert np.allclose(arr_antenna.polarization.pol_vector, np.array([0, 1]), 1e-6)

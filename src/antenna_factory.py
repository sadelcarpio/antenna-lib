from src.antenna import Antenna
from src.array_antennas.array import AntennaArray
from src.single_antennas.dipole import DipoleAntenna
from src.single_antennas.loop import LoopAntenna
from src.single_antennas.single import SingleAntenna


class AntennaFactory:
    @staticmethod
    def create_antenna(antenna_type: str, **kwargs) -> SingleAntenna:  # TODO: aprovechar el typing en vez de kwargs
        """Factory method"""
        match antenna_type:
            case 'dipole':
                return DipoleAntenna(**kwargs)
            case 'loop':
                return LoopAntenna(**kwargs)

    @staticmethod
    def create_antenna_array(antennas: list[Antenna]) -> AntennaArray:
        """Factory method"""
        return AntennaArray(antennas)

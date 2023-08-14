from src.antenna import Antenna
from src.array_antennas.array import AntennaArray
from src.single_antennas.dipole import DipoleAntenna
from src.single_antennas.loop import LoopAntenna
from src.single_antennas.single import SingleAntenna


class AntennaFactory:
    @staticmethod
    def create_antenna(antenna_type: str, **kwargs) -> SingleAntenna:  # TODO: aprovechar el typing en vez de kwargs
        """Factory method"""
        if antenna_type == 'dipole':
            return DipoleAntenna(**kwargs)
        elif antenna_type == 'loop':
            return LoopAntenna(**kwargs)
        else:
            raise ValueError('Tipo de antena no válido.')

    @staticmethod
    def create_antenna_array(antennas: list[Antenna]) -> AntennaArray:
        """Factory method"""
        return AntennaArray(antennas)

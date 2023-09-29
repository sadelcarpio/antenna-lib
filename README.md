# Antenna Lib
Proyecto open source de diseño y simulación de antenas en Python.

Código de ejemplo:
```python
from antenna_lib.array_antennas import AntennaArrayFactory
from antenna_lib.single_antennas import DipoleAntenna

my_antenna_array = AntennaArrayFactory.create_array(DipoleAntenna(length=0.5), spacing=0.5,
                                                    phase_progression=-np.pi / 2,
                                                    amplitudes=[0.5, 0.5, 0.5, 1., 1., 1.])

my_antenna_array.plot_radiation_pattern(field=True)
my_antenna_array.plot_3d_pattern(field=True)
```

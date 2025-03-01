# PyWMM Package

This package provides methods to compute geomagnetic field components using the World Magnetic Model (WMM).

## Usage

For example:

```python
from wmm import WMMv2

# Get the declination at a specific latitude, longitude, year, and altitude.
declination = WMMv2.get_declination(34.0, -118.0, 2020, 0)
print("Declination:", declination)
```

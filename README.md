# PyWMM Package

A Python implementation of the World Magnetic Model (WMM) for calculating Earth's magnetic field parameters at any point on or above the Earth's surface.

## Overview

The World Magnetic Model (WMM) is the standard model used by the U.S. Department of Defense, the U.K. Ministry of Defence, NATO, and the International Hydrographic Organization for navigation, attitude, and heading referencing systems. This package provides a pure Python implementation for easy integration into geospatial applications, navigation systems, or any project requiring geomagnetic field information.

## Features

- Calculate magnetic declination (variation between true north and magnetic north)
- Calculate magnetic inclination (dip angle)
- Calculate total intensity of Earth's magnetic field
- Calculate horizontal, north, east, and vertical components of the magnetic field
- Support for custom coefficient files
- Coefficient file validation and conversion
- Support for loading coefficient data from byte streams (e.g., from HTTP requests)
- Accurate calculations at any latitude, longitude, altitude, and date within the model's valid range

## Installation

```bash
pip install pywmm
```

## Usage Examples

### Basic Usage

```python
from pywmm import WMMv2

# Initialize the model (uses default coefficient file)
wmm = WMMv2()

# Calculate magnetic declination at a location
# Parameters: latitude, longitude, decimal year, altitude (km)
declination = wmm.get_declination(34.0, -118.0, 2025.0, 0)
print(f"Magnetic declination: {declination:.2f}°")

# Calculate other magnetic field components
dip = wmm.get_dip_angle(34.0, -118.0, 2025.0, 0)
print(f"Magnetic dip angle: {dip:.2f}°")

intensity = wmm.get_intensity(34.0, -118.0, 2025.0, 0)
print(f"Total field intensity: {intensity:.1f} nT")
```

### Complete Field Components

```python
from pywmm import WMMv2
from datetime import datetime
from pywmm.utils import decimal_year

# Current location (San Francisco)
lat = 37.7749
lon = -122.4194
alt = 0  # sea level in km

# Get current decimal year
current_date = datetime.now().strftime("%Y-%m-%d")
year = decimal_year(current_date)

# Initialize the model
wmm = WMMv2()

# Calculate all field components at once (most efficient)
wmm.calculate_geomagnetic(lat, lon, year, alt)

# Now all properties are available
print(f"Declination: {wmm.dec:.2f}°")
print(f"Inclination: {wmm.dip:.2f}°")
print(f"Total Intensity: {wmm.ti:.1f} nT")
print(f"Horizontal Intensity: {wmm.bh:.1f} nT")
print(f"North Component: {wmm.bx:.1f} nT")
print(f"East Component: {wmm.by:.1f} nT")
print(f"Vertical Component: {wmm.bz:.1f} nT")
```

### Using Custom Coefficient Files

```python
from pywmm import WMMv2

# Initialize with a custom coefficient file
wmm = WMMv2(coeff_file="/path/to/custom/WMM.COF")

# Use the model as normal
declination = wmm.get_declination(34.0, -118.0, 2025.0, 0)
```

### Initializing from Byte Data

```python
from pywmm import WMMv2

# Load coefficient data from bytes (e.g., from a HTTP response)
with open("/path/to/downloaded/WMM.COF", "rb") as f:
    coef_data = f.read()

# Initialize directly from bytes
wmm = WMMv2.from_bytes(coef_data)

# Use the model as normal
declination = wmm.get_declination(34.0, -118.0, 2025.0, 0)
```

### Working with Coefficient Files

```python
from pywmm.coefficients import validate_coefficient_file, convert_to_cof_format, replace_coefficient_file

# Validate a coefficient file
is_valid, error_message = validate_coefficient_file("/path/to/coefficient_file.txt")
if is_valid:
    print("File is valid")
else:
    print(f"File is invalid: {error_message}")

# Convert a text file to proper COF format
success, result = convert_to_cof_format("/path/to/raw_data.txt", "/path/to/output.COF")
if success:
    print(f"Conversion successful: {result}")
else:
    print(f"Conversion failed: {result}")

# Replace the default coefficient file
success, message = replace_coefficient_file("/path/to/new_coefficients.COF")
if success:
    print(f"Replacement successful: {message}")
else:
    print(f"Replacement failed: {message}")
```

### Updating Coefficients at Runtime

```python
from pywmm import WMMv2

# Initialize the model with default coefficients
wmm = WMMv2()

# Later, update with new coefficient file
success = wmm.update_coefficients(new_coeff_file="/path/to/new/WMM.COF")
if success:
    print("Coefficients updated successfully")

# Or update with coefficient data from bytes
with open("/path/to/downloaded/WMM.COF", "rb") as f:
    coef_data = f.read()

success = wmm.update_coefficients(new_coeff_data=coef_data)
if success:
    print("Coefficients updated from byte data")
```

### Batch Processing with Date Range

```python
from pywmm import WMMv2
from pywmm.utils import date_range, decimal_year

# Initialize model
wmm = WMMv2()

# Location (New York City)
lat = 40.7128
lon = -74.0060

# Generate a series of dates (every 6 months for 5 years)
dates = date_range("2025-01-01", "2030-01-01", 182)
years = [decimal_year(date) for date in dates]

# Calculate declination for each date
results = []
for date, year in zip(dates, years):
    dec = wmm.get_declination(lat, lon, year, 0)
    results.append((date, dec))

# Print results
for date, dec in results:
    print(f"{date}: {dec:.2f}°")
```

## API Reference

### Main Class

#### `WMMv2(coeff_file=None, coeff_data=None)`

Initialize the World Magnetic Model.

- **Parameters**:
  - `coeff_file` (str, optional): Path to a custom coefficient file. If None, the default WMM.COF file is used.
  - `coeff_data` (bytes, optional): Coefficient data as bytes. If provided, this will be used instead of loading from a file.

#### Methods

- **`get_declination(latitude, longitude, year, altitude=0)`**: Calculate magnetic declination in degrees
- **`get_dip_angle(latitude, longitude, year, altitude=0)`**: Calculate magnetic inclination/dip angle in degrees
- **`get_intensity(latitude, longitude, year, altitude=0)`**: Calculate total magnetic field intensity in nT
- **`get_horizontal_intensity(latitude, longitude, year, altitude=0)`**: Calculate horizontal intensity in nT
- **`get_north_intensity(latitude, longitude, year, altitude=0)`**: Calculate northward component in nT
- **`get_east_intensity(latitude, longitude, year, altitude=0)`**: Calculate eastward component in nT
- **`get_vertical_intensity(latitude, longitude, year, altitude=0)`**: Calculate downward component in nT
- **`update_coefficients(new_coeff_file=None, new_coeff_data=None)`**: Update the model with new coefficient data
- **`from_bytes(byte_data)`** (class method): Create a WMMv2 instance from byte data

### Coefficient Handler Functions

#### `validate_coefficient_file(file_path)`

Validate that a file contains properly formatted WMM coefficients.

- **Parameters**:
  - `file_path` (str): Path to the coefficient file to validate
- **Returns**: tuple(is_valid, error_message)

#### `convert_to_cof_format(input_file_path, output_file_path=None)`

Convert a text file with WMM coefficient data to the proper COF format.

- **Parameters**:
  - `input_file_path` (str): Path to the input text file
  - `output_file_path` (str, optional): Path for the output COF file
- **Returns**: tuple(success, file_path or error_message)

#### `replace_coefficient_file(new_file_path, backup=True)`

Replace the default WMM coefficient file with a new one.

- **Parameters**:
  - `new_file_path` (str): Path to the new coefficient file
  - `backup` (bool): Whether to create a backup of the original file
- **Returns**: tuple(success, message)

#### `save_coefficients_from_request(request_data, output_file_path)`

Save coefficient data from a HTTP request to a file.

- **Parameters**:
  - `request_data` (bytes): Raw byte data from the request body
  - `output_file_path` (str): Path where to save the coefficient file
- **Returns**: tuple(success, message)

### Utility Functions

#### `date_range(start_date, end_date, step_days)`

Generate a list of dates between start_date and end_date with specified interval.

- **Parameters**:
  - `start_date` (str): Start date in 'YYYY-MM-DD' format
  - `end_date` (str): End date in 'YYYY-MM-DD' format
  - `step_days` (int): Interval between dates in days
- **Returns**: List of date strings in 'YYYY-MM-DD' format

#### `decimal_year(date_str)`

Convert a date string to decimal year representation.

- **Parameters**:
  - `date_str` (str): Date in 'YYYY-MM-DD' format
- **Returns**: Float representing the decimal year (e.g., 2025.5 for July 1, 2025)

## Model Validity

The WMM is typically updated every 5 years, and each model is valid for a 5-year epoch. The accuracy of the WMM decreases as time progresses from the base epoch of the model. For best results, ensure you're using the most recent coefficient file.

## Notes

- All latitudes and longitudes are in decimal degrees
- Latitudes range from -90 (South Pole) to 90 (North Pole)
- Longitudes range from -180 to 180 (negative for West, positive for East)
- Altitudes are in kilometers above the WGS-84 ellipsoid
- Decimal years can be calculated using the provided `decimal_year()` utility function
- Coefficient files must follow the standard WMM format with proper header and coefficient lines
- When working with coefficient data from external sources, always validate the format before use

## License

MIT License

Copyright (c) 2024 Douglas Rojas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

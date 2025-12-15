# PIDs (Parameter IDs)

## Overview

PIDs (Parameter IDs) are runtime diagnostic and monitoring parameters used throughout the ECU for datalogging, real-time monitoring, and inter-system communication. These parameters are calculated and updated continuously during engine operation.

## Parameter Definitions

These parameters are available for datalogging and monitoring. Values are computed in real-time and cannot be pre-defined in calibration tables.

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **RAM Air Flow Sensor Voltage 'V'** | `ubyte` | V (volts) | Direct voltage reading from Mass Airflow sensor |
| **RAM Learned Ignition Timing Correct 'V'** | `ubyte` | °, V | Learned knock correction voltage |
| **RMBR 16V Fuel Pump Control** | `ubyte` | - | Fuel pump control signal (16V system) |
| **RMBR 16V Position Left 'V'** | `ubyte` | V | Left position sensor voltage (16V) |
| **RMBR Cylinder Roughness 1** | `ubyte` | - | Cylinder 1 combustion roughness metric |
| **RMBR Cylinder Roughness 2** | `ubyte` | - | Cylinder 2 combustion roughness metric |
| **RMBR Cylinder Roughness 3** | `ubyte` | - | Cylinder 3 combustion roughness metric |
| **RMBR Cylinder Roughness 4** | `ubyte` | - | Cylinder 4 combustion roughness metric |
| **RMBS AVCS Advance Angle Left** | `ubyte` | ° | Left/intake cam advance angle |
| **RMBS AVCS Advance Angle Right 'V'** | `ubyte` | °, V | Right/exhaust cam advance angle with voltage |
| **RMBS Vehicle Speed** | `ubyte` | - | Vehicle speed from various sources |
| **RO8 Camshaft Angle Right 'V'** | `ubyte` | °, V | Right camshaft position angle/voltage |
| **RO8 Idle Switch** | `ubyte` | - | Idle throttle position switch state |
| **SAE Actual Gear Ratio** | - | - | Current transmission gear ratio (SAE standard) |
| **SAE Ambient Air Density** | - | kg/m³ | Calculated ambient air density |
| **SAE Ambient Air Temperature** | - | °F | Ambient air temperature |
| **FAO Coolant Temperature** | `ubyte` | °C | Engine coolant temperature |
| **FAO Coolant Temperature °C** | `ubyte` | °C | Engine coolant temperature (Celsius) |
| **FAO DI Temperature °C** | `ubyte` | °C | Direct injection fuel temperature |
| **FAO Gear Selection** | - | - | Current gear selection |
| **FAO Mass Air Flow** | `ubyte` | - | Mass airflow measurement |
| **FAO Mass Air Flow Ratio** | `ubyte` | - | MAF ratio/correction |
| **FAOQ Oil Temperature** | `ubyte` | °C | Engine oil temperature |
| **Engine Speed RPM** | `ubyte` | RPM | Engine crankshaft speed |
| **FAO Target Ignition Timing** | - | ° | Calculated target ignition advance |
| **FAO5 Boost Aim Manual Mode** | - | - | Manual boost control target |
| **FAO6 Short Term Fuel Trim (%)** | `ubyte` | % | Short-term fuel correction |
| **FA10 Boost Desired** | - | - | Desired boost pressure |
| **FA19 Mass Air Flow** | `ubyte` | - | Mass airflow (alternate PID) |
| **FA24 AF Sensor 1** | `ubyte` | - | Air/fuel ratio sensor 1 reading |
| **FA26 Coolant Temp °C** | `ubyte` | °C | Coolant temperature (alternate PID) |
| **FA3A WG Duty Cycle Commanded** | - | % | Wastegate duty cycle command |
| **FA40 Cruise Bench 2X** | `ubyte` | - | Cruise control bench parameter |

## Usage Notes

- All `ubyte` parameters are 8-bit unsigned integers (0-255)
- Parameters marked with voltage units may report both physical and electrical values
- RMBR/RMBS/RO8/SAE/FAO prefixes indicate different PID namespaces/protocols
- These parameters are used as inputs for calibration tables and diagnostic monitoring
- Actual runtime values depend on engine operating conditions

## Related Tables

PIDs are referenced throughout all calibration categories:
- AVCS tables use cam position PIDs
- Fuel tables use MAF, coolant temp, and AFR sensor PIDs
- Ignition tables use knock and timing PIDs
- Airflow tables use boost and MAF PIDs

## Datalogging

These parameters are the primary data points available for:
- Real-time dashboard monitoring
- Datalogs for tuning analysis
- Diagnostic trouble code (DTC) evaluation
- Closed-loop control feedback

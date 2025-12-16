# Engine

Core engine operating parameters and limits.

## Overview

Engine tables define fundamental operating characteristics:
- Rev limiters
- Speed limiters
- Load limits
- Temperature thresholds
- Operating mode transitions

## Subcategories

### Rev Limiters
Controls maximum engine speed:
- **Rev Limit - Main**: Primary RPM limiter (fuel cut)
- **Rev Limit - Hard**: Absolute maximum RPM
- **Rev Limit - Soft**: Warning/reduced power threshold

### Speed Limiters
Vehicle speed restrictions:
- **Speed Limiter**: Maximum vehicle speed
- **Speed Limiter - Valet Mode**: Restricted speed mode

### Idle Control
Manages idle speed and stability:
- **Idle Speed - Target**: Base idle RPM targets by temperature
- **Idle Speed - Warm**: Fully warmed idle target
- **Idle Speed - Cold**: Cold start elevated idle
- **Idle Speed - A/C On**: Idle with A/C compressor engaged
- **Idle Mass Airflow**: Airflow targets for idle

### Temperature Thresholds
Thermal protection parameters:
- **Coolant Warning**: High temp warning threshold
- **Oil Temperature Limits**: Oil-based protection thresholds
- **IAT Compensation**: Intake air temperature corrections

### Radiator Fan Control
Cooling system management:
- **Fan On Threshold**: Temperature to activate cooling fan
- **Fan Off Threshold**: Temperature to deactivate fan
- **Fan Speed Stages**: Multi-speed fan control

### Load Calculation
Engine load determination:
- **Load Calculation Parameters**: Load formula constants
- **VE (Volumetric Efficiency)**: Cylinder filling estimates

## Key Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Rev Limit - Main | Scalar | Primary fuel-cut rev limit (RPM) |
| Speed Limiter | Scalar | Maximum vehicle speed (km/h or mph) |
| Idle Speed - Target | 2D Map | Idle RPM by coolant temperature |
| Idle Speed - A/C Adder | Scalar | RPM increase with A/C on |
| Radiator Fan On | Scalar | Fan activation temperature (°C) |
| Radiator Fan Off | Scalar | Fan deactivation temperature (°C) |
| Coolant Temp Warning | Scalar | High temp warning threshold (°C) |

## Related Systems

- **Fuel**: Fuel cut during rev limit
- **Ignition**: Timing retard for protection
- **Throttle**: Throttle limiting
- **Airflow**: Idle airflow control

## Technical Details

### Rev Limiter Operation
The ECU limits RPM through fuel cut:
1. **Soft Limit**: Warning, possible power reduction
2. **Hard Limit**: Fuel injectors disabled
3. **Recovery**: Fuel restored when RPM drops below threshold
4. **Hysteresis**: Prevents rapid on/off cycling

### Idle Speed Control
ECU maintains target idle through:
- **Throttle Position**: Electronic throttle adjustment
- **Ignition Timing**: Timing advance/retard for speed control
- **Fuel Trim**: Maintains stoichiometric at idle
- **Load Compensation**: Adjusts for A/C, power steering, electrical loads

## Notes

- Contains critical safety limiters
- Modify with extreme caution
- Rev limiter protects valvetrain from over-rev
- Speed limiter may be legal requirement in some regions
- Idle tables critical for drivability and emissions
- Temperature thresholds protect from thermal damage

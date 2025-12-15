# Engine - Idle Speed - Idle Speed Coolant/Baro Compensation A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | RPM |
| **Source File** | `Baro Compensation A - 2018 - LF9C102P.csv` |

## Description

Provides RPM compensation to idle speed targets based on both barometric pressure (altitude) and coolant temperature. This 2D table adds or subtracts RPM from the base idle target to account for altitude effects on engine breathing and combustion.

At high altitude (low barometric pressure), reduced air density affects combustion stability, potentially requiring higher idle RPM to maintain smooth operation. This compensation table allows the ECU to automatically adjust idle speed when driving at different elevations.

The stock table shows all zero values, indicating no altitude compensation is applied to idle speed in the factory calibration. This provides a framework for tuners to add altitude-based idle adjustments if needed.

## Axes

### X-Axis

- **Parameter**: Barometric Pressure
- **Unit**: PASCAL
- **Range**: 0.0000 to 236808.6250
- **Points**: 16

### Y-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: 3.7500 to 22.5000
- **Points**: 16

## Cell Values

- **Unit**: RPM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 | 15787.2422 | 31574.4844 | 47361.7266 | 63148.9688 | 78936.2109 | 94723.4531 | 110510.6953 |
---------------------------------------------------------------------------------------------------------------------
    3.7500 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    5.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    6.2500 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    7.5000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    8.7500 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   11.2500 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   12.5000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using barometric pressure and coolant temperature:

1. **Barometric Reading**: ECU reads atmospheric pressure from barometric sensor
2. **Temperature Reading**: ECU reads coolant temperature
3. **Table Lookup**: 2D interpolation finds compensation value
4. **Application**: Compensation value added to base idle target

**Final Idle Target = Base Target (from A-J tables) + Baro/Coolant Compensation**

Stock values are all 0.0, meaning no compensation is applied. Non-zero values would add or subtract RPM from base target.

## Related Tables

- **Engine - Idle Speed - Target A-J**: Base idle targets this compensates
- **Engine - Idle Speed - Coolant/Baro Compensation B**: Second compensation table
- **Sensors - Barometric Pressure**: Source for X-axis input

## Related Datalog Parameters

- **Barometric Pressure (kPa/Pa)**: X-axis input
- **Coolant Temperature (°C)**: Y-axis input
- **Target Idle RPM**: Final commanded idle
- **Altitude (calculated)**: Derived from barometric pressure

## Tuning Notes

**Stock Behavior**: All zeros - no altitude compensation applied

**When to Add Compensation:**
- Vehicle frequently operates at high altitude (>5000 ft)
- Experiencing rough idle or stalling at elevation
- Want to improve idle stability in mountain regions

**Typical Modifications:**
- Add +25-50 RPM at low barometric pressures (high altitude)
- Greater compensation at cold temperatures where combustion is less stable
- Gradual transition across altitude range to prevent harsh changes

**Example Pattern:**
- Sea level (101 kPa): 0 RPM compensation
- 5000 ft (~85 kPa): +25 RPM
- 10000 ft (~70 kPa): +50 RPM

## Warnings

- Large compensations cause noticeable idle changes when altitude changes
- Test at various altitudes to verify appropriate compensation
- Excessive compensation at high altitude wastes fuel
- Insufficient compensation may cause stalling in thin air
- Consider fuel and ignition altitude compensations as well

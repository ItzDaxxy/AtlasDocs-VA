# AVCS - Intake - Barometric Multiplier Low - Intake Cam Target Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier Low - Intake Cam Target Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines the "aggressive" intake camshaft advance targets for LOW barometric pressure (high altitude) conditions when TGVs are open. This table represents a performance-oriented intake cam strategy for altitude operation.

The data shows consistently positive values (10-25°) indicating intake cam advance across most of the operating range. This aggressive advance strategy aims to maximize overlap with exhaust cam retard for improved scavenging and power at altitude.

The aggressive altitude table is used when the ECU selects aggressive AVCS mode while operating at higher elevations.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 2.8380
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8000.0000
- **Points**: 20

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
  800.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
 1200.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |
 1600.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2000.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2400.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2800.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 3200.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Mode Selection**: ECU determines aggressive AVCS mode is active
2. **Barometric Check**: Low barometric pressure (high altitude)
3. **TGV Check**: TGVs are OPEN
4. **Table Lookup**: 2D interpolation for intake cam target
5. **Output**: Target sent to intake AVCS solenoid

**Aggressive Altitude Strategy:**
- Performance-focused cam timing at elevation
- Consistent advance values (10-25°)
- Maximizes overlap with exhaust cam

## Related Tables

- **AVCS - Intake - Baro High - Intake Cam Target Aggressive (TGV Open)**: Sea level variant
- **AVCS - Intake - Baro Low - Intake Cam Target (TGV Open)**: Standard altitude table
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target Aggressive (TGV Open)**: Companion exhaust

## Related Datalog Parameters

- **AVCS Intake Target (°)**: Commanded position
- **AVCS Intake Actual (°)**: Measured position
- **Barometric Pressure (kPa)**: Altitude determination
- **AVCS Mode**: Aggressive mode selection
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Aggressive Strategy at Altitude:**
- Consistent 10-25° advance across range
- More aggressive than standard altitude table
- Optimized for power over emissions/economy

**Altitude Performance:**
- Different scavenging at altitude
- Turbo behavior changes in thin air
- Aggressive overlap may not suit all conditions

## Warnings

- Aggressive mode at altitude demanding on engine
- Test at actual altitude conditions
- Monitor knock activity carefully
- Coordinate with exhaust cam aggressive table
- May not be optimal for all altitude conditions

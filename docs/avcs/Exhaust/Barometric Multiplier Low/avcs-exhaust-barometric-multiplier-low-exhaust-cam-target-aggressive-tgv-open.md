# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines the "aggressive" exhaust camshaft retard targets for LOW barometric pressure (high altitude) conditions when TGVs are open. This is the altitude-compensated version of the aggressive exhaust cam target table.

At higher altitudes, the aggressive strategy is modified to account for reduced air density and different turbo behavior. The values may differ from the sea-level aggressive table to optimize performance in thin air conditions.

This table is used when the ECU selects aggressive AVCS mode while operating at higher elevations.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1935 to 2.8380
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7200.0000
- **Points**: 18

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1935 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     0.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
  800.0000 |     0.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1100.0000 |     7.5017 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    20.0027 |
 1200.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    20.0027 |
 1600.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2000.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2400.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2800.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Mode Selection**: ECU determines aggressive AVCS mode is active
2. **Barometric Check**: Low barometric pressure (high altitude)
3. **TGV Check**: TGVs are OPEN
4. **Table Lookup**: 2D interpolation for exhaust cam target
5. **Output**: Target sent to exhaust AVCS solenoid

**Altitude + Aggressive Mode:**
- Combines performance strategy with altitude compensation
- May be more or less aggressive than sea level
- Optimized for thin air turbo behavior

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target Aggressive (TGV Open)**: Sea level variant
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Open)**: Standard altitude table
- **AVCS - Intake - Baro Low - Intake Cam Target Aggressive (TGV Open)**: Companion intake

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Commanded position
- **AVCS Exhaust Actual (°)**: Measured position
- **Barometric Pressure (kPa)**: Table selection
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- Altitude-specific performance tuning
- Coordinate with other altitude tables
- Test at actual altitude conditions

**Altitude Considerations:**
- Different scavenging dynamics at altitude
- Turbo works differently in thin air
- May need different strategy than sea level

## Warnings

- Altitude tuning requires altitude testing
- Don't copy sea level values without validation
- Monitor turbo behavior at altitude
- Coordinate with intake cam altitude tables
- Test knock activity at altitude

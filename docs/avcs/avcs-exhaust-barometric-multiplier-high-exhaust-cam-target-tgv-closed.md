# AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Defines target exhaust camshaft retard angles for HIGH barometric pressure (sea level to ~3000 ft) conditions when the Tumble Generator Valves (TGV) are CLOSED. This table is used during idle, light load, cold start, and cruise conditions at normal altitudes.

When TGVs are closed, the intake runners are restricted to create tumble motion in the cylinders. This improves combustion efficiency and emissions at light loads. The exhaust cam strategy compensates with generally higher retard values to maintain adequate valve overlap.

The data shows significantly higher retard values (25-50°) compared to TGV-open tables (10-30°), reflecting the need for more overlap when intake flow is restricted.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1935 to 3.0960
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
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1100.0000 |     0.0000 |    10.0014 |    15.0007 |    11.0012 |     8.0016 |     8.0016 |     8.0016 |     8.0016 |
 1200.0000 |     0.0000 |    25.0021 |    37.0032 |    28.0016 |    19.0029 |    19.0029 |    20.0027 |    25.0021 |
 1600.0000 |     0.0000 |    34.0036 |    40.0055 |    40.0055 |    30.0041 |    27.0018 |    23.0023 |    20.0027 |
 2000.0000 |     0.0000 |    34.0036 |    51.0067 |    42.0052 |    33.0037 |    29.0043 |    24.0022 |    20.0027 |
 2400.0000 |     0.0000 |    49.0043 |    40.0055 |    41.0054 |    33.0037 |    29.0043 |    24.0022 |    20.0027 |
 2800.0000 |     0.0000 |    20.0027 |    29.0043 |    32.0038 |    35.0034 |    30.0041 |    25.0021 |    20.0027 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Barometric Check**: ECU determines barometric pressure is HIGH (normal altitude)
2. **TGV Check**: TGVs are in CLOSED position
3. **Table Lookup**: 2D interpolation for exhaust cam retard target
4. **Compensation**: Additional modifiers applied
5. **Command**: Final target sent to exhaust AVCS solenoid

**TGV Closed Strategy:**
- Higher retard values than TGV-open
- Compensates for restricted intake flow
- Optimizes internal EGR for emissions

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target (TGV Open)**: TGV open variant
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Closed)**: Altitude variant
- **AVCS - Intake - Baro High - Intake Cam Target (TGV Closed)**: Companion intake table

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Commanded position
- **AVCS Exhaust Actual (°)**: Measured position
- **Barometric Pressure (kPa)**: Table selection
- **TGV Position**: Closed state
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- TGV delete renders this table inactive
- Critical for idle stability and emissions
- Higher values than TGV-open are intentional

**TGV Closed Strategy:**
- More retard compensates for intake restriction
- Maintains adequate scavenging despite reduced flow
- Optimized for emissions and fuel economy

**Considerations:**
- This table active during emissions testing
- Idle, cruise, and cold start depend on these values
- Stock calibration optimized for emissions compliance

## Warnings

- TGV-closed cells are emissions-critical
- Changes can affect idle quality significantly
- Cold start and warm-up depend on this table
- If deleting TGVs, copy TGV-open values here
- Don't reduce retard at idle without testing stability

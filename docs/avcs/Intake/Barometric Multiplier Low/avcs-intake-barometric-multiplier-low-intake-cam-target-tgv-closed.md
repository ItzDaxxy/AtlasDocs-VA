# AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Defines target intake camshaft advance angles for LOW barometric pressure (high altitude) conditions when the Tumble Generator Valves (TGV) are CLOSED. This table controls intake cam timing during idle, light load, and cruise conditions at higher altitudes.

Intake cam advance moves the intake camshaft timing earlier relative to the crankshaft. The data shows a mix of negative values (retard from base position) and positive values (advance from base position), reflecting the complex optimization required for TGV-closed operation where tumble is being generated.

When TGVs are closed, the intake runners are restricted. The intake cam strategy must complement this - often with less aggressive advance to maintain good combustion stability with the tumbling charge motion.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 3.0960
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
  400.0000 |   -10.0014 |   -11.0012 |   -13.0010 |   -11.0012 |    -6.0019 |     0.9999 |    10.0014 |    15.0007 |
  800.0000 |   -10.0014 |   -11.0012 |   -13.0010 |   -11.0012 |    -6.0019 |     0.9999 |    10.0014 |    20.0027 |
 1200.0000 |   -13.0010 |   -13.0010 |   -16.0006 |   -11.0012 |    -0.9999 |     0.9999 |     2.9996 |    10.0014 |
 1600.0000 |   -15.0007 |   -16.0006 |   -20.0027 |   -12.0011 |    -2.9996 |     2.9996 |     0.9999 |     4.9993 |
 2000.0000 |   -15.0007 |   -15.0007 |   -20.0027 |   -10.0014 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |   -15.0007 |   -25.0021 |   -25.0021 |   -12.0011 |    -3.9995 |    -3.9995 |    -4.9993 |    -4.9993 |
 2800.0000 |   -14.0008 |   -14.0008 |   -17.0032 |   -17.0032 |   -12.0011 |   -11.0012 |   -11.0012 |   -10.0014 |
 3200.0000 |   -14.0008 |   -14.0008 |   -17.0032 |   -18.0030 |   -11.0012 |   -10.0014 |   -10.0014 |   -10.0014 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Barometric Check**: ECU determines barometric pressure is LOW (high altitude)
2. **TGV Check**: TGVs are in CLOSED position
3. **Table Lookup**: 2D interpolation for intake cam target
4. **Coordination**: Exhaust cam target also determined
5. **Command**: Target sent to intake AVCS solenoid

**TGV Closed at Altitude:**
- Idle and cruise conditions at elevation
- Tumble generation with restricted runners
- Intake cam strategy optimized for stability

## Related Tables

- **AVCS - Intake - Baro High - Intake Cam Target (TGV Closed)**: Sea level variant
- **AVCS - Intake - Baro Low - Intake Cam Target (TGV Open)**: TGV open variant
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Closed)**: Companion exhaust table

## Related Datalog Parameters

- **AVCS Intake Target (°)**: Commanded position
- **AVCS Intake Actual (°)**: Measured position
- **Barometric Pressure (kPa)**: Table selection
- **TGV Position**: Closed for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**TGV Closed Strategy:**
- Values often more conservative than TGV-open
- Negative values (retard) common at low loads
- Positive values (advance) at higher loads
- Optimized for combustion stability with tumble

**Altitude Considerations:**
- Different air density affects optimal timing
- Stock calibration already altitude-compensated
- May need adjustment for altitude-frequent drivers

## Warnings

- TGV-closed affects emissions and idle quality
- Changes impact cold start behavior
- Coordinate with exhaust cam at altitude
- Test at actual altitude conditions
- Don't assume sea level values work at altitude

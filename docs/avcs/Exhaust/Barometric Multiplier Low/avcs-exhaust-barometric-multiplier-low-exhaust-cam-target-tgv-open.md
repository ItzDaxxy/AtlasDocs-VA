# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines target exhaust camshaft retard angles for LOW barometric pressure (high altitude, ~3000+ ft) conditions when the Tumble Generator Valves (TGV) are open. This is the altitude-compensated version of the exhaust cam target table.

At higher altitudes, reduced air density affects combustion characteristics and turbo behavior. This table provides modified exhaust cam targets optimized for these conditions. The lower values compared to the high-barometric table reflect the reduced need for aggressive scavenging when air density is lower.

Exhaust cam retard delays exhaust valve closing, creating more overlap with intake valve opening. This affects scavenging, internal EGR, and turbo spool characteristics - all of which behave differently at altitude.

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
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1100.0000 |     0.0000 |     4.9993 |     9.0015 |     9.0015 |     9.0015 |     9.0015 |     8.0016 |    10.0014 |
 1200.0000 |     0.0000 |     4.9993 |    10.0014 |    12.0011 |    14.0008 |    17.0032 |    21.0026 |    25.0021 |
 1600.0000 |     0.0000 |    12.0011 |    15.0007 |    19.0029 |    23.0023 |    22.0025 |    21.0026 |    15.0007 |
 2000.0000 |     0.0000 |    12.0011 |    18.0030 |    25.0021 |    32.0038 |    24.0022 |    22.0025 |    15.0007 |
 2400.0000 |     0.0000 |    11.0012 |    12.0011 |    22.0025 |    31.0040 |    25.0021 |    22.0025 |    15.0007 |
 2800.0000 |     0.0000 |    11.0012 |    11.0012 |    20.0027 |    29.0043 |    26.0019 |    23.0023 |    15.0007 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Barometric Check**: ECU determines barometric pressure is LOW (high altitude)
2. **TGV Check**: TGVs are in OPEN position
3. **Table Lookup**: 2D interpolation for exhaust cam retard target
4. **Compensation**: Additional modifiers applied (temperature, etc.)
5. **Command**: Final target sent to exhaust AVCS solenoid

**Altitude Effects:**
- Lower air density = different scavenging dynamics
- Turbo works harder to achieve same boost
- Exhaust cam strategy adjusted accordingly

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target (TGV Open)**: Sea level equivalent
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Closed)**: TGV closed variant
- **AVCS - Intake - Baro Low - Intake Cam Target**: Companion intake table
- **AVCS - Exhaust - Retard Compensation**: Additional adjustments

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Commanded position
- **AVCS Exhaust Actual (°)**: Measured position
- **Barometric Pressure (kPa)**: Table selection
- **TGV Position**: Open/closed state
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- May need adjustment for altitude-frequent drivers
- Coordinate with intake cam altitude tables
- Less aggressive than sea level tables typically

**Altitude Considerations:**
- Lower air density changes optimal valve events
- Turbo requires different exhaust energy management
- Stock calibration already compensates for altitude

**Adjustment Guidelines:**
- Changes of 2-5 degrees incremental
- Test at actual altitude conditions if possible
- Monitor AVCS tracking and knock activity

## Warnings

- Coordinate exhaust and intake cam timing changes
- Altitude-specific tuning requires altitude testing
- Don't assume sea level values work at altitude
- Monitor turbo spool and boost response after changes
- Excessive overlap at altitude can hurt performance

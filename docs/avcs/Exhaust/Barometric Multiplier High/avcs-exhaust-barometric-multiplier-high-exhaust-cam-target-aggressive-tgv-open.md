# AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines the "aggressive" exhaust camshaft retard targets for high barometric pressure (sea level) conditions when TGVs are open. This table represents a more performance-oriented cam timing strategy compared to the standard target table.

The aggressive table may be selected during certain driving modes or conditions where the ECU determines more aggressive valve timing is appropriate. The data shows relatively conservative values (mostly 10-15°), suggesting this table may blend with or modify the base target rather than replace it entirely.

Exhaust cam retard controls valve overlap timing - more retard creates more overlap with intake valves, affecting scavenging, turbo spool, and internal EGR.

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
 1100.0000 |     7.5017 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1200.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1600.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2000.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2400.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2800.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
```

## Functional Behavior

The ECU performs 2D interpolation based on RPM and calculated load:

1. **Mode Selection**: ECU determines aggressive AVCS mode is active
2. **Barometric Check**: High barometric pressure confirmed
3. **TGV Check**: TGVs are OPEN
4. **Table Lookup**: 2D interpolation for exhaust cam target
5. **Output**: Target sent to exhaust AVCS solenoid

**Aggressive Mode Characteristics:**
- May activate during sport mode or aggressive throttle
- Potentially optimized for performance over emissions
- Coordinates with aggressive intake cam table

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target (TGV Open)**: Standard target table
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target Aggressive (TGV Open)**: Altitude variant
- **AVCS - Intake - Baro High - Intake Cam Target Aggressive (TGV Open)**: Companion intake table
- **AVCS - Exhaust - Retard Compensation**: Additional modifiers

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Commanded position
- **AVCS Exhaust Actual (°)**: Measured position
- **AVCS Mode**: Standard vs aggressive selection
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- May increase retard for improved turbo spool
- Coordinate with intake cam aggressive table
- Test impact on emissions and driveability

**Aggressive Strategy:**
- Performance-focused valve timing
- May sacrifice some emissions for power
- Typically more overlap than standard table

**Considerations:**
- Stock values appear relatively conservative
- May be room for more aggressive timing
- Always test knock activity after changes

## Warnings

- Aggressive cam timing can increase knock risk
- Coordinate exhaust and intake cam changes
- Monitor emissions if vehicle is tested
- Test across full RPM/load range
- Don't assume more retard is always better

# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Provides compensation adders for the aggressive exhaust cam retard strategy at LOW barometric pressure (high altitude) when TGVs are open. This table modifies the aggressive exhaust cam target at altitude.

The data shows all zeros, indicating no additional compensation is applied to the aggressive exhaust cam strategy at altitude. The aggressive target altitude table values are used directly.

Unlike the standard TGV-open altitude compensation which has active negative values, the aggressive strategy does not receive additional altitude adjustment beyond the base aggressive altitude table.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Calculated Load
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
 1100.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU uses this as a compensation adder (currently inactive):

1. **Mode Check**: Aggressive AVCS mode active
2. **Barometric Check**: Low barometric pressure (altitude)
3. **Base Target**: ECU gets aggressive altitude exhaust cam target
4. **Compensation**: This table provides offset (all zeros)
5. **Result**: Aggressive altitude target used without modification

**Stock Calibration:**
- All values are 0.0
- Aggressive altitude table used directly
- No layered altitude compensation for aggressive mode

## Related Tables

- **AVCS - Exhaust - Baro Low - Exhaust Cam Target Aggressive (TGV Open)**: Base target
- **AVCS - Exhaust - Baro High - Compensation Aggressive (TGV Open)**: Sea level variant
- **AVCS - Exhaust - Baro Low - Compensation (TGV Open)**: Standard has active values

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final commanded position
- **Barometric Pressure (kPa)**: Altitude determination
- **AVCS Mode**: Aggressive mode selection
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Comparison to Standard:**
- Standard TGV-open altitude compensation is active (negative values)
- Aggressive mode altitude compensation is inactive (zeros)
- Different optimization strategy for each mode

**Altitude + Aggressive:**
- Aggressive altitude base table handles all adjustment
- No layered compensation in stock calibration
- Available for custom performance tuning

## Warnings

- Aggressive mode at altitude is demanding on engine
- Test thoroughly at actual altitude
- Monitor knock activity carefully
- Coordinate with intake cam aggressive altitude tables
- Don't assume sea level aggressive values work at altitude

# AVCS - Exhaust -  Barometric Multiplier High - Exhaust Cam Retard Compensation Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust -  Barometric Multiplier High - Exhaust Cam Retard Compensation Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Provides compensation adders for the aggressive exhaust cam retard strategy at HIGH barometric pressure (sea level) when TGVs are open. This table modifies the aggressive exhaust cam target under specific conditions.

The data shows all zeros, indicating no additional compensation is applied to the aggressive exhaust cam strategy at sea level. The aggressive target table values are used directly without modification.

This table exists for tuning flexibility - compensation could be added for specific performance or condition-based adjustments to the aggressive cam strategy.

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
2. **Base Target**: ECU gets aggressive exhaust cam target
3. **Compensation**: This table provides offset (all zeros)
4. **Result**: Aggressive target used without modification

**Stock Calibration:**
- All values are 0.0
- Aggressive target table used directly
- Available for custom tuning

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target Aggressive (TGV Open)**: Base target
- **AVCS - Exhaust - Baro Low - Compensation Aggressive (TGV Open)**: Altitude variant
- **AVCS - Exhaust - Baro High - Compensation (TGV Open)**: Standard compensation

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final commanded position
- **AVCS Mode**: Aggressive mode selection
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Stock Values:**
- All zeros - aggressive targets used directly
- Available for performance tuning
- Could add condition-specific aggressive adjustments

**Potential Uses:**
- Temperature-based aggressive compensation
- Load-specific aggressive modifications
- Fine-tuning without changing aggressive base table

## Warnings

- Aggressive cam timing already more demanding
- Additional compensation increases complexity
- Test thoroughly after any changes
- Monitor knock and driveability
- Coordinate with intake cam aggressive tables

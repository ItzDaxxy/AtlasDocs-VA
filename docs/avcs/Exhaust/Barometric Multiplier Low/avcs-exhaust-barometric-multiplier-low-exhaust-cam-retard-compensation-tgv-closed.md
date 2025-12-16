# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Provides altitude-specific compensation for exhaust cam retard at LOW barometric pressure (high altitude) when TGVs are CLOSED. This table is used during idle, light load, and cruise conditions at high altitude.

The data shows all zeros, indicating no additional altitude compensation is applied for TGV-closed exhaust cam timing. The base altitude target table handles all necessary adjustments for these operating conditions.

Unlike the TGV-open compensation table which has active negative values, TGV-closed operation uses only base target values at altitude.

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
 1100.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU uses this as a compensation adder (currently inactive):

1. **Base Target**: ECU gets exhaust cam target from TGV-closed altitude table
2. **Compensation Lookup**: This table provides offset (all zeros)
3. **Result**: Base target used without modification

**Stock Calibration:**
- All values are 0.0 - no compensation applied
- TGV-closed altitude base table is sufficient
- Available for aftermarket tuning

**Contrast with TGV-Open:**
- TGV-open altitude compensation has active negative values
- TGV-closed does not require additional compensation
- Different optimization strategy for each TGV state

## Related Tables

- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Closed)**: Base target
- **AVCS - Exhaust - Baro Low - Compensation (TGV Open)**: Active altitude compensation
- **AVCS - Exhaust - Baro High - Compensation (TGV Closed)**: Sea level variant

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final target (same as base)
- **TGV Position**: Closed for this table
- **Barometric Pressure (kPa)**: Low/altitude condition
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Stock Values:**
- All zeros - no additional compensation
- TGV-closed base table handles altitude needs
- Available for custom tuning if needed

**TGV-Closed at Altitude:**
- Idle and cruise at altitude
- Base table already optimized
- Compensation available for fine-tuning

## Warnings

- Changes affect altitude TGV-closed operation
- Idle quality at altitude sensitive
- Test at actual altitude conditions
- Coordinate with other altitude tables

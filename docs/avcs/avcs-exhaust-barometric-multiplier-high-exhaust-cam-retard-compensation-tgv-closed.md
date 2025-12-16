# AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Provides additional compensation adders for exhaust cam retard targets at high barometric pressure (sea level) when TGVs are CLOSED. This table adds to the base exhaust cam target under specific conditions.

The data shows all zeros, indicating this compensation table is not actively used in the stock calibration. The base target tables for TGV-closed operation are used without additional compensation.

This table exists for tuning flexibility and allows modification of cam timing behavior during TGV-closed conditions (idle, light load, cruise) without altering the primary target tables.

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

The ECU uses this table as an adder to the base target:

1. **Base Target**: ECU looks up exhaust cam target from TGV-closed main table
2. **Compensation Lookup**: This table provides additional offset
3. **Final Target**: Base Target + Compensation = Commanded Position

**Stock Calibration:**
- All values are 0.0 - no compensation applied
- TGV-closed base target used directly
- Available for custom tuning

**TGV Closed Operation:**
- Active during idle, light load, cruise
- Higher base retard than TGV-open
- Compensation could fine-tune these conditions

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target (TGV Closed)**: Base target this modifies
- **AVCS - Exhaust - Compensation (TGV Open)**: TGV open variant
- **AVCS - Exhaust - Retard Target Adder Activation**: Temperature activation

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final commanded position
- **TGV Position**: Closed state for this table
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- Fine-tune idle cam timing
- Adjust cruise behavior
- Temperature-based cam adjustments

**Stock Values:**
- All zeros - stock calibration doesn't use compensation
- TGV-closed base tables sufficient for OEM
- Available for aftermarket use

**TGV-Closed Considerations:**
- Affects emissions-critical operating areas
- Idle quality sensitive to cam timing
- Cold start depends on these conditions

## Warnings

- TGV-closed areas are emissions-sensitive
- Changes affect idle stability
- Cold start and warm-up impacted
- Keep compensation values modest
- Test driveability after any changes

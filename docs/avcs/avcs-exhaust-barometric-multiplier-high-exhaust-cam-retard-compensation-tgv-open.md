# AVCS - Exhaust -  Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust -  Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Provides additional compensation adders for exhaust cam retard targets at high barometric pressure (sea level) when TGVs are open. This table adds to the base exhaust cam target under specific conditions.

The data shows all zeros, indicating this compensation table is not actively used in the stock calibration - the base target tables are used without additional compensation. This table exists for tuning flexibility and may be populated for specific applications.

Compensation tables allow fine-tuning of cam timing based on additional parameters without modifying the primary target tables.

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
 1100.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU uses this table as an adder to the base target:

1. **Base Target**: ECU looks up exhaust cam target from main table
2. **Compensation Lookup**: This table provides additional offset
3. **Final Target**: Base Target + Compensation = Commanded Position

**Stock Calibration:**
- All values are 0.0 - no compensation applied
- Base target table used directly
- Available for custom tuning

**Formula:**
```
Final_Exhaust_Target = Base_Target + Compensation
```

## Related Tables

- **AVCS - Exhaust - Baro High - Exhaust Cam Target (TGV Open)**: Base target this modifies
- **AVCS - Exhaust - Retard Target Adder Activation**: Temperature-based activation
- **AVCS - Exhaust - Compensation (TGV Closed)**: TGV closed variant

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final commanded position
- **AVCS Exhaust Actual (°)**: Measured position
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- Add compensation for specific operating conditions
- Can adjust timing without modifying main tables
- Useful for conditional cam timing changes

**Stock Values:**
- All zeros - no compensation in stock calibration
- Indicates base tables are sufficient for OEM requirements
- Available for aftermarket tuning use

**Potential Uses:**
- Temperature-based cam timing adjustment
- Condition-specific overlap modification
- Fine-tuning without changing base tables

## Warnings

- Compensation adds to base target - watch total values
- Ensure final target stays within AVCS mechanical limits
- Test across operating range after adding compensation
- Monitor AVCS tracking error after changes

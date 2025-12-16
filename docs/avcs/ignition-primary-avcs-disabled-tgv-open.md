# Ignition - Primary - AVCS Disabled - TGV Open

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Primary - AVCS Disabled - TGV Open - 2017 - RogueWRX.csv` |

## Description

Defines primary ignition timing in degrees BTDC for conditions when AVCS is DISABLED AND TGVs are OPEN. This combination typically occurs during warm-up if TGVs open before AVCS activates, or during AVCS system faults at higher loads where TGVs open for airflow.

Values range from 34° advance at light load/mid RPM to -8° (retarded after TDC) at high load/low RPM conditions. The table shows slightly more aggressive timing than the AVCS-disabled TGV-closed variant because open TGVs indicate higher airflow demands where timing can be optimized.

AVCS-disabled with TGV-open is a fallback condition where cam timing is fixed but intake restriction is removed for higher airflow needs. This represents a transitional state during warm-up or a fault recovery mode.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.8360
- **Points**: 16

### Y-Axis

- **Parameter**: Boost Control - RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8400.0000
- **Points**: 22

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    15.0000 |    20.0000 |    18.0000 |    10.0000 |     7.5000 |    -1.0000 |    -4.0000 |    -8.0000 |
  800.0000 |    15.0000 |    20.0000 |    18.5000 |    10.0000 |     7.5000 |    -1.0000 |    -1.5000 |    -3.0000 |
 1200.0000 |    20.0000 |    22.0000 |    17.0000 |    16.0000 |    11.0000 |     6.0000 |     1.0000 |    -2.0000 |
 1600.0000 |    25.0000 |    22.0000 |    18.0000 |    18.0000 |    15.0000 |    10.5000 |     5.5000 |     2.0000 |
 2000.0000 |    27.0000 |    27.0000 |    25.0000 |    23.0000 |    22.5000 |    17.5000 |    14.0000 |     8.0000 |
 2400.0000 |    29.0000 |    29.0000 |    27.0000 |    24.0000 |    23.0000 |    19.5000 |    13.5000 |     9.5000 |
 2800.0000 |    29.0000 |    28.5000 |    25.0000 |    23.0000 |    22.0000 |    19.5000 |    14.5000 |    13.5000 |
 3200.0000 |    34.0000 |    30.0000 |    26.0000 |    24.0000 |    22.5000 |    21.0000 |    16.5000 |    13.5000 |
```

## Functional Behavior

The ECU performs 2D interpolation based on calculated load and RPM:

1. **AVCS Check**: AVCS system is DISABLED
2. **TGV Check**: TGVs are in OPEN position
3. **Table Selection**: Use this AVCS-disabled TGV-open timing map
4. **Base Lookup**: 2D interpolation for base timing
5. **Corrections Applied**: IAT, knock, DAM, octane adjustments
6. **Final Timing**: Command sent to ignition system

**AVCS Disabled + TGV Open:**
- May occur during warm-up transition
- AVCS fault with high load demand
- Cams fixed, but TGVs opened for airflow
- Higher load operation without AVCS optimization

## Related Tables

- **Ignition - Primary - AVCS Enabled - TGV Open**: AVCS enabled variant
- **Ignition - Primary - AVCS Disabled - TGV Closed**: TGV closed variant
- **Fuel - Open Loop - AVCS Disabled - Target Base (TGV Open)**: Companion fuel table
- **Ignition - Primary - Knock Correction**: Knock-based timing reduction

## Related Datalog Parameters

- **Ignition Timing**: Final timing output
- **Feedback Knock Correction**: Immediate knock response
- **Fine Knock Learn**: Learned knock correction
- **AVCS Status**: Disabled for this table
- **TGV Position**: Open for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Fallback Operation:**
- Used when AVCS cannot actuate
- Fixed cam timing limits optimization
- TGVs open for maximum airflow
- Timing calibrated for non-optimal cam position

**Diagnostic Considerations:**
- Frequent use indicates AVCS issue
- Check oil pressure and AVCS solenoids
- AVCS fault codes should be investigated
- May indicate persistent system problems

## Warnings

- Prolonged AVCS-disabled operation is suboptimal
- Power and efficiency reduced without AVCS
- Check for AVCS fault codes if persistent
- Cold weather extends AVCS-disabled operation
- AVCS solenoid or wiring faults require repair
- Monitor knock activity in this fallback mode

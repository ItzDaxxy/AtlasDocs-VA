# Ignition - Primary - AVCS Enabled - TGV Closed

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Primary - AVCS Enabled - TGV Closed - 2017 - RogueWRX.csv` |

## Description

Defines primary ignition timing in degrees BTDC for conditions when AVCS is ENABLED AND TGVs are CLOSED. This is one of four primary timing tables selected based on AVCS and TGV state, used during idle, light load, cold start, and cruise conditions where TGVs restrict intake flow to create tumble.

Values range from 34° advance at light load/low RPM to -9° (retarded after TDC) at high load/low RPM conditions. The table shows aggressive timing at low loads with significant reduction as load increases to prevent knock.

TGV-closed operation with AVCS enabled represents normal idle and light-load operation where tumble promotes efficient combustion, allowing more timing advance. AVCS optimizes cam timing while TGVs enhance mixture motion.

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
  400.0000 |    15.0000 |    20.0000 |    19.0000 |    11.0000 |     5.0000 |     0.0000 |    -4.0000 |    -9.0000 |
  800.0000 |    15.0000 |    20.0000 |    18.0000 |    15.0000 |     9.0000 |     3.0000 |    -3.0000 |    -8.0000 |
 1200.0000 |    20.0000 |    28.0000 |    22.0000 |    12.5000 |     8.5000 |     5.0000 |     0.0000 |    -4.0000 |
 1600.0000 |    28.0000 |    28.0000 |    22.5000 |    15.0000 |    10.0000 |     9.5000 |     5.0000 |     1.0000 |
 2000.0000 |    28.0000 |    28.0000 |    27.0000 |    21.0000 |    13.0000 |    10.5000 |     9.0000 |     4.0000 |
 2400.0000 |    31.0000 |    31.0000 |    27.0000 |    22.0000 |    17.0000 |    12.5000 |    10.0000 |     6.0000 |
 2800.0000 |    31.0000 |    27.0000 |    20.0000 |    18.5000 |    16.5000 |    13.0000 |    10.0000 |     6.0000 |
 3200.0000 |    26.5000 |    25.0000 |    19.5000 |    16.0000 |    15.0000 |    13.0000 |    12.0000 |     8.5000 |
```

## Functional Behavior

The ECU performs 2D interpolation based on calculated load and RPM:

1. **State Check**: AVCS enabled AND TGVs closed
2. **Table Selection**: Use this AVCS-enabled TGV-closed timing map
3. **Base Lookup**: 2D interpolation for base timing
4. **Corrections Applied**: IAT, knock, DAM, octane adjustments
5. **Final Timing**: Command sent to ignition system

**AVCS Enabled + TGV Closed Timing:**
- Normal idle and light-load operation
- Tumble enhances combustion efficiency
- AVCS optimizes overlap for conditions
- More timing possible due to better combustion

## Related Tables

- **Ignition - Primary - AVCS Enabled - TGV Open**: TGV open variant
- **Ignition - Primary - AVCS Disabled - TGV Closed**: AVCS disabled variant
- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed)**: Companion fuel table
- **Ignition - Primary - Knock Correction**: Knock-based timing reduction

## Related Datalog Parameters

- **Ignition Timing**: Final timing output
- **Feedback Knock Correction**: Immediate knock response
- **Fine Knock Learn**: Learned knock correction
- **AVCS Status**: Enabled for this table
- **TGV Position**: Closed for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**TGV Closed Strategy:**
- Light load benefits from tumble combustion
- Timing can be more aggressive than TGV-open
- Critical for idle quality and emissions
- AVCS overlap optimized for these conditions

**Idle/Cruise Operation:**
- Low-load cells affect daily drivability
- Timing affects fuel economy at cruise
- Changes here impact emissions testing
- Conservative approach recommended

## Warnings

- TGV-closed timing affects idle and emissions
- Changes impact cold start behavior
- Verify no knock at all TGV-closed conditions
- TGV delete requires timing reconsideration
- Monitor knock at light-load conditions
- Excessive timing causes rough idle

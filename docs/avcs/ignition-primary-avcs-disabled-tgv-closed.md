# Ignition - Primary - AVCS Disabled - TGV Closed

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Primary - AVCS Disabled - TGV Closed - 2017 - RogueWRX.csv` |

## Description

Defines primary ignition timing in degrees BTDC for conditions when AVCS is DISABLED AND TGVs are CLOSED. This table is used during cold start warm-up before AVCS activates, or when AVCS system faults are present, while operating at idle or light load where TGVs remain closed.

Values range from 26° advance at light load/low RPM to -8° (retarded after TDC) at high load/low RPM conditions. The table generally shows more conservative timing than the AVCS-enabled variant because fixed cam timing (0° position) provides less optimal combustion characteristics.

AVCS-disabled conditions typically occur during cold start before oil pressure is sufficient to actuate the AVCS solenoids. Without AVCS optimization, slightly reduced timing provides engine protection during this transitional period.

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
  400.0000 |    15.0000 |    19.0000 |    15.0000 |    11.0000 |     7.0000 |     0.0000 |    -4.0000 |    -8.0000 |
  800.0000 |    15.0000 |    19.0000 |    15.5000 |    12.0000 |     8.0000 |     0.0000 |    -1.0000 |    -5.0000 |
 1200.0000 |    20.0000 |    20.0000 |    16.0000 |    13.0000 |     9.5000 |     5.0000 |     0.0000 |    -4.0000 |
 1600.0000 |    22.0000 |    22.0000 |    18.0000 |    15.5000 |    12.0000 |     6.5000 |     3.0000 |    -2.0000 |
 2000.0000 |    23.0000 |    22.5000 |    19.0000 |    17.0000 |    13.5000 |     8.0000 |     6.0000 |     1.0000 |
 2400.0000 |    24.0000 |    22.5000 |    19.5000 |    17.5000 |    14.0000 |    11.0000 |     7.0000 |     4.0000 |
 2800.0000 |    25.0000 |    23.0000 |    20.0000 |    20.0000 |    17.0000 |    12.0000 |     8.0000 |     6.0000 |
 3200.0000 |    26.0000 |    24.0000 |    20.0000 |    19.5000 |    17.5000 |    14.0000 |     9.0000 |     4.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation based on calculated load and RPM:

1. **AVCS Check**: AVCS system is DISABLED (cold start or fault)
2. **TGV Check**: TGVs are in CLOSED position
3. **Table Selection**: Use this AVCS-disabled TGV-closed timing map
4. **Base Lookup**: 2D interpolation for base timing
5. **Corrections Applied**: IAT, knock, DAM, octane adjustments
6. **Final Timing**: Command sent to ignition system

**AVCS Disabled Conditions:**
- Cold start (insufficient oil pressure)
- AVCS system fault codes present
- Warm-up period before AVCS activation
- Cams at default (0°) position

## Related Tables

- **Ignition - Primary - AVCS Enabled - TGV Closed**: AVCS enabled variant
- **Ignition - Primary - AVCS Disabled - TGV Open**: TGV open variant
- **Fuel - Open Loop - AVCS Disabled - Target Base (TGV Closed)**: Companion fuel table
- **Ignition - Primary - Knock Correction**: Knock-based timing reduction

## Related Datalog Parameters

- **Ignition Timing**: Final timing output
- **Feedback Knock Correction**: Immediate knock response
- **Fine Knock Learn**: Learned knock correction
- **AVCS Status**: Disabled for this table
- **TGV Position**: Closed for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**AVCS Disabled Strategy:**
- Used during cold start warm-up
- Cams at default position (no advance/retard)
- Timing compensates for fixed cam timing
- More conservative than AVCS-enabled tables

**Cold Start Considerations:**
- AVCS typically enables after ~30-60 seconds
- Oil pressure required for AVCS actuation
- Timing must work without cam timing benefits
- Cold engine more knock-resistant

## Warnings

- Affects cold start timing behavior
- AVCS disabled limits engine optimization
- Check AVCS status if table always active
- AVCS fault codes require diagnosis
- Cold weather extends AVCS-disabled period
- Monitor for persistent AVCS disable conditions

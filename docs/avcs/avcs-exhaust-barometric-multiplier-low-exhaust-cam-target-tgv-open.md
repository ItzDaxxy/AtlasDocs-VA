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

*Add description of what this table controls and when it's used.*

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

*Add description of how the ECU interpolates and uses this table.*

## Related Tables

- TBD

## Related Datalog Parameters

- TBD

## Tuning Notes

*Add practical tuning guidance and typical modification patterns.*

## Warnings

*Add safety considerations and potential risks.*

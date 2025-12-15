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

*Add description of what this table controls and when it's used.*

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

*Add description of how the ECU interpolates and uses this table.*

## Related Tables

- TBD

## Related Datalog Parameters

- TBD

## Tuning Notes

*Add practical tuning guidance and typical modification patterns.*

## Warnings

*Add safety considerations and potential risks.*

# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

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
 1100.0000 |     0.0000 |    10.0014 |    15.0007 |    11.0012 |     8.0016 |     8.0016 |     8.0016 |     8.0016 |
 1200.0000 |     0.0000 |    25.0021 |    37.0032 |    28.0016 |    19.0029 |    19.0029 |    20.0027 |    25.0021 |
 1600.0000 |     0.0000 |    34.0036 |    40.0055 |    40.0055 |    30.0041 |    27.0018 |    23.0023 |    20.0027 |
 2000.0000 |     0.0000 |    34.0036 |    51.0067 |    42.0052 |    33.0037 |    29.0043 |    24.0022 |    20.0027 |
 2400.0000 |     0.0000 |    49.0043 |    40.0055 |    41.0054 |    33.0037 |    29.0043 |    24.0022 |    20.0027 |
 2800.0000 |     0.0000 |    20.0027 |    29.0043 |    32.0038 |    35.0034 |    30.0041 |    25.0021 |    20.0027 |
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

# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Open) - 2018 - LF9C102P.csv` |

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
 1100.0000 |     0.0000 |   -10.0014 |   -15.0007 |   -13.0010 |    -8.0016 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |   -25.0021 |   -37.0032 |   -33.0037 |   -19.0029 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |   -34.0036 |   -40.0055 |   -40.0055 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |   -34.0036 |   -51.0067 |   -42.0052 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |   -34.0036 |   -28.0016 |   -29.0043 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
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

# Airflow - MAF - MAF Volumetric Efficiency Correction B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - MAF - MAF Volumetric Efficiency Correction B - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: Airflow - Turbo - Manifold Absolute Pressure
- **Unit**: PSI
- **Range**: 3.0216 to 34.7487
- **Points**: 16

### Y-Axis

- **Parameter**: Engine - RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7600.0000
- **Points**: 22

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     3.0216 |     4.5324 |     5.2878 |     6.0433 |     7.5541 |     9.0649 |    12.0865 |    15.1081 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    54.2755 |    63.0310 |    65.5304 |    67.7734 |    70.0317 |    71.4630 |    73.0316 |    73.9014 |
  800.0000 |    54.2755 |    63.0310 |    65.5304 |    67.7734 |    70.0317 |    71.4630 |    73.0316 |    73.9014 |
 1200.0000 |    57.5592 |    65.8539 |    68.2251 |    70.4132 |    72.4915 |    74.6277 |    75.3357 |    74.8840 |
 1600.0000 |    64.8987 |    70.6970 |    76.7242 |    78.0792 |    81.9550 |    82.3212 |    83.1146 |    84.6924 |
 2000.0000 |    64.5996 |    69.5679 |    72.2260 |    74.7345 |    77.3285 |    79.3671 |    81.1310 |    84.1888 |
 2400.0000 |    64.5996 |    73.3978 |    75.6409 |    78.5797 |    81.9733 |    84.5581 |    86.0504 |    87.4969 |
 2800.0000 |    59.9976 |    66.6992 |    69.7327 |    73.2483 |    77.5757 |    80.4596 |    82.3395 |    83.4473 |
 3200.0000 |    62.0972 |    66.6992 |    69.3512 |    70.1721 |    76.5045 |    78.0487 |    82.2052 |    83.6060 |
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

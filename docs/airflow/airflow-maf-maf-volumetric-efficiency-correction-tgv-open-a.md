# Airflow - MAF - MAF Volumetric Efficiency Correction (TGV Open) A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - MAF - MAF Volumetric Efficiency Correction (TGV Open) A - 2018 - LF9C102P.csv` |

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
  400.0000 |    93.0084 |    73.4100 |    76.9745 |    85.5255 |    94.0796 |   106.9061 |    96.2158 |   100.4944 |
  800.0000 |    66.2506 |    65.1428 |    64.8254 |    64.5874 |    64.2548 |    64.0198 |    66.3452 |    75.1404 |
 1200.0000 |    62.8357 |    65.4968 |    66.2567 |    66.8274 |    67.6239 |    66.1804 |    72.1222 |    87.4817 |
 1600.0000 |    66.5741 |    69.8761 |    70.8191 |    71.5271 |    72.3816 |    72.7081 |    73.8922 |    82.8583 |
 2000.0000 |    70.1263 |    69.9463 |    69.8914 |    69.8547 |    70.1538 |    71.3745 |    74.3683 |    81.3538 |
 2400.0000 |    74.8688 |    74.9786 |    75.0122 |    75.0366 |    75.7721 |    76.6235 |    77.6123 |    81.8512 |
 2800.0000 |    68.8293 |    71.2494 |    71.9391 |    72.4579 |    73.0804 |    73.3307 |    72.8912 |    79.5349 |
 3200.0000 |    68.6188 |    70.6055 |    71.1731 |    71.6003 |    72.4854 |    73.4528 |    74.0021 |    80.4047 |
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

# Airflow - Turbo - Wastegate - Wastegate Duty Initial

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 17x14 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate Duty Initial - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: REQ TORQUE
- **Unit**: NM
- **Range**: 200.0000 to 400.0000
- **Points**: 14

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 2000.0000 to 8000.0000
- **Points**: 17

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   200.0000 |   220.0000 |   240.0000 |   260.0000 |   280.0000 |   300.0000 |   320.0000 |   340.0000 |
--------------------------------------------------------------------------------------------------------------------
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    15.0000 |    25.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    21.0000 |    34.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     7.0000 |    19.0000 |    31.0000 |
 3200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    10.0000 |    24.0000 |    34.0000 |
 3600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     7.0000 |    23.0000 |    39.0000 |
 4000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     8.0000 |    22.0000 |    35.0000 |
 4400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     8.0000 |    24.0000 |    32.0000 |
 4800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    11.0000 |    28.0000 |    42.0000 |    46.0000 |
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

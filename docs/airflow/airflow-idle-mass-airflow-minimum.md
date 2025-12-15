# Airflow - Idle - Mass Airflow Minimum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | G_PER_SEC |
| **Source File** | `Airflow - Idle - Mass Airflow Minimum - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: Idle Control - Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Idle Control - RPM
- **Unit**: NONE
- **Range**: 0.0000 to 7800.0000
- **Points**: 21

## Cell Values

- **Unit**: G_PER_SEC
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |
  400.0000 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |
  800.0000 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |
 1200.0000 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |
 1600.0000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |
 2000.0000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |
 2400.0000 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |
 2800.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |
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

# Airflow - Turbo - Boost - Compensation - Boost Barometric Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x8 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Boost - Compensation - Boost Barometric Compensation - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: Boost Control - Barometric Pressure
- **Unit**: PASCAL
- **Range**: 63129.6953 to 96006.9375
- **Points**: 8

### Y-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 1600.0000 to 8000.0000
- **Points**: 9

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM | 63129.6953 | 69705.1484 | 76280.5938 | 82856.0391 | 89431.4922 | 92060.1250 | 94692.6172 | 96006.9375 |
--------------------------------------------------------------------------------------------------------------------
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4000.0000 |   -11.7188 |    -9.3750 |    -7.0313 |    -4.6875 |    -2.3438 |     0.0000 |     0.0000 |     0.0000 |
 4800.0000 |   -28.9063 |   -24.2188 |   -18.7500 |   -13.2813 |    -6.2500 |    -3.1250 |     0.0000 |     0.0000 |
 5600.0000 |   -39.8438 |   -34.3750 |   -27.3438 |   -18.7500 |   -10.9375 |    -7.8125 |    -3.1250 |     0.0000 |
 6400.0000 |   -24.2188 |   -17.1875 |   -10.9375 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 7200.0000 |   -24.2188 |   -17.1875 |   -10.9375 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
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

# Airflow - Turbo - Wastegate - Wastegate Barometric Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x10 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate Barometric Compensation - 2018 - LF9C102P.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: Boost Control - Barometric Pressure
- **Unit**: PASCAL
- **Range**: 63129.6953 to 99953.7500
- **Points**: 10

### Y-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 3000.0000 to 6100.0000
- **Points**: 9

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM | 63129.6953 | 69705.1484 | 76280.5938 | 82856.0391 | 89431.4922 | 92060.1250 | 94692.6172 | 96006.9375 |
--------------------------------------------------------------------------------------------------------------------
 3000.0000 |   -20.3125 |   -14.8438 |   -10.1563 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4000.0000 |   -29.6875 |   -25.0000 |   -20.3125 |   -14.8438 |    -7.8125 |     0.0000 |     0.0000 |     0.0000 |
 4800.0000 |   -35.1563 |   -29.6875 |   -25.0000 |   -18.7500 |   -11.7188 |     0.0000 |     0.0000 |     0.0000 |
 5200.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |    -7.0313 |     0.0000 |     0.0000 |
 5600.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 5800.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 5900.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 6000.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
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

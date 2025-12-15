# Throttle - Requested Torque - Limits - Requested Torque IAT Limit

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 14x12 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Requested Torque IAT Limit - 2017 - RogueWRX.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: IAT
- **Unit**: CELSIUS
- **Range**: -40.0000 to 70.0000
- **Points**: 12

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7600.0000
- **Points**: 14

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |   120.0000 |   120.0000 |   120.0000 |   120.0000 |   160.0000 |   160.0000 |   160.0000 |   160.0000 |
  800.0000 |   120.0000 |   120.0000 |   120.0000 |   125.0000 |   160.0000 |   160.0000 |   160.0000 |   160.0000 |
 1200.0000 |   130.0000 |   130.0000 |   145.0000 |   145.0000 |   185.0000 |   200.0000 |   215.0000 |   215.0000 |
 1600.0000 |   140.0000 |   140.0000 |   150.0000 |   150.0000 |   230.0000 |   240.0000 |   250.0000 |   250.0000 |
 1800.0000 |   150.0000 |   175.0000 |   195.0000 |   210.0000 |   275.0000 |   288.0000 |   300.0000 |   300.0000 |
 2000.0000 |   160.0000 |   210.0000 |   240.0000 |   270.0000 |   300.0000 |   325.0000 |   350.0000 |   350.0000 |
 2300.0000 |   205.0000 |   240.0000 |   240.0000 |   281.2500 |   300.0000 |   339.5000 |   350.0000 |   350.0000 |
 2400.0000 |   220.0000 |   240.0000 |   250.0000 |   285.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |
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

# Throttle - Requested Torque - Out-of-Gear - D

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Out-of-Gear - D - 2017 - RogueWRX.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: Throttle - Requested Torque - Accelerator Position
- **Unit**: PERCENT
- **Range**: 0.0000 to 100.0000
- **Points**: 20

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 8000.0000
- **Points**: 21

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.4944 |     0.4959 |     0.4974 |     0.4990 |     0.5005 |     0.9995 |     2.0005 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     3.0000 |     3.1000 |     3.2000 |     3.3000 |     4.0000 |     7.0000 |    14.9000 |
 1000.0000 |     0.0000 |     2.6000 |     2.7000 |     2.8000 |     2.9000 |     3.0000 |     5.0000 |     7.9000 |
 1200.0000 |     0.0000 |     0.2000 |     0.2125 |     0.2250 |     0.3000 |     0.3125 |     0.8000 |     3.0000 |
 1400.0000 |     0.0000 |     0.2000 |     0.2125 |     0.2250 |     0.2375 |     0.3000 |     0.3125 |     0.9000 |
 1600.0000 |     0.0000 |     0.2000 |     0.2125 |     0.2250 |     0.2375 |     0.3000 |     0.3125 |     0.4000 |
 1800.0000 |     0.0000 |     0.2000 |     0.2125 |     0.2250 |     0.2375 |     0.2500 |     0.3000 |     0.4000 |
 2000.0000 |     0.0000 |     0.1000 |     0.2125 |     0.2250 |     0.2375 |     0.2500 |     0.2625 |     0.4000 |
 2200.0000 |     0.0000 |     0.1000 |     0.1250 |     0.2000 |     0.2125 |     0.2250 |     0.2375 |     0.3000 |
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

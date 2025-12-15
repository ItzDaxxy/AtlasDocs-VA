# Fuel - Open Loop - AVCS Enabled - Target Base (Low DAM)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Enabled - Target Base (Low DAM) - 2017 - RogueWRX.csv` |

## Description

*Add description of what this table controls and when it's used.*

## Axes

### X-Axis

- **Parameter**: CALC LOAD
- **Unit**: G_PER_REV
- **Range**: 0.9058 to 2.9762
- **Points**: 20

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 9200.0000
- **Points**: 24

## Cell Values

- **Unit**: AFR_EQ
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.9058 |     1.0352 |     1.2293 |     1.2940 |     1.5528 |     1.8116 |     2.0704 |     2.3292 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
  800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
 1200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
 1600.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1172 |     1.1602 |     1.1797 |     1.3008 |     1.3008 |
 2000.0000 |     1.0000 |     1.0000 |     1.0508 |     1.1172 |     1.2109 |     1.2500 |     1.2813 |     1.3086 |
 2400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1094 |     1.1406 |     1.3008 |     1.3008 |     1.3789 |
 2800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0195 |     1.1016 |     1.1914 |     1.2891 |     1.3984 |
 3200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0313 |     1.1172 |     1.1992 |     1.2813 |     1.3516 |
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

# Throttle - Requested Torque - Limits - Maximums - Maximum C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x11 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Maximums - Maximum C - 2017 - RogueWRX.csv` |

## Description

Defines the maximum allowable torque request based on engine RPM for operating condition C. This table provides a third set of torque limits used under specific ECU-determined conditions, completing the Maximum A/B/C table set.

Maximum C may apply during conditions like warm engine operation, specific driving modes, or as a baseline for comparison against other maximum tables. The ECU selects the minimum of applicable maximum tables to determine the final torque limit.

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 1200.0000 to 8400.0000
- **Points**: 11

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |  1200.0000 |  1600.0000 |  2000.0000 |  2800.0000 |  3600.0000 |  4400.0000 |  5200.0000 |  6000.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using engine RPM:

1. **RPM Reading**: ECU monitors current engine RPM
2. **Condition Check**: ECU determines if Maximum C conditions apply
3. **Table Lookup**: Interpolates maximum torque for current RPM
4. **Torque Limiting**: Requested torque capped at this value

## Related Tables

- **Throttle - Requested Torque - Limits - Maximum A/B**: Other maximum torque tables
- **Throttle - Requested Torque - In-Gear/Out-of-Gear**: Base torque request tables
- **Throttle - Target Throttle - Main**: Torque to throttle conversion

## Related Datalog Parameters

- **Requested Torque (Nm)**: Driver's torque demand
- **Limited Torque (Nm)**: Final capped torque
- **Engine RPM**: X-axis input

## Tuning Notes

**Common Modifications:**
- Maintain consistency with Maximum A and B tables
- Scale proportionally with engine modifications
- Match to actual engine torque capability

**Considerations:**
- All three maximum tables work together
- ECU uses minimum of applicable limits

## Warnings

- Torque limits protect drivetrain components
- Excessive torque limits risk engine/transmission damage
- Changes must match supporting modifications

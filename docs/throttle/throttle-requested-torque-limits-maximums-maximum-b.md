# Throttle - Requested Torque - Limits - Maximums - Maximum B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x11 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Maximums - Maximum B - 2017 - RogueWRX.csv` |

## Description

Defines the maximum allowable torque request based on engine RPM for operating condition B. This table provides an alternate set of torque limits used under specific conditions, potentially when additional safety margin is required.

Maximum B may apply during conditions like reduced traction situations, specific gear operation, or temperature-related derating. The ECU selects between Maximum A, B, and C tables based on operating state.

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
2. **Condition Check**: ECU determines if Maximum B conditions apply
3. **Table Lookup**: Interpolates maximum torque for current RPM
4. **Torque Limiting**: Requested torque capped at this value

## Related Tables

- **Throttle - Requested Torque - Limits - Maximum A/C**: Other maximum torque tables
- **Throttle - Requested Torque - In-Gear/Out-of-Gear**: Base torque request tables
- **Throttle - Target Throttle - Main**: Torque to throttle conversion

## Related Datalog Parameters

- **Requested Torque (Nm)**: Driver's torque demand
- **Limited Torque (Nm)**: Final capped torque
- **Engine RPM**: X-axis input

## Tuning Notes

**Common Modifications:**
- Coordinate changes with Maximum A and C tables
- Ensure consistency across all maximum tables
- Match to actual engine capability

**Considerations:**
- May be more conservative than Maximum A for protection
- Changes should match drivetrain limits

## Warnings

- Torque limits protect drivetrain components
- Excessive limits risk mechanical damage
- Test carefully in all operating conditions

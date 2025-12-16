# Throttle - Requested Torque - Limits - Maximums - Maximum A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x11 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Maximums - Maximum A - 2017 - RogueWRX.csv` |

## Description

Defines the maximum allowable torque request based on engine RPM for operating condition A. This table sets an upper limit on how much torque the driver can request through the accelerator pedal, preventing excessive torque demands that could exceed the engine's safe operating limits.

Maximum A is one of multiple maximum torque tables (A, B, C) used under different operating conditions. The ECU selects the appropriate table based on factors like gear position, traction control status, or temperature conditions.

This limit directly affects throttle response and power delivery - the requested torque (from pedal input) is clipped to these maximum values before being converted to throttle opening commands.

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
2. **Condition Check**: ECU determines if Maximum A conditions apply
3. **Table Lookup**: Interpolates maximum torque for current RPM
4. **Torque Limiting**: Requested torque capped at this value
5. **Throttle Control**: Limited torque request converted to throttle position

**Torque Request Flow:**
Pedal Position → Base Torque Request → MIN(Request, Maximum Table) → Throttle Target

## Related Tables

- **Throttle - Requested Torque - Limits - Maximum B/C**: Other maximum torque tables
- **Throttle - Requested Torque - In-Gear/Out-of-Gear**: Base torque request tables
- **Throttle - Target Throttle - Main**: Converts torque request to throttle position

## Related Datalog Parameters

- **Requested Torque (Nm)**: Driver's torque demand (before limiting)
- **Limited Torque (Nm)**: Final torque after applying limits
- **Engine RPM**: X-axis input for table lookup
- **Throttle Opening (%)**: Final throttle command

## Tuning Notes

**Common Modifications:**
- Increase values to allow higher torque requests on modified engines
- Must be coordinated with actual engine capability
- Higher limits require supporting fuel, boost, and ignition changes

**Considerations:**
- These limits exist to protect the drivetrain
- Exceeding engine/transmission torque capacity risks damage
- Changes should match other torque management tables

## Warnings

- Exceeding safe torque limits causes drivetrain damage
- Must match actual engine torque output capability
- Coordinate with boost limits and fuel delivery capacity
- Excessive torque requests can overwhelm traction control
- Test carefully - torque limits are safety-critical

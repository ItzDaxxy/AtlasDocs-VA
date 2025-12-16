# Throttle - Requested Torque - Limits - Requested Torque Limit Per Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Requested Torque Limit Per Gear - 2017 - RogueWRX.csv` |

## Description

Defines maximum allowable torque request for each gear position (0-7, where 0 typically represents neutral/unknown and 1-6 represent actual gears). This table allows gear-specific torque limiting to protect the drivetrain in lower gears where torque multiplication is highest.

Lower gears see higher driveline loads due to gear multiplication - 1st gear may have torque limits 40-50% lower than 6th gear to protect the clutch, transmission, and axles from excessive stress. This is particularly important for modified vehicles with increased engine torque output.

## Axes

### X-Axis

- **Parameter**: null
- **Unit**: NONE
- **Range**: 0.0000 to 7.0000
- **Points**: 8

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     1.0000 |     2.0000 |     3.0000 |     4.0000 |     5.0000 |     6.0000 |     7.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs direct lookup using current gear:

1. **Gear Detection**: ECU determines current gear from RPM/speed ratio
2. **Table Lookup**: Direct lookup for that gear's torque limit
3. **Torque Limiting**: Requested torque capped at gear-specific value
4. **Protection Active**: Lower gears = lower torque limits

**Gear-Based Protection:**
- Gear 1: Most restrictive (highest driveline multiplication)
- Gear 2-3: Moderate restriction
- Gear 4-6: Less restrictive (lower multiplication)

## Related Tables

- **Transmission - Gear Ratios**: Used for gear detection
- **Throttle - Requested Torque - Limits - Maximum A/B/C**: Other torque limits
- **Throttle - Requested Torque - In-Gear**: Base torque request tables

## Related Datalog Parameters

- **Current Gear**: Determines which limit applies
- **Requested Torque (Nm)**: Before gear limiting
- **Limited Torque (Nm)**: After gear-based limiting

## Tuning Notes

**Common Modifications:**
- Increase limits on modified drivetrains (clutch, axles, transmission)
- Must match actual drivetrain strength
- Scale proportionally with engine torque increases

**Considerations:**
- 1st gear limit is most critical - highest driveline stress
- Clutch capacity often limiting factor
- Axle strength varies by model year and option packages

## Warnings

- Exceeding drivetrain limits causes mechanical failure
- Clutch, axles, and transmission have specific torque ratings
- Modified clutches may handle more torque but require adjustment
- Always verify drivetrain can handle torque before increasing limits
- 1st/2nd gear launches put maximum stress on components

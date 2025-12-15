# Throttle - Requested Torque - In-Gear - C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - In-Gear - C - 2017 - RogueWRX.csv` |

## Description

This is an additional variant in-gear requested torque table (variant C) that defines engine torque output in Nm when the transmission is in-gear. The presence of multiple variants (A, B, C, D) suggests the ECU has sophisticated table selection logic based on various operating conditions such as vehicle speed ranges, gear selection, driving modes, or environmental factors. This table contributes to the ECU's ability to optimize power delivery across diverse driving scenarios.

## Axes

### X-Axis

- **Parameter**: Throttle - Requested Torque - Accelerator Position
- **Unit**: PERCENT
- **Range**: 0.0000 to 100.0000
- **Points**: 20

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 6805.0781
- **Points**: 21

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.2502 |     0.2594 |     0.2701 |     0.2792 |     0.5005 |     0.9995 |     2.0005 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     3.0000 |     3.1000 |     3.2000 |     3.3000 |     4.0000 |     7.0000 |    14.9000 |
 1200.0000 |     0.0000 |     2.6000 |     2.7000 |     2.8000 |     2.9000 |     3.0000 |     5.0000 |     7.9000 |
 1600.0000 |     0.0000 |     2.5000 |     2.5125 |     2.5250 |     2.5375 |     2.5500 |     2.8000 |     3.0000 |
 2000.0000 |     0.0000 |     2.5000 |     2.5125 |     2.5250 |     2.5375 |     2.5500 |     2.8000 |     3.0000 |
 2400.0000 |     0.0000 |     2.5000 |     2.5125 |     2.5250 |     2.5375 |     2.5500 |     2.8000 |     3.0000 |
 2800.0000 |     0.0000 |     1.5000 |     1.5125 |     1.5250 |     1.5375 |     1.5750 |     1.6000 |     1.8000 |
 3200.0000 |     0.0000 |     1.3000 |     1.3125 |     1.3250 |     1.3375 |     1.3750 |     1.4250 |     1.5000 |
 3600.0000 |     0.0000 |     1.1000 |     1.1125 |     1.1250 |     1.1375 |     1.1750 |     1.2000 |     1.2500 |
```

## Functional Behavior

The ECU uses 2D interpolation based on RPM and accelerator position when conditions select In-Gear C table. The exact switching logic may involve multiple parameters such as gear position, vehicle speed, coolant temperature, or other factors. The torque output is processed identically to other torque request tables, passing through the denominator and limits before controlling throttle.

## Related Tables

- Throttle - Requested Torque - In-Gear - A, B (Main), D
- Throttle - Requested Torque - Out-of-Gear tables
- Throttle - Requested Torque - Requested Torque Denominator
- Throttle - Requested Torque - Limits

## Related Datalog Parameters

- Requested Torque
- Accelerator Pedal Position
- Engine RPM
- Clutch Switch Status
- Gear Position
- Vehicle Speed
- Active Table Selector

## Tuning Notes

For In-Gear C variant tuning:
- Determine activation conditions through careful datalogging
- May be gear-specific or speed-range specific
- Often calibrated similarly to In-Gear B unless specific differentiation is needed
- Some tuners copy In-Gear B values to all variants for consistency
- Consider whether specialized calibration provides meaningful benefit
Without clear understanding of activation logic, conservative calibration matching In-Gear B is recommended.

## Warnings

Multiple table variants increase calibration complexity:
- Switching between tables must be seamless to avoid drivability issues
- Mismatched values across variants can cause inconsistent throttle response
- Difficult to test all activation conditions comprehensively
- May be activated only in specific gears or speed ranges
- Incorrect values can cause safety issues in the specific conditions where this table is active
Document when this table is used. Ensure all in-gear variants maintain safe, consistent behavior.

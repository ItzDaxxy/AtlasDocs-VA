# Throttle - Requested Torque - In-Gear - A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - In-Gear - A - 2017 - RogueWRX.csv` |

## Description

This is an alternate in-gear requested torque table that defines engine torque output in Nm based on accelerator pedal position and RPM when the transmission is in-gear. The "A" designation indicates this is a secondary or variant table that may be used under specific operating conditions different from the "B (Main)" table. The ECU selects between In-Gear A and B tables based on additional switching logic such as driving mode, vehicle speed, or other operational parameters.

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

The ECU interpolates this table using RPM and accelerator pedal position when in-gear conditions are met and the switching logic selects table A. The output torque value is processed through the denominator table to create a torque ratio for throttle control. The switching between In-Gear A and B may be transparent to the driver or may correspond to specific driving modes or conditions.

## Related Tables

- Throttle - Requested Torque - In-Gear - B (Main)
- Throttle - Requested Torque - In-Gear - C, D
- Throttle - Requested Torque - Out-of-Gear tables
- Throttle - Requested Torque - Requested Torque Denominator
- Throttle - Requested Torque - Limits

## Related Datalog Parameters

- Requested Torque
- Accelerator Pedal Position
- Engine RPM
- Clutch Switch Status
- Gear Position
- Active Torque Table Selector

## Tuning Notes

When tuning In-Gear A, understand its relationship to In-Gear B:
- Compare values to In-Gear B to identify intended behavior differences
- Some tuners make A and B identical to simplify calibration
- May represent different drive modes (Sport vs Normal, etc.)
- Ensure smooth transitions if ECU switches between A and B during driving
- Coordinate with Target Throttle and torque limit tables
Monitor datalogs to determine when this table is active versus In-Gear B.

## Warnings

Incorrect calibration can cause:
- Abrupt power delivery changes when switching between In-Gear A and B
- Traction loss if torque requests exceed tire grip capability
- Confusion during troubleshooting if table selection is not understood
- Drivability issues if A and B tables have very different characteristics
- Over-boost or engine damage if requests exceed safe limits
Test thoroughly in all conditions where this table may be active. Ensure torque limits protect the engine.

# Throttle - Requested Torque - In-Gear - D

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | ` .csv` |

## Description

This is the fourth variant in-gear requested torque table (variant D) defining engine torque output in Nm when the transmission is in-gear. The D variant represents the most specialized in-gear table, potentially used for very specific operating conditions such as particular gears, driving modes, or edge case scenarios. The expanded RPM range (up to 8000 RPM vs 6805 in A/B/C variants) suggests this may be used for high-RPM or performance-oriented conditions.

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

The ECU interpolates this table using RPM and accelerator position when specific conditions select the In-Gear D variant. The extended RPM range suggests this table may be active during high-performance driving or specific gear selections. Note the very low torque values in many cells (0.2-0.4 Nm at mid-range), which may indicate this is a specialized table for particular operating conditions rather than normal driving.

## Related Tables

- Throttle - Requested Torque - In-Gear - A, B (Main), C
- Throttle - Requested Torque - Out-of-Gear - D (similar RPM range)
- Throttle - Requested Torque - Requested Torque Denominator
- Throttle - Requested Torque - Limits

## Related Datalog Parameters

- Requested Torque
- Accelerator Pedal Position
- Engine RPM
- Clutch Switch Status
- Gear Position
- Vehicle Speed
- Driving Mode Selector

## Tuning Notes

The D variant requires careful analysis before modification:
- Very low torque values suggest specialized purpose - understand before changing
- Extended RPM range indicates high-RPM operation capability
- May be used only in specific gears (likely higher gears based on low torque values)
- Could represent an economy mode, cruise mode, or deceleration fuel cut recovery
- Observe extensive datalogs to confirm when this table is actually used
Do not assume this table should match In-Gear B - it appears intentionally different for specific purposes.

## Warnings

This table's unusual characteristics require special attention:
- Very low torque values may cause unexpected behavior if activated during normal driving
- Modifying without understanding activation conditions can create serious drivability issues
- May be critical for specific vehicle systems (cruise control, traction management, etc.)
- Extended RPM range means changes affect high-RPM behavior
- Incorrect calibration could prevent proper operation of associated vehicle features
Only modify if activation conditions are clearly understood. The low torque values are likely intentional for the specific conditions where this table is used.

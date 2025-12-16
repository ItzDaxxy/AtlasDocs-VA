# Throttle - Requested Torque - In-Gear - B (Main)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - In-Gear - B (Main) - 2017 - RogueWRX.csv` |

## Description

This table defines the requested engine torque in Newton-meters (Nm) based on accelerator pedal position and engine RPM when the transmission is IN-GEAR (clutch engaged). The "B (Main)" designation indicates this is the primary table used for in-gear operation. The ECU uses this table to convert driver input from the accelerator pedal into a specific torque demand that the engine must produce. This torque request then feeds into the Target Throttle tables to determine the actual throttle plate opening. In-gear tables typically provide more conservative torque requests compared to out-of-gear tables to improve traction control and drivability.

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

The ECU interpolates this table using current engine RPM and accelerator pedal position to determine the target torque output in Nm. This torque value is then divided by the Requested Torque Denominator table to create a torque ratio, which is used as the X-axis input for Target Throttle tables. The in-gear detection typically comes from the clutch position switch or transmission gear sensor. When the clutch is engaged (in-gear condition detected), this table becomes active. The requested torque is also subject to various limits including DAM limit, IAT limit, and per-gear limits before being sent to throttle control.

## Related Tables

- Throttle - Requested Torque - Out-of-Gear - Main
- Throttle - Requested Torque - In-Gear - A, C, D
- Throttle - Requested Torque - Requested Torque Denominator
- Throttle - Requested Torque - Limits (DAM, IAT, Per Gear)
- Throttle - Target Throttle tables

## Related Datalog Parameters

- Requested Torque
- Accelerator Pedal Position
- Engine RPM
- Clutch Switch Status
- Gear Position
- Final Requested Torque (after limits)
- Torque Ratio

## Tuning Notes

Modifying this table directly affects throttle response and power delivery when in gear:
- Increasing torque values creates more aggressive throttle response and faster acceleration
- Decreasing values creates smoother, more conservative power delivery
- Low RPM areas (800-2000 RPM) are critical for daily drivability and smoothness
- Higher torque requests may require adjustments to Target Throttle tables
- Must be coordinated with boost control to prevent over-boost
- Consider traction limitations in lower gears when increasing values
Common modifications include smoothing transitions, reducing low-RPM sensitivity, and scaling values for increased power output. Always validate changes don't exceed torque limits or cause traction issues.

## Warnings

Improper modifications can create dangerous driving conditions:
- Excessive torque requests can cause wheel spin and loss of traction, especially in lower gears
- Too aggressive low-RPM torque can cause bucking, lurching, or stalling
- Mismatched in-gear and out-of-gear tables cause jerking during clutch engagement
- Values exceeding engine capability can cause over-boost, knock, or mechanical damage
- Very low values can make vehicle undriveable or unable to accelerate safely
- Inconsistent pedal response can confuse the driver and cause control issues
Always consider the vehicle's traction capabilities, especially in wet conditions. Test modifications in safe, controlled environments. Ensure torque limits are properly set to prevent engine damage.

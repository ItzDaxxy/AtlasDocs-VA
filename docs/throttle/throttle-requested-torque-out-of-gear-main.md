# Throttle - Requested Torque - Out-of-Gear - Main

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Out-of-Gear - Main - 2017 - RogueWRX.csv` |

## Description

Defines the base torque request generated from accelerator pedal position when the vehicle is out of gear (clutch depressed, neutral, or between gears). This table converts accelerator pedal percentage and RPM into a torque request value used by the throttle control system.

Out-of-gear tables typically allow higher torque requests than in-gear tables at the same pedal position because there's no load on the drivetrain. This allows for quicker rev-matching, blipping for downshifts, and responsive throttle feel during gear changes.

The "Main" table is the primary out-of-gear torque request map, with variants A, C, D providing alternative mappings for different conditions.

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

The ECU performs 2D interpolation using accelerator position and RPM:

1. **Out-of-Gear Detection**: ECU detects clutch depressed or neutral
2. **Pedal Reading**: ECU reads accelerator position (0-100%)
3. **RPM Reading**: ECU monitors current engine RPM
4. **Table Lookup**: 2D interpolation determines torque request
5. **Throttle Control**: Torque request converted to throttle position

**Out-of-Gear vs In-Gear:**
- Out-of-gear: Higher torque/pedal for responsive free-rev
- In-gear: Lower torque/pedal for smoother power delivery

## Related Tables

- **Throttle - Requested Torque - Out-of-Gear A/C/D**: Variant tables
- **Throttle - Requested Torque - In-Gear**: In-gear torque mapping
- **Throttle - Target Throttle - Main**: Torque to throttle conversion

## Related Datalog Parameters

- **Accelerator Position (%)**: X-axis input
- **Engine RPM**: Y-axis input
- **Clutch Switch**: Determines in-gear vs out-of-gear
- **Requested Torque (Nm)**: Output from this table

## Tuning Notes

**Common Modifications:**
- Increase low-pedal values for more responsive blipping
- Adjust for better rev-matching during downshifts
- Smooth transitions for more predictable feel

**Considerations:**
- Affects how quickly engine responds during gear changes
- Higher values = faster revving but potentially harder to control
- Must work well with rev-hang reduction if modified

## Warnings

- Excessive values cause unpredictable throttle response
- Very high torque requests in neutral can over-rev engine
- Coordinate with in-gear tables for smooth clutch engagement
- Test carefully during actual driving scenarios

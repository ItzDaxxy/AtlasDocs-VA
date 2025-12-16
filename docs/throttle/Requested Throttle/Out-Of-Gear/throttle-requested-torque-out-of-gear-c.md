# Throttle - Requested Torque - Out-of-Gear - C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Out-of-Gear - C - 2017 - RogueWRX.csv` |

## Description

Defines an alternate torque request map for out-of-gear operation (variant C). This table converts accelerator pedal position and RPM into torque request when the clutch is depressed or the transmission is in neutral.

Table C may be used under specific ECU-determined conditions. Multiple out-of-gear tables (Main, A, C, D) allow optimization for different operating scenarios such as temperature, driving mode, or system state.

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

1. **Out-of-Gear Detection**: ECU detects clutch or neutral state
2. **Condition Check**: ECU determines if Table C conditions apply
3. **Pedal/RPM Reading**: ECU reads accelerator and RPM
4. **Table Lookup**: 2D interpolation for torque request
5. **Throttle Control**: Torque converted to throttle position

## Related Tables

- **Throttle - Requested Torque - Out-of-Gear Main/A/D**: Other out-of-gear tables
- **Throttle - Requested Torque - In-Gear**: In-gear torque mapping
- **Throttle - Target Throttle - Main**: Torque to throttle conversion

## Related Datalog Parameters

- **Accelerator Position (%)**: X-axis input
- **Engine RPM**: Y-axis input
- **Clutch Switch**: Out-of-gear detection
- **Requested Torque (Nm)**: Table output

## Tuning Notes

**Common Modifications:**
- Coordinate with Main and other out-of-gear tables
- Adjust for consistent throttle feel across conditions
- Match to driver preference for rev-matching

**Considerations:**
- Changes should be consistent across all out-of-gear tables
- Test under conditions that activate this specific table

## Warnings

- Excessive values cause unpredictable throttle response
- Coordinate with in-gear tables for smooth transitions
- Test during actual gear changes

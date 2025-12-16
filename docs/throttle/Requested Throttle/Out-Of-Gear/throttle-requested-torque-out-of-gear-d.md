# Throttle - Requested Torque - Out-of-Gear - D

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x20 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Out-of-Gear - D - 2017 - RogueWRX.csv` |

## Description

Defines an alternate torque request map for out-of-gear operation (variant D). This table converts accelerator pedal position and RPM into torque request when the clutch is depressed or the transmission is in neutral.

Table D shows notably lower torque values across most of the table compared to Main/A/C variants, suggesting it may be used for specific conditions requiring reduced throttle response, such as limp mode, cold start, or certain diagnostic states.

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

The ECU performs 2D interpolation using accelerator position and RPM:

1. **Out-of-Gear Detection**: ECU detects clutch or neutral state
2. **Condition Check**: ECU determines if Table D conditions apply
3. **Pedal/RPM Reading**: ECU reads accelerator and RPM
4. **Table Lookup**: 2D interpolation for torque request
5. **Throttle Control**: Torque converted to throttle position

**Notable Characteristics:**
- Lower values than other out-of-gear tables
- May be used for reduced-response conditions
- Conservative mapping for safety scenarios

## Related Tables

- **Throttle - Requested Torque - Out-of-Gear Main/A/C**: Other out-of-gear tables
- **Throttle - Requested Torque - In-Gear**: In-gear torque mapping
- **Throttle - Target Throttle - Main**: Torque to throttle conversion

## Related Datalog Parameters

- **Accelerator Position (%)**: X-axis input
- **Engine RPM**: Y-axis input
- **Clutch Switch**: Out-of-gear detection
- **Requested Torque (Nm)**: Table output

## Tuning Notes

**Common Modifications:**
- Generally not modified as it's likely a fallback/safety table
- May need adjustment if other out-of-gear tables are modified
- Understand activation conditions before changing

**Considerations:**
- Lower values suggest conservative/safety-oriented table
- May activate during fault conditions

## Warnings

- Modifying safety-oriented tables can create dangerous conditions
- Understand why this table activates before changing values
- Test thoroughly in all operating conditions

# Throttle - Requested Torque - Requested Torque Denominator

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x21 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Requested Torque Denominator - 2017 - RogueWRX.csv` |

## Description

Defines the denominator value used in torque ratio calculations based on engine RPM. The ECU uses this to normalize torque requests relative to the engine's torque capability at each RPM point.

**Torque Ratio = Requested Torque / Denominator**

This creates a normalized value (typically 0-1) representing the percentage of available torque being requested. The denominator effectively represents the maximum torque reference at each RPM, allowing consistent throttle mapping regardless of where peak torque occurs in the power band.

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 8000.0000
- **Points**: 21

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   800.0000 |  1000.0000 |  1200.0000 |  1400.0000 |  1600.0000 |  1800.0000 |  2000.0000 |  2400.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using engine RPM:

1. **RPM Reading**: ECU monitors current engine RPM
2. **Table Lookup**: Interpolates denominator value for current RPM
3. **Ratio Calculation**: Torque Ratio = Requested Torque / Denominator
4. **Usage**: Ratio used in Target Throttle tables and other calculations

**Calculation Example:**
- Requested Torque: 300 Nm
- Denominator at RPM: 400 Nm
- Torque Ratio: 300/400 = 0.75 (75% of available torque)

## Related Tables

- **Throttle - Target Throttle - Main**: Uses torque ratio for throttle calculation
- **Throttle - Requested Torque - In-Gear/Out-of-Gear**: Source of torque request
- **Throttle - Requested Torque - Limits**: Torque capping tables

## Related Datalog Parameters

- **Requested Torque (Nm)**: Numerator in ratio calculation
- **Requested Torque Ratio**: Result of calculation (0-1 typical)
- **Engine RPM**: X-axis input for denominator lookup

## Tuning Notes

**Common Modifications:**
- Adjust to match engine's actual torque curve on modified engines
- Should approximate peak torque capability at each RPM
- Affects how pedal position translates to throttle opening

**Considerations:**
- Scaling this affects pedal sensitivity across RPM range
- Lower values = more aggressive throttle response
- Should match actual engine capability for linear pedal feel

## Warnings

- Incorrect values cause nonlinear or unpredictable throttle response
- Too low causes excessive throttle opening for given pedal position
- Too high causes sluggish response
- Coordinate with Target Throttle tables when modifying

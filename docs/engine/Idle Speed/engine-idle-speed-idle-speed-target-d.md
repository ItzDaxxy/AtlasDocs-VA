# Engine - Idle Speed - Idle Speed Target D

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target D - 2018 - LF9C102P.csv` |

## Description

Defines target idle RPM based on coolant temperature for operating condition D. This is one of multiple idle speed target tables (A through J) used by the ECU to determine desired idle speed under various operating conditions. The ECU selects among these tables based on combinations of A/C compressor state, transmission position (Park/Neutral vs Drive), electrical load status, and other accessory loads.

Table D typically corresponds to a specific load combination such as transmission in gear with A/C off. Each table provides a temperature-based idle RPM curve, with higher RPM commanded at cold temperatures for stable warm-up and lower RPM when fully warmed for fuel economy and NVH reduction.

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: RPM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using coolant temperature:

1. **Condition Check**: ECU determines if Table D conditions are active based on current operating state
2. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
3. **Table Lookup**: Interpolates between temperature breakpoints to determine target RPM
4. **Idle Control**: Electronic throttle and ignition timing adjusted to achieve target RPM

**Idle Target Selection Logic:**
The ECU continuously monitors multiple inputs to select the appropriate idle table. When conditions matching Table D are met, this table provides the base target RPM, which may be further modified by compensations.

## Related Tables

- **Engine - Idle Speed - Target A, B, C, E-J**: Other idle target tables for different conditions
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Altitude-based idle adjustments
- **Throttle - Idle Control**: Throttle position control to achieve target RPM

## Related Datalog Parameters

- **Target Idle RPM**: Final commanded idle speed after table selection
- **Actual RPM**: Measured engine speed at idle
- **Coolant Temperature (°C)**: X-axis input for table lookup
- **A/C Clutch Status**: Affects table selection
- **Transmission Gear/Range**: Affects table selection
- **Electrical Load Status**: May affect table selection

## Tuning Notes

**Common Modifications:**
- Increase values if idle is unstable under this specific condition
- Adjust cold temperature values if cold-start idle hunts or is rough
- Maintain consistency with other idle tables (A-J) to prevent abrupt RPM changes when conditions change

**Considerations:**
- Changes should be coordinated across all idle tables for smooth transitions
- Higher idle improves stability but increases fuel consumption and heat
- Lower idle improves fuel economy but may cause stalling if too aggressive
- Test under the specific conditions that activate this table

## Warnings

- Inconsistent values between tables cause hunting or surging during condition transitions
- Too low idle RPM may cause stalling, especially with A/C cycling or electrical loads
- Too high idle wastes fuel and may indicate underlying issues
- Always test all operating conditions (A/C on/off, in gear/neutral, various loads) after changes
- Ensure idle tables work correctly with any camshaft or intake modifications

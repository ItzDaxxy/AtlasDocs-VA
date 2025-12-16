# Engine - Idle Speed - Idle Speed Target E

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target E - 2018 - LF9C102P.csv` |

## Description

Defines target idle RPM based on coolant temperature for operating condition E. This is one of multiple idle speed target tables (A through J) used by the ECU to determine desired idle speed under various operating conditions. The ECU selects among these tables based on combinations of A/C compressor state, transmission position, electrical load status, and other accessory demands.

Table E typically corresponds to a specific load combination, potentially transmission in gear with A/C engaged. Each table provides a temperature-based idle RPM curve, commanding higher RPM at cold temperatures for stable combustion during warm-up and lower RPM when fully warmed for improved fuel economy.

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

1. **Condition Check**: ECU determines if Table E conditions are active based on current operating state
2. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
3. **Table Lookup**: Interpolates between temperature breakpoints to determine target RPM
4. **Idle Control**: Electronic throttle and ignition timing adjusted to achieve target RPM

**Idle Target Selection Logic:**
The ECU continuously monitors multiple inputs to select the appropriate idle table. When conditions matching Table E are met, this table provides the base target RPM.

## Related Tables

- **Engine - Idle Speed - Target A-D, F-J**: Other idle target tables for different conditions
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Altitude-based idle adjustments
- **Throttle - Idle Control**: Throttle position control to achieve target RPM

## Related Datalog Parameters

- **Target Idle RPM**: Final commanded idle speed
- **Actual RPM**: Measured engine speed at idle
- **Coolant Temperature (°C)**: X-axis input for table lookup
- **A/C Clutch Status**: Affects table selection
- **Transmission Gear/Range**: Affects table selection

## Tuning Notes

**Common Modifications:**
- Increase values if idle is unstable under this specific condition
- Adjust cold temperature values if cold-start idle is rough
- Maintain consistency with other idle tables to prevent abrupt RPM changes

**Considerations:**
- Changes should be coordinated across all idle tables
- Higher idle = more stability but increased fuel consumption
- Test under the specific conditions that activate this table

## Warnings

- Inconsistent values between tables cause hunting or surging during transitions
- Too low idle RPM may cause stalling with accessory loads
- Too high idle wastes fuel
- Test all operating conditions after changes

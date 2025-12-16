# Engine - Idle Speed - Idle Speed Target C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target C - 2018 - LF9C102P.csv` |

## Description

Defines target idle RPM based on coolant temperature for operating condition C. This is one of multiple idle speed target tables (A through J) used by the ECU to determine desired idle speed. The ECU selects between tables based on operating state - Table C may correspond to a specific combination of conditions such as A/C status, transmission position, or electrical load state.

Each table provides a temperature-based idle RPM curve, with higher RPM at cold temperatures for warm-up and lower RPM when fully warmed for fuel economy.

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

1. **Condition Check**: ECU determines if Table C conditions are active
2. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
3. **Table Lookup**: Interpolates between temperature breakpoints
4. **Idle Control**: Adjusts throttle to achieve target RPM

## Related Tables

- **Engine - Idle Speed - Target A, B, D-J**: Other idle target tables
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Additional compensation
- **Throttle - Idle Control**: Achieves target RPM

## Related Datalog Parameters

- **Target Idle RPM**: Commanded idle speed
- **Actual Idle RPM**: Measured engine speed
- **Coolant Temperature (°C)**: X-axis input
- **A/C Clutch Status**: May affect table selection

## Tuning Notes

**Common Modifications:**
- Increase values if idle is unstable under specific conditions
- Maintain consistency with other idle tables (A, B, D-J)
- Adjust cold temperatures if warm-up idle is rough

**Considerations:**
- Changes should be coordinated across all idle tables
- Higher idle = more stable but wastes fuel
- Test under the specific conditions that activate this table

## Warnings

- Inconsistent values between tables cause hunting or surging
- Too low may cause stalling; too high wastes fuel
- Always modify in conjunction with related idle tables
- Test all operating conditions (A/C on/off, different loads) after changes

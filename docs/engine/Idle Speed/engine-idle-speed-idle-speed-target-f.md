# Engine - Idle Speed - Idle Speed Target F

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target F - 2018 - LF9C102P.csv` |

## Description

Defines target idle RPM based on coolant temperature for operating condition F. This is one of multiple idle speed target tables (A through J) used by the ECU to determine desired idle speed under various operating conditions. The ECU selects among these tables based on combinations of A/C compressor state, transmission position, electrical load status, and other operating parameters.

Table F corresponds to a specific combination of operating conditions. Each table provides a temperature-based idle RPM curve, with higher RPM at cold temperatures for stable warm-up operation and lower RPM when fully warmed for fuel efficiency.

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

1. **Condition Check**: ECU determines if Table F conditions are active
2. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
3. **Table Lookup**: Interpolates between temperature breakpoints for target RPM
4. **Idle Control**: Electronic throttle adjusted to achieve target RPM

## Related Tables

- **Engine - Idle Speed - Target A-E, G-J**: Other idle target tables
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Altitude adjustments
- **Throttle - Idle Control**: Throttle position control

## Related Datalog Parameters

- **Target Idle RPM**: Commanded idle speed
- **Actual RPM**: Measured engine speed
- **Coolant Temperature (°C)**: X-axis input
- **A/C Clutch Status**: Affects table selection
- **Transmission Position**: Affects table selection

## Tuning Notes

**Common Modifications:**
- Increase values if idle is unstable under this condition
- Adjust cold temperature values for smoother warm-up
- Maintain consistency with other idle tables

**Considerations:**
- Coordinate changes across all idle tables
- Test under specific conditions that activate this table

## Warnings

- Inconsistent values between tables cause idle hunting
- Too low may cause stalling; too high wastes fuel
- Test all operating conditions after changes

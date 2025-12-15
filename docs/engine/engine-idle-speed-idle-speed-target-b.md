# Engine - Idle Speed - Idle Speed Target B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target B - 2018 - LF9C102P.csv` |

## Description

Defines target idle RPM based on coolant temperature for operating condition B. This is one of multiple idle speed target tables (A through J) used by the ECU to determine desired idle speed under various conditions. Table B typically provides an alternate target for specific operating states such as A/C compressor engagement, electrical load conditions, or transmission state.

The ECU selects between idle tables based on active conditions. Table B values are often slightly higher than Table A to compensate for additional parasitic loads that require more engine power to maintain stable idle.

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

The ECU performs 1D interpolation using coolant temperature to determine target idle RPM when the conditions for Table B are active:

1. **Condition Check**: ECU determines if Table B conditions are met (e.g., A/C on, specific load state)
2. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
3. **Table Lookup**: Interpolates between temperature breakpoints to find target RPM
4. **Idle Control**: Adjusts electronic throttle to achieve target
5. **Load Compensation**: Higher targets compensate for additional loads

## Related Tables

- **Engine - Idle Speed - Target A, C-J**: Other idle target tables for different conditions
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Additional compensation factors
- **Throttle - Idle Control**: Works with targets to achieve desired RPM

## Related Datalog Parameters

- **Target Idle RPM**: The commanded idle speed
- **Actual Idle RPM**: Measured engine speed at idle
- **Coolant Temperature (°C)**: X-axis input for table lookup
- **A/C Clutch Status**: May trigger Table B selection
- **Electrical Load**: May affect table selection

## Tuning Notes

**Common Modifications:**
- Increase values if engine stalls with A/C or high electrical loads
- Keep values 50-100 RPM higher than Table A for additional load compensation
- Adjust proportionally with Table A modifications

**Considerations:**
- Must coordinate with other idle tables to prevent RPM jumps when switching conditions
- Higher idle wastes fuel but provides better stability under load
- Monitor for consistent behavior across table transitions

## Warnings

- Inconsistent values between tables can cause hunting or surging when conditions change
- Too low may cause stalling under load; too high wastes fuel
- Always modify in conjunction with related idle tables (A, C-J) for smooth operation
- Test with all accessories (A/C, lights, steering) to verify stability

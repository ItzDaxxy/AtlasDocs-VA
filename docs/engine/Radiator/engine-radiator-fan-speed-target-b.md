# Engine - Radiator - Fan Speed Target B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Engine - Radiator - Fan Speed Target B - 2018 - LF9C102P.csv` |

## Description

Defines the target fan speed (PWM duty cycle) based on coolant temperature for operating condition B. This table provides progressive fan speed control, allowing variable fan speeds rather than simple on/off operation. The PWM signal controls the fan motor speed, with higher percentages commanding faster fan rotation.

Table B may be used under specific conditions such as A/C operation or different vehicle speed ranges. Multiple fan speed tables (A, B, C) allow the ECU to optimize cooling fan behavior across different operating scenarios.

## Axes

### X-Axis

- **Parameter**: Sensors - Coolant Temperature
- **Unit**: CELSIUS
- **Range**: 93.9990 to 101.9995
- **Points**: 9

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |    93.9990 |    95.0000 |    96.0010 |    96.9995 |    98.0005 |    98.9990 |   100.0000 |   101.0010 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using coolant temperature:

1. **Temperature Reading**: ECU monitors coolant temperature sensor
2. **Condition Check**: ECU determines if Table B conditions are active
3. **Table Lookup**: Interpolates between temperature breakpoints for duty cycle
4. **PWM Output**: Duty cycle commands fan motor speed

Higher temperature = higher duty cycle = faster fan speed. The table spans 94-102°C, the critical range for cooling decisions.

## Related Tables

- **Engine - Radiator - Fan Speed Target A/C**: Other fan speed tables
- **Engine - Radiator - Fan 1/2 - Coolant Threshold A-E**: Activation thresholds

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input for table lookup
- **Radiator Fan Duty (%)**: Output from this table
- **Radiator Fan Status**: On/Off state
- **Vehicle Speed**: May affect table selection

## Tuning Notes

**Common Modifications:**
- Increase duty at lower temperatures for more aggressive cooling
- Raise maximum duty for improved high-temp cooling
- Smooth curve for quieter fan operation

**Considerations:**
- Higher duty = more noise and electrical load
- Coordinate changes across A, B, and C tables
- Consider fan motor limitations (continuous 100% may reduce lifespan)

## Warnings

- Insufficient fan speed at high temps risks overheating
- Excessive fan speed increases noise and wear
- Ensure electrical system can handle sustained high duty cycles
- Test in hot conditions to verify adequate cooling

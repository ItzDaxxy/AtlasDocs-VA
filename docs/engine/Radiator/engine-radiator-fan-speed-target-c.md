# Engine - Radiator - Fan Speed Target C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Engine - Radiator - Fan Speed Target C - 2018 - LF9C102P.csv` |

## Description

Defines the target fan speed (PWM duty cycle) based on coolant temperature for operating condition C. This table provides progressive fan speed control for specific operating scenarios. The PWM signal modulates fan motor speed, with higher duty cycles commanding faster rotation.

Table C may correspond to conditions such as idle operation, post-drive key-off cooling, or specific A/C states. Multiple fan speed tables allow optimized cooling behavior across different driving and environmental conditions.

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
2. **Condition Check**: ECU determines if Table C conditions are active
3. **Table Lookup**: Interpolates between temperature breakpoints
4. **PWM Output**: Commands fan motor speed via duty cycle

The table covers 94-102°C, providing fine control through the critical cooling temperature range.

## Related Tables

- **Engine - Radiator - Fan Speed Target A/B**: Other fan speed tables
- **Engine - Radiator - Fan 1/2 - Coolant Threshold A-E**: Activation thresholds

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **Radiator Fan Duty (%)**: Output duty cycle
- **Radiator Fan Status**: On/Off state
- **Vehicle Speed**: May affect table selection

## Tuning Notes

**Common Modifications:**
- Adjust curve shape for desired cooling response
- Coordinate with Tables A and B for consistent behavior
- Consider condition-specific requirements (idle vs driving)

**Considerations:**
- Changes should maintain cooling capability
- Higher duty cycles increase power draw
- Test across operating conditions this table affects

## Warnings

- Insufficient cooling risks engine damage
- Excessive duty causes unnecessary noise and wear
- Verify adequate cooling in all conditions after changes

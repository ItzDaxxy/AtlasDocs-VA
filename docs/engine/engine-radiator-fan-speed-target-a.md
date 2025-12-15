# Engine - Radiator - Fan Speed Target A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Engine - Radiator - Fan Speed Target A - 2018 - LF9C102P.csv` |

## Description

Defines the PWM duty cycle (fan speed) for the radiator fan based on coolant temperature. This table controls how fast the fan spins at various temperatures, allowing for variable-speed operation instead of simple on/off control.

The temperature range (94°C to 102°C) covers the transition from normal operating temperature to near-overheating, with fan speed increasing as temperature rises. This provides more efficient cooling - lower speeds at moderate temperatures reduce noise and power consumption, while higher speeds at elevated temperatures maximize cooling capacity.

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

The ECU performs 1D interpolation using coolant temperature to determine PWM duty cycle:

1. **Temperature Reading**: ECU reads coolant temperature from ECT sensor
2. **Table Lookup**: Interpolates between temperature breakpoints (94-102°C)
3. **PWM Output**: Generates PWM signal at calculated duty cycle
4. **Fan Response**: Fan motor speed proportional to duty cycle (0% = off, 100% = full speed)

Typical progression:
- ~94°C: Low speed (~30-40% duty)
- ~97°C: Medium speed (~50-60% duty)
- ~100°C: High speed (~80-90% duty)
- ~102°C: Maximum speed (100% duty)

## Related Tables

- **Engine - Radiator - Fan Speed Target B/C**: Alternate speed tables for different conditions
- **Engine - Radiator - Fan 1/2 Coolant Threshold A-E**: On/off activation thresholds
- **Sensors - Coolant Temperature**: Temperature input calibration

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **Radiator Fan Duty (%)**: Output from this table
- **Radiator Fan Status**: On/off state
- **Vehicle Speed**: May affect fan control strategy

## Tuning Notes

**Common Modifications:**
- Increase low-temp speeds for more aggressive cooling (track use)
- Decrease low-temp speeds to reduce fan noise (street use)
- Steepen curve for faster response to temperature rise

**Aftermarket Fan Considerations:**
- High-flow fans may need lower duty cycles for same cooling
- PWM compatibility varies - verify fan supports variable speed control
- Consider fan motor current draw at high duty cycles

## Warnings

- Setting duty too low at high temperatures risks overheating
- Maximum duty at all temperatures wastes power and increases noise
- Ensure fan is PWM-compatible before modifying
- Test cooling performance after modifications with temperature logging
- Some aftermarket fans may not respond linearly to PWM duty changes

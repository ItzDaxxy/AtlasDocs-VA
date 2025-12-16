# Engine - Radiator - Fan 1 - Coolant Threshold C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 1 - Coolant Threshold C - 2018 - LF9C102P.csv` |

## Value

**95.0000 CELSIUS**

## Description

Defines a coolant temperature threshold for radiator fan control. This threshold is part of the fan control hysteresis system that determines when the fan activates or changes speed. At 95°C, this value works with other thresholds (A, B, D, E) to create a multi-stage fan control strategy.

The multiple threshold values allow the ECU to implement smooth fan operation without constant on/off cycling, while also enabling variable fan speeds based on cooling demand.

## Related Tables

- **Engine - Radiator - Fan 1 - Coolant Threshold A**: Primary activation threshold
- **Engine - Radiator - Fan 1 - Coolant Threshold B**: Secondary threshold
- **Engine - Radiator - Fan 1 - Coolant Threshold D**: Deactivation threshold (90°C)
- **Engine - Radiator - Fan 1 - Coolant Threshold E (Main)**: Main control threshold
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan Duty (%)**: Output PWM to fan motor
- **Radiator Fan Status**: On/Off state

## Tuning Notes

**Common Modifications:**
- Lower threshold for improved cooling with performance modifications
- Maintain relationship with other thresholds for proper hysteresis
- Consider A/C operation which may override these thresholds

**Considerations:**
- Lowering thresholds increases fan noise and electrical load
- Too aggressive cooling may impact engine warm-up
- Ensure adequate gap between activation/deactivation thresholds

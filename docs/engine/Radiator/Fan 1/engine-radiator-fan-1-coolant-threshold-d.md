# Engine - Radiator - Fan 1 - Coolant Threshold D

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 1 - Coolant Threshold D - 2018 - LF9C102P.csv` |

## Value

**90.0000 CELSIUS**

## Description

Defines a coolant temperature threshold for radiator fan deactivation. At 90°C, this threshold is lower than the activation thresholds (typically 95-98°C), creating hysteresis that prevents rapid fan cycling. When coolant temperature drops below this value, the fan may reduce speed or turn off.

The 5°C gap between activation (95°C) and deactivation (90°C) prevents the fan from rapidly cycling on and off as temperature fluctuates around a single setpoint.

## Related Tables

- **Engine - Radiator - Fan 1 - Coolant Threshold A**: Primary activation threshold (95°C)
- **Engine - Radiator - Fan 1 - Coolant Threshold B**: Secondary threshold (98°C)
- **Engine - Radiator - Fan 1 - Coolant Threshold C**: Additional threshold (95°C)
- **Engine - Radiator - Fan 1 - Coolant Threshold E (Main)**: Main control threshold
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan Duty (%)**: Output PWM to fan motor
- **Radiator Fan Status**: On/Off state

## Tuning Notes

**Common Modifications:**
- Lower for more aggressive cooling (e.g., 85°C)
- Maintain minimum 3-5°C gap below activation threshold
- Consider impact on engine warm-up time

**Considerations:**
- Too close to activation threshold causes rapid cycling
- Too low extends fan run time unnecessarily
- Adjust proportionally with activation thresholds

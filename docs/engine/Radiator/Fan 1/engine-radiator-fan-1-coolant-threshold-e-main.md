# Engine - Radiator - Fan 1 - Coolant Threshold E (Main)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 1 - Coolant Threshold E (Main) - 2018 - LF9C102P.csv` |

## Value

**95.0000 CELSIUS**

## Description

Defines the main coolant temperature threshold for radiator fan activation. At 95°C, this is the primary trigger point for fan operation under normal driving conditions. This threshold represents the balance between maintaining optimal engine operating temperature and preventing overheating.

The "Main" designation indicates this is the primary threshold used during typical driving, with other thresholds (A, B, C, D) providing additional control points for hysteresis and multi-speed operation.

## Related Tables

- **Engine - Radiator - Fan 1 - Coolant Threshold A/B/C/D**: Supporting thresholds for hysteresis
- **Engine - Radiator - Fan 2 - Coolant Threshold E (Main)**: Secondary fan main threshold
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan Duty (%)**: Output PWM to fan motor
- **Radiator Fan Status**: On/Off state
- **A/C Request**: May override cooling fan thresholds

## Tuning Notes

**Common Modifications:**
- Lower to 90-93°C for track use or performance modifications
- Lower if experiencing heat soak issues during aggressive driving
- Consider intercooler/radiator upgrades before significant changes

**Considerations:**
- Stock 95°C maintains optimal combustion chamber temperatures
- Lower values increase fan wear and electrical load
- Ensure cooling system can handle increased fan demand
- A/C operation typically forces fan on regardless of coolant temp

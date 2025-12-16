# Engine - Radiator - Fan 2 - Coolant Threshold E (Main)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 2 - Coolant Threshold E (Main) - 2018 - LF9C102P.csv` |

## Value

**100.0000 CELSIUS**

## Description

Defines the main coolant temperature threshold for secondary fan (Fan 2) activation. At 100°C, this is the primary trigger point for engaging additional cooling capacity. The "Main" designation indicates this is the primary threshold for Fan 2 operation during normal driving conditions.

Fan 2 activates 5°C above Fan 1's main threshold (95°C), creating a two-stage cooling strategy. If Fan 1 alone cannot maintain temperatures below 100°C, Fan 2 engages to provide supplemental airflow.

## Related Tables

- **Engine - Radiator - Fan 2 - Coolant Threshold A/B/C**: Supporting Fan 2 thresholds
- **Engine - Radiator - Fan 1 - Coolant Threshold E (Main)**: Primary fan main threshold (95°C)
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan 1/2 Duty (%)**: Both fan PWM outputs
- **Radiator Fan 1/2 Status**: On/Off states
- **A/C Request**: May force both fans on

## Tuning Notes

**Common Modifications:**
- Lower to 95-97°C for track use or performance builds
- Match or slightly exceed Fan 1 thresholds for staged cooling
- Lower in hot climates or for high-power builds

**Considerations:**
- Stock 100°C allows Fan 1 to handle most cooling needs
- Lower values increase electrical load from dual fan operation
- Frequently reaching 100°C may indicate cooling system limitations
- Consider radiator/fan upgrades if consistently using Fan 2

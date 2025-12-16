# Engine - Radiator - Fan 2 - Coolant Threshold A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 2 - Coolant Threshold A - 2018 - LF9C102P.csv` |

## Value

**100.0000 CELSIUS**

## Description

Defines the primary coolant temperature threshold for activating the secondary radiator fan (Fan 2). At 100°C, this threshold is higher than Fan 1 thresholds, indicating Fan 2 serves as a high-demand cooling supplement that activates when Fan 1 alone cannot maintain adequate cooling.

Fan 2 typically provides additional airflow when the primary fan cannot keep up with cooling demands, such as during hot ambient temperatures, traffic/idle conditions, or after aggressive driving.

## Related Tables

- **Engine - Radiator - Fan 2 - Coolant Threshold B/C/E**: Other Fan 2 thresholds for hysteresis
- **Engine - Radiator - Fan 1 - Coolant Threshold A-E**: Primary fan thresholds (lower temps)
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan 2 Duty (%)**: Secondary fan PWM output
- **Radiator Fan 2 Status**: On/Off state

## Tuning Notes

**Common Modifications:**
- Lower to 95-98°C for earlier secondary fan activation
- Particularly useful for track driving or hot climates
- Consider upgrading to high-flow fans if frequently reaching these temps

**Considerations:**
- Running both fans increases electrical load significantly
- Frequently hitting 100°C may indicate cooling system issues
- Maintain gap above Fan 1 thresholds for staged cooling

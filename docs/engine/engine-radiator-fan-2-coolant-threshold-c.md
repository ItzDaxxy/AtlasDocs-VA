# Engine - Radiator - Fan 2 - Coolant Threshold C

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 2 - Coolant Threshold C - 2018 - LF9C102P.csv` |

## Value

**100.0000 CELSIUS**

## Description

Defines an additional threshold for Fan 2 control at 100°C. This threshold works with other Fan 2 thresholds (A, B, E) to provide hysteresis and multi-stage control for the secondary cooling fan.

At 100°C, this matches Threshold A, providing a secondary trigger point for the Fan 2 control logic under different operating conditions.

## Related Tables

- **Engine - Radiator - Fan 2 - Coolant Threshold A/B/E**: Other Fan 2 thresholds
- **Engine - Radiator - Fan 1 - Coolant Threshold A-E**: Primary fan thresholds
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan 2 Duty (%)**: Secondary fan PWM output
- **Radiator Fan 2 Status**: On/Off state

## Tuning Notes

**Common Modifications:**
- Lower proportionally with other Fan 2 thresholds
- Maintain relationship with A and B thresholds for proper hysteresis
- Consider impact on fan cycling behavior

**Considerations:**
- Changes should be coordinated across all Fan 2 thresholds
- Lower values increase fan usage but improve cooling response
- Ensure alternator and electrical system can handle dual fan load

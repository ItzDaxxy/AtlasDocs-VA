# Engine - Radiator - Fan 2 - Coolant Threshold B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 2 - Coolant Threshold B - 2018 - LF9C102P.csv` |

## Value

**101.0010 CELSIUS**

## Description

Defines a secondary threshold for Fan 2 control at 101°C. This is the highest temperature threshold in the fan control system, representing maximum cooling demand. Above this temperature, both fans should be operating at maximum capacity.

The 101°C threshold serves as an elevated trigger point within the Fan 2 hysteresis system, potentially commanding higher fan speed or ensuring both fans are at maximum duty cycle.

## Related Tables

- **Engine - Radiator - Fan 2 - Coolant Threshold A/C/E**: Other Fan 2 thresholds
- **Engine - Radiator - Fan 1 - Coolant Threshold A-E**: Primary fan thresholds
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM duty cycle tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Input for threshold comparison
- **Radiator Fan 2 Duty (%)**: Secondary fan PWM output
- **Radiator Fan 2 Status**: On/Off state

## Tuning Notes

**Common Modifications:**
- Lower to 98-99°C for earlier maximum cooling activation
- Critical threshold for track/performance applications
- Consider this an emergency cooling trigger point

**Considerations:**
- Reaching 101°C regularly indicates insufficient cooling capacity
- May require cooling system upgrades (radiator, fans, shroud)
- Monitor for overheating issues if frequently exceeding this temp

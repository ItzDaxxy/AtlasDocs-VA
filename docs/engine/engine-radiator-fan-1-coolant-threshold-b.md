# Engine - Radiator - Fan 1 - Coolant Threshold B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 1 - Coolant Threshold B - 2018 - LF9C102P.csv` |

## Value

**98.0005 CELSIUS**

## Description

Defines an alternate coolant temperature threshold (98°C) for Radiator Fan 1 activation in operating condition B. Multiple threshold values (A through E) allow the ECU to implement staged or conditional fan control based on factors like A/C status, vehicle speed, or load.

Threshold B at 98°C is higher than Threshold A (95°C), suggesting this may be used for conditions where aggressive cooling is less critical or to implement hysteresis (fan turns on at 98°C, turns off at 95°C) to prevent rapid cycling.

## Related Tables

- **Engine - Radiator - Fan 1 - Coolant Threshold A/C/D/E**: Other activation thresholds
- **Engine - Radiator - Fan 2 - Coolant Threshold A-E**: Second fan thresholds
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM speed control tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Primary input compared against threshold
- **Radiator Fan 1 Status**: On/off state
- **Vehicle Speed**: May affect which threshold is used
- **A/C Request**: May affect threshold selection

## Tuning Notes

**Purpose of Multiple Thresholds:**
- Implements hysteresis to prevent rapid on/off cycling
- Provides different activation points for different operating conditions
- Allows staged cooling (lower threshold for A/C on, higher for A/C off)

**Modifications:**
- Maintain 2-3°C gap between thresholds for effective hysteresis
- Lower all thresholds proportionally for track use
- Coordinate with Fan 2 thresholds for proper staged cooling

## Warnings

- Setting too high risks overheating between threshold A and B
- Ensure logical relationship between thresholds (B > A for typical hysteresis)
- Monitor coolant temps to verify cooling system adequacy
- Do not create large gaps between thresholds without testing

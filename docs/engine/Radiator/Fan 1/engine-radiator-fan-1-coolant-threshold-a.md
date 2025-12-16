# Engine - Radiator - Fan 1 - Coolant Threshold A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Engine - Radiator - Fan 1 - Coolant Threshold A - 2018 - LF9C102P.csv` |

## Value

**95.0000 CELSIUS**

## Description

Defines the coolant temperature threshold at which Radiator Fan 1 activates in operating condition A. The VA WRX uses multiple threshold values (A through E) that may apply to different operating scenarios such as A/C on/off, vehicle speed, and engine load conditions.

At 95°C, this represents a typical activation temperature for auxiliary cooling when the engine is at or approaching its upper normal operating range. This helps prevent overheating while avoiding unnecessary fan operation at lower temperatures.

Fan 1 is typically the primary (or low-speed) radiator fan. The ECU compares coolant temperature against this threshold to determine when to energize the fan relay.

## Related Tables

- **Engine - Radiator - Fan 1 - Coolant Threshold B/C/D/E**: Alternate thresholds for different conditions
- **Engine - Radiator - Fan 2 - Coolant Threshold A-E**: Second fan activation thresholds
- **Engine - Radiator - Fan Speed Target A/B/C**: PWM fan speed control tables

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Primary input compared against threshold
- **Radiator Fan 1 Status**: On/off state of fan relay
- **Radiator Fan 2 Status**: On/off state of second fan
- **A/C Request**: May affect which threshold is used
- **Vehicle Speed**: May affect fan control strategy

## Tuning Notes

**When to Modify:**
- Aftermarket radiator with improved cooling (can raise threshold slightly)
- Track use where aggressive cooling is needed (lower threshold)
- Living in hot climate (lower threshold for earlier activation)
- High-efficiency electric fans with better airflow (can raise threshold)

**Typical Modifications:**
- Lower 5-10°C for earlier cooling during spirited driving
- Coordinate with Fan 2 thresholds for staged cooling
- Match fan activation to thermostat opening temperature

**Do NOT:**
- Raise above 100°C unless you have verified cooling capacity
- Lower below 85°C (excessive fan cycling, fuel waste)
- Modify without considering related threshold tables

## Warnings

- Setting too high risks overheating and potential engine damage
- Setting too low causes excessive fan cycling and reduced fuel economy
- Ensure threshold is above normal operating temperature (~88-92°C) to prevent constant operation
- Track/race applications should use lower thresholds than street driving
- Monitor coolant temps after modification to verify adequate cooling

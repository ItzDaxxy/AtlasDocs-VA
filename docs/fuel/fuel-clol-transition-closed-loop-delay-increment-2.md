# Fuel - CL/OL Transition - Closed Loop Delay Increment 2

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - Closed Loop Delay Increment 2 - 2018 - LF9C102P.csv` |

## Value

**1.0000 NONE**

## Description

This scalar defines the second delay increment in the multi-stage delay system for transitioning from open-loop to closed-loop fuel control. It works in conjunction with Delay Increment 1 and 3 to create a staged delay before the ECU begins using O2 sensor feedback.

**Purpose:**
- Part of multi-stage delay preventing rapid CL/OL oscillation
- Allows progressive transition to closed-loop operation
- Provides additional time for O2 sensor stabilization

**Value Interpretation:**
- Value of 1.0 represents the base delay unit
- Higher values increase delay duration
- Combined with Increments 1 and 3 for total delay calculation

## Related Tables

- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 1](./fuel-clol-transition-closed-loop-delay-increment-1.md)**: First delay increment
- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 3](./fuel-clol-transition-closed-loop-delay-increment-3.md)**: Third delay increment
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Targets used after closed-loop entry

## Related Datalog Parameters

- **Fuel Mode**: Monitor open-loop to closed-loop transitions
- **AF Correction STFT (%)**: Observe when fuel trims activate
- **Coolant Temperature**: Affects delay conditions
- **O2 Sensor Voltage**: Verify sensor is ready before CL entry

## Tuning Notes

**Stock Behavior:** Stock value of 1.0 calibrated with other delay increments for smooth CL entry.

**Common Modifications:**
- Generally left at stock unless specific transition issues occur
- Modify proportionally with other delay increments

**Validation:** Monitor Fuel Mode and STFT after CL entry. Erratic trims indicate insufficient delay.

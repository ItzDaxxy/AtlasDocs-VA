# Fuel - CL/OL Transition - Closed Loop Delay Increment 1

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - Closed Loop Delay Increment 1 - 2018 - LF9C102P.csv` |

## Value

**1.0000 NONE**

## Description

This scalar defines the first delay increment used when transitioning from open-loop to closed-loop fuel control. After conditions are met to enter closed-loop mode, the ECU waits for a period determined by delay increment values before actually switching to closed-loop operation.

**Purpose:**
- Prevents rapid oscillation between open-loop and closed-loop modes
- Allows O2 sensors to stabilize before their feedback is trusted
- Provides smooth transition by gradually introducing closed-loop correction

**Value Interpretation:**
- Value of 1.0 represents the base delay unit (in ECU cycles or time units)
- Higher values increase the delay before closed-loop engagement
- Works in conjunction with Delay Increment 2 and 3 for multi-stage delay logic

## Related Tables

- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 2](./fuel-clol-transition-closed-loop-delay-increment-2.md)**: Second delay increment in multi-stage delay
- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 3](./fuel-clol-transition-closed-loop-delay-increment-3.md)**: Third delay increment in multi-stage delay
- **[Fuel - CL/OL Transition - CL Limits](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Load/RPM limits that trigger switch to open loop
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Closed-loop targets used after delay completes

## Related Datalog Parameters

- **Fuel Mode**: Shows current mode (open-loop vs closed-loop) - monitor transition timing
- **AF Correction STFT (%)**: Short-term fuel trim - observe when it becomes active after delay
- **Coolant Temperature**: Affects when closed-loop entry conditions are met
- **O2 Sensor Voltage/Lambda**: Verify sensors are providing valid readings before CL entry

## Tuning Notes

**Stock Behavior:** Stock value of 1.0 provides baseline delay timing calibrated for OEM sensors and conditions.

**Common Modifications:**
- **Cold Start Tuning**: Increasing delay can improve cold start stability by keeping ECU in open-loop longer
- **Quick CL Entry**: Decreasing values (not recommended) speeds up CL entry, potentially before sensors stabilize

**Recommended Approach:**
1. Generally leave at stock unless experiencing specific transition issues
2. If modifying, change all three delay increments proportionally
3. Log fuel trims immediately after CL entry to verify smooth transition

**Validation:** Monitor Fuel Mode transitions and STFT behavior. Erratic STFT immediately after CL entry may indicate delay is too short.

**Warning:** Reducing delay values can cause unstable fuel control if O2 sensors haven't reached operating temperature.

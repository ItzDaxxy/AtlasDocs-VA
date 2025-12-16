# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Coolant Temperature - Coolant Temperature Offset (Negative)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Coolant Temperature - Coolant Temperature Offset (Negative) - 2018 - LF9C102P.csv` |

## Value

**50.0000 NONE**

## Description

This scalar defines a negative offset applied to the coolant temperature threshold for closed-loop transition. It creates a hysteresis band or adjustment factor for coolant temperature-based CL/OL switching.

**Purpose:**
- Modifies coolant temperature threshold calculation
- May create hysteresis to prevent mode cycling
- Adjusts CL entry/exit point based on temperature

**Value Interpretation:**
- Value of 50.0 represents a 50°C offset (subtracted from threshold)
- Used to calculate effective temperature threshold
- Higher values = larger adjustment to base threshold

**Operating Logic:**
This offset is typically subtracted from a base coolant temperature threshold. For example, if the base threshold is 70°C and offset is 50°C, effective entry threshold might be 70-50=20°C, or this may be used for return-to-CL calculation after exiting to OL.

## Related Tables

- **[Fuel - CL/OL Transition - Coolant Temperature Minimum](./fuel-clol-transition-cl-limits-switch-to-open-loop-coolant-temperature-coolant-temperature-minimum.md)**: Base coolant temp threshold
- **[Fuel - CL/OL Transition - Catalyst Temp Hysteresis](./fuel-clol-transition-catalyst-temp-hysteresis-switch-to-open-loop.md)**: Similar hysteresis concept for catalyst temp
- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 1](./fuel-clol-transition-closed-loop-delay-increment-1.md)**: Time-based delay component

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Primary input for threshold comparison
- **Fuel Mode**: Observe CL/OL state changes relative to coolant temp
- **AF Correction STFT (%)**: Verify stable trims when CL enabled
- **Engine Runtime**: Correlate with warm-up progression

## Tuning Notes

**Stock Behavior:** Stock value of 50.0 provides significant offset, suggesting it's used to calculate an effective threshold or hysteresis band.

**Common Modifications:**
- Generally left at stock to maintain calibrated warm-up behavior
- Reducing offset may allow earlier CL entry during warm-up
- Increasing offset delays CL entry for more conservative operation

**Validation:** Monitor CL entry behavior during warm-up. Ensure no erratic trim oscillation when transitioning.

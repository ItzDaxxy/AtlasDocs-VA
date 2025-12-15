# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Coolant Temperature - Coolant Temperature Minimum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Coolant Temperature - Coolant Temperature Minimum - 2018 - LF9C102P.csv` |

## Value

**0.0000 NONE**

## Description

This scalar defines the minimum coolant temperature threshold for enabling closed-loop fuel control. Below this temperature, the ECU operates in open-loop mode because the engine and O2 sensors are not yet warm enough for reliable feedback control.

**Purpose:**
- Prevents closed-loop operation when engine is cold
- Ensures O2 sensors have reached operating temperature before trusting feedback
- Works with other CL enabling conditions (load, intake temp, etc.)

**Value Interpretation:**
- Value of 0.0 suggests no minimum threshold (other parameters may control this)
- Higher values = engine must be warmer before CL is allowed
- Typical minimum would be 40-60°C for O2 sensor accuracy

**Operating Logic:**
If coolant temperature is below this minimum, the ECU cannot enter closed-loop mode regardless of other conditions. This is one of several gates that must pass for CL entry.

## Related Tables

- **[Fuel - CL/OL Transition - Coolant Temperature Offset (Negative)](./fuel-clol-transition-cl-limits-switch-to-open-loop-coolant-temperature-coolant-temperature-offset-negative.md)**: Offset applied to coolant temp threshold
- **[Fuel - CL/OL Transition - Closed Loop Delay Increment 1](./fuel-clol-transition-closed-loop-delay-increment-1.md)**: Time-based delay for CL entry
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Lambda targets used in CL mode

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Compare to threshold to understand CL eligibility
- **Fuel Mode**: Verify CL enabled when coolant temp exceeds minimum
- **O2 Sensor Voltage**: Sensor accuracy depends on operating temperature
- **AF Correction STFT (%)**: Trims should be inactive until CL enabled

## Tuning Notes

**Stock Behavior:** Stock value of 0.0 suggests the minimum temperature threshold is controlled by other parameters or is effectively disabled.

**Common Modifications:**
- Generally left at stock unless experiencing CL issues during warm-up
- Setting a higher minimum can prevent erratic trims during cold operation
- Must balance with emissions requirements (faster CL entry = better emissions)

**Validation:** Monitor Fuel Mode and STFT activation during warm-up to verify CL entry timing is appropriate.

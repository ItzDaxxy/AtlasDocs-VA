# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Intake Temperature - Intake Temperature Offset (Negative)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Intake Temperature - Intake Temperature Offset (Negative) - 2018 - LF9C102P.csv` |

## Value

**50.0000 NONE**

## Description

This scalar defines a negative offset applied to the intake temperature maximum threshold for CL/OL switching. It adjusts the effective IAT threshold, potentially creating hysteresis or condition-based modification.

**Purpose:**
- Modifies the IAT Maximum threshold calculation
- May create hysteresis for IAT-based CL/OL switching
- Provides adjustment factor for effective threshold

**Value Interpretation:**
- Value of 50.0 represents 50°C offset
- With IAT Maximum at 255 and offset at 50, effective threshold would be 205°C
- Since 205°C is still unrealistic, this offset has no practical effect in stock calibration

**Operating Logic:**
Effective Threshold = IAT Maximum - Offset = 255 - 50 = 205°C. Since typical IAT values range from 20-80°C (or up to ~100°C in extreme heat soak), this threshold is never reached. The parameter exists for potential calibration use but is effectively disabled in stock tune.

## Related Tables

- **[Fuel - CL/OL Transition - Intake Temperature Maximum](./fuel-clol-transition-cl-limits-switch-to-open-loop-intake-temperature-intake-temperature-maximum.md)**: Base threshold this offset modifies
- **[Fuel - CL/OL Transition - Coolant Temperature Offset](./fuel-clol-transition-cl-limits-switch-to-open-loop-coolant-temperature-coolant-temperature-offset-negative.md)**: Similar concept for coolant temp
- **[Fuel - CL/OL Transition - Calculated Load Offset A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-offset-a-negative.md)**: Similar concept for load

## Related Datalog Parameters

- **Intake Air Temperature (°C)**: Primary input (typical range 20-80°C)
- **Fuel Mode**: CL/OL state (not affected by IAT in stock config)
- **Ambient Temperature**: Correlates with baseline IAT
- **Boost Pressure**: Higher boost = higher IAT after intercooler

## Tuning Notes

**Stock Behavior:** Stock value of 50.0 with IAT Maximum at 255 means this parameter has no practical effect - threshold is still unrealistically high.

**Common Modifications:**
- Only relevant if IAT Maximum is lowered significantly
- If IAT Max set to 70°C with 50°C offset, effective threshold would be 20°C (unrealistic)
- Most tuners focus on other CL limits rather than IAT

**Practical Application:** If enabling IAT-based OL switching, consider:
- Set IAT Maximum to ~80-90°C
- Set offset to ~10-20°C for hysteresis
- Effective entry: 80°C, effective exit: 60-70°C

**Validation:** Monitor IAT during operation to understand your actual operating range before modifying these thresholds.

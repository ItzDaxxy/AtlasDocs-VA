# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Offset A (Negative)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Offset A (Negative) - 2018 - LF9C102P.csv` |

## Value

**0.0000 NONE**

## Description

This scalar defines a negative offset applied to the Calculated Load Maximum A threshold. It adjusts the effective load threshold for CL/OL transition, typically creating hysteresis or condition-based modification.

**Purpose:**
- Modifies the Load Maximum A threshold calculation
- May create hysteresis for load-based CL/OL switching
- Provides adjustment factor for effective threshold

**Value Interpretation:**
- Value of 0.0 means no offset applied to threshold A
- Positive values would be subtracted from Load Maximum A
- With 0.0 offset, effective threshold equals Load Maximum A (226)

**Operating Logic:**
The effective load threshold may be calculated as: Effective Threshold = Load Maximum A - Offset A. With offset at 0.0, the effective threshold equals the base Load Maximum A value of 226.

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Base threshold this offset modifies
- **[Fuel - CL/OL Transition - Calculated Load Offset B](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-offset-b-negative.md)**: Companion offset for threshold B
- **[Fuel - CL/OL Transition - Catalyst Temp Hysteresis](./fuel-clol-transition-catalyst-temp-hysteresis-switch-to-open-loop.md)**: Similar offset concept

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to effective threshold
- **Fuel Mode**: Observe CL/OL switching behavior
- **Command Fuel Final (λ)**: Verify fueling matches expected mode
- **Boost Pressure**: Correlates with load values

## Tuning Notes

**Stock Behavior:** Stock value of 0.0 means no offset is applied, making Load Maximum A (226) the direct threshold.

**Common Modifications:**
- Adding offset would lower the effective OL entry threshold
- Could be used to create earlier OL entry under specific conditions
- Generally left at stock unless fine-tuning CL/OL boundaries

**Hysteresis Use:** If this offset is used for return-to-CL (hysteresis), load would need to drop to (226 - offset) before returning to CL. With 0.0 offset, no hysteresis band exists for this parameter.

**Validation:** Monitor load and fuel mode to verify OL triggers at expected threshold.

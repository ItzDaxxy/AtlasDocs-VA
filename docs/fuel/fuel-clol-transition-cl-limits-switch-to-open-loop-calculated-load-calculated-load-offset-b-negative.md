# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Offset B (Negative)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Offset B (Negative) - 2018 - LF9C102P.csv` |

## Value

**0.0000 NONE**

## Description

This scalar defines a negative offset applied to the Calculated Load Maximum B threshold. It adjusts the secondary load threshold for CL/OL transition, providing modification capability for the alternate load check.

**Purpose:**
- Modifies the Load Maximum B threshold calculation
- Creates potential hysteresis or condition-based adjustment
- Works with offset A for complete load threshold control

**Value Interpretation:**
- Value of 0.0 means no offset applied to threshold B
- With threshold B at 255 and offset at 0, effective threshold remains 255
- Since threshold B is already at maximum, this offset has minimal practical effect

**Operating Logic:**
Effective Threshold B = Load Maximum B - Offset B = 255 - 0 = 255. Since threshold B is effectively disabled (at max value), this offset doesn't materially affect operation.

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum B](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-b.md)**: Base threshold this offset modifies (255)
- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Primary operative threshold (226)
- **[Fuel - CL/OL Transition - Calculated Load Offset A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-offset-a-negative.md)**: Companion offset for threshold A

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to thresholds
- **Fuel Mode**: Observe CL/OL switching (primarily via threshold A)
- **Command Fuel Final (λ)**: Verify expected fueling behavior
- **Boost Pressure**: Correlates with calculated load values

## Tuning Notes

**Stock Behavior:** Stock value of 0.0 with threshold B at 255 means this parameter has no practical effect on stock calibration.

**Common Modifications:**
- Rarely modified since threshold B is at maximum
- Only relevant if Load Maximum B is lowered from 255
- Focus tuning efforts on threshold A and offset A instead

**Understanding the System:** The A/B threshold system with offsets allows complex condition-dependent load control. Stock calibration simplifies this by setting B to max, effectively using only threshold A.

**Validation:** Focus monitoring on threshold A behavior since threshold B is effectively disabled in stock calibration.

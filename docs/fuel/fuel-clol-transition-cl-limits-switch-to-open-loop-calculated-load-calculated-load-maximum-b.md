# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Maximum B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Maximum B - 2018 - LF9C102P.csv` |

## Value

**255.0000 NONE**

## Description

This scalar defines a secondary maximum calculated load threshold ("B") above which the ECU switches from closed-loop to open-loop fuel control. This higher threshold works with Load Maximum A for multi-stage or condition-dependent load-based switching.

**Purpose:**
- Provides a secondary/alternate load threshold for OL switching
- May be used under different operating conditions than threshold A
- Value of 255 represents maximum possible 8-bit value (effectively "always CL" for this condition)

**Value Interpretation:**
- Value of 255.0 represents ~2.55 g/rev calculated load threshold
- This is near or at the maximum representable value (8-bit max = 255)
- Effectively disables this particular threshold (very high load required)

**Operating Logic:**
The ECU may use threshold A or B depending on other operating conditions. With threshold B set to 255 (max value), this particular load check is effectively bypassed, meaning threshold A (226) is the primary load-based OL trigger.

**Load Reference:**
- 255 g/rev = ~2.55 g/rev calculated load
- This exceeds typical peak boost loads on stock turbo
- Effectively means "always pass this check"

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Primary load threshold (226)
- **[Fuel - CL/OL Transition - Calculated Load Offset B](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-offset-b-negative.md)**: Offset for this threshold
- **[Fuel - Power Enrichment - Hysteresis (Enriching)](./fuel-power-enrichment-hysteresis-enriching.md)**: Related enrichment trigger

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to threshold (unlikely to reach 255)
- **Fuel Mode**: Verify OL activation (primarily via threshold A)
- **Command Fuel Final (λ)**: Observe fueling behavior
- **Boost Pressure**: Correlates with calculated load

## Tuning Notes

**Stock Behavior:** Stock value of 255 effectively disables this threshold, making Load Maximum A the operative load-based CL limit.

**Common Modifications:**
- Rarely modified since it's already at maximum
- If lowered, would create a second load threshold for specific conditions
- Most tuners focus on Load Maximum A for load-based OL control

**Understanding A vs B:** The dual threshold system (A and B) likely applies under different conditions (e.g., different coolant temps, different TGV states). With B at max, the simpler threshold A controls load-based switching.

**Validation:** Log calculated load values to understand your actual operating range. Stock turbo rarely exceeds 2.2-2.4 g/rev at peak boost.

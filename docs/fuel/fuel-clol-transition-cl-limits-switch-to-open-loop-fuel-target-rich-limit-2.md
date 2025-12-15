# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Fuel Target - Rich Limit 2

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | LAMBDA |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Fuel Target - Rich Limit 2 - 2018 - LF9C102P.csv` |

## Value

**0.8000 LAMBDA**

## Description

This scalar defines a secondary rich lambda limit for CL/OL switching. It works with Rich Limit 1 to provide dual-threshold control, potentially for different operating conditions or as a hysteresis mechanism.

**Purpose:**
- Provides secondary rich limit threshold for CL/OL control
- May be used under different conditions than Rich Limit 1
- Both limits at 0.80λ suggests simplified single-threshold behavior

**Value Interpretation:**
- Value of 0.80 lambda = 11.76:1 AFR gasoline
- Matches Rich Limit 1 (no differentiation between thresholds)
- Both at same value effectively creates single-threshold behavior

**Operating Logic:**
With both Rich Limit 1 and Rich Limit 2 at 0.80λ, there is no distinction between them. The ECU uses 0.80λ as the single rich limit for CL/OL switching. Different values would enable condition-dependent thresholds.

**Potential Uses for Dual Thresholds:**
- Different limits for different TGV states
- Different limits for different coolant temperature ranges
- Hysteresis: enter OL at 0.80, return to CL at 0.85

## Related Tables

- **[Fuel - CL/OL Transition - Fuel Target Rich Limit 1](./fuel-clol-transition-cl-limits-switch-to-open-loop-fuel-target-rich-limit-1.md)**: Primary rich limit (also 0.80λ)
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: WOT lambda targets
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: CL lambda targets

## Related Datalog Parameters

- **Command Fuel Final (λ)**: Compare to threshold
- **Fuel Mode**: Observe CL/OL state
- **A/F Sensor 1 (λ)**: Actual measured AFR
- **TGV Position**: May correlate with which limit is used

## Tuning Notes

**Stock Behavior:** Stock value matches Rich Limit 1, providing unified behavior. Both thresholds trigger OL when commanded lambda drops below 0.80.

**Common Modifications:**
- Could set slightly higher than Limit 1 for return-to-CL hysteresis
- Example: Limit 1 = 0.80 (OL entry), Limit 2 = 0.85 (CL return)
- Prevents mode cycling during fluctuating lambda targets

**Creating Hysteresis:**
1. Set Rich Limit 1 to 0.78λ (trigger OL entry)
2. Set Rich Limit 2 to 0.85λ (allow CL return)
3. Creates dead band where mode doesn't change

**Validation:** If experiencing fuel mode cycling during part-throttle operation with borderline lambda targets, consider separating these thresholds to add hysteresis.

# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Fuel Target - Rich Limit 1

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | LAMBDA |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Fuel Target - Rich Limit 1 - 2018 - LF9C102P.csv` |

## Value

**0.8000 LAMBDA**

## Description

This scalar defines a rich lambda limit that determines when the ECU should switch from closed-loop to open-loop fuel control. When the commanded fuel target becomes richer than this threshold, closed-loop operation is inappropriate and the ECU switches to open-loop.

**Purpose:**
- Prevents closed-loop operation when enrichment is required
- Triggers OL mode when fuel target is below stoichiometric (λ < 1.0)
- Ensures O2 sensor feedback is disabled during intentional rich operation

**Value Interpretation:**
- Value of 0.80 lambda = 11.76:1 AFR gasoline
- When commanded lambda drops below 0.80, ECU exits closed-loop
- This is a significant enrichment (20% richer than stoichiometric)

**Operating Logic:**
Closed-loop fuel control aims for stoichiometric (λ = 1.0). When enrichment is needed (power enrichment, catalyst protection), targets go rich (λ < 1.0). This threshold tells the ECU "if we need to be richer than 0.80λ, don't use O2 feedback."

**Lambda Reference:**
- λ = 1.0: Stoichiometric (14.7:1 AFR gasoline)
- λ = 0.90: Slightly rich (13.2:1)
- λ = 0.80: Rich for WOT power (11.76:1)
- λ = 0.75: Aggressive enrichment (11.0:1)

## Related Tables

- **[Fuel - CL/OL Transition - Fuel Target Rich Limit 2](./fuel-clol-transition-cl-limits-switch-to-open-loop-fuel-target-rich-limit-2.md)**: Secondary rich limit threshold
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: WOT lambda targets (typically 0.78-0.82)
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: CL lambda targets (typically 1.0)

## Related Datalog Parameters

- **Command Fuel Final (λ)**: Compare to threshold to understand mode switching
- **Fuel Mode**: Verify OL active when target is below 0.80λ
- **A/F Sensor 1 (λ)**: Actual measured lambda
- **Calculated Load (g/rev)**: Correlates with enrichment targets

## Tuning Notes

**Stock Behavior:** Stock threshold of 0.80λ aligns with typical WOT enrichment targets (~0.78-0.82λ), ensuring CL is disabled during power enrichment.

**Common Modifications:**
- **Lower Threshold (0.75-0.78)**: Allows CL operation with mild enrichment
- **Higher Threshold (0.85-0.90)**: Earlier OL entry, more conservative
- Generally left at stock unless experiencing CL/OL transition issues

**Interaction with Power Enrichment:** If Power Enrichment Target is 0.78λ and this limit is 0.80λ, the ECU switches to OL when power enrichment activates - which is correct behavior.

**Warning:** Setting this threshold leaner than your power enrichment targets would cause conflicting behavior (trying to use CL feedback while commanding rich).

**Validation:** Log Command Fuel Final and Fuel Mode during WOT. Verify OL activates when lambda target drops below this threshold.

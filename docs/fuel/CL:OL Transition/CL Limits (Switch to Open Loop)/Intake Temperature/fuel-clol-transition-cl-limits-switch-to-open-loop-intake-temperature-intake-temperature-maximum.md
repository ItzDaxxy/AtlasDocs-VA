# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Intake Temperature - Intake Temperature Maximum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Intake Temperature - Intake Temperature Maximum - 2018 - LF9C102P.csv` |

## Value

**255.0000 NONE**

## Description

This scalar defines the maximum intake air temperature threshold above which the ECU switches from closed-loop to open-loop fuel control. High IAT conditions may require enrichment for safe operation, as hot intake air increases knock risk.

**Purpose:**
- Triggers OL mode when intake air is dangerously hot
- Protects engine from lean operation during high-IAT conditions
- Works with other CL limits (load, coolant temp, etc.)

**Value Interpretation:**
- Value of 255.0 represents maximum possible threshold (~255°C scaled)
- Effectively disables IAT-based OL switching (no realistic IAT reaches 255°C)
- Stock calibration relies on other parameters for CL/OL control

**Operating Logic:**
With threshold set to 255 (max value), this parameter is effectively disabled. The ECU uses other criteria (load, catalyst temp, fuel target) for CL/OL switching rather than IAT.

## Related Tables

- **[Fuel - CL/OL Transition - Intake Temperature Offset (Negative)](./fuel-clol-transition-cl-limits-switch-to-open-loop-intake-temperature-intake-temperature-offset-negative.md)**: Offset for this threshold
- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Primary operative CL limit
- **[Fuel - Power Enrichment - Hysteresis (Enriching)](./fuel-power-enrichment-hysteresis-enriching.md)**: Load-based enrichment entry

## Related Datalog Parameters

- **Intake Air Temperature (°C)**: Compare to threshold (won't reach 255°C)
- **Fuel Mode**: CL/OL state (not affected by IAT at stock settings)
- **Calculated Load (g/rev)**: Primary CL/OL trigger in stock calibration
- **Command Fuel Final (λ)**: Observe fueling targets

## Tuning Notes

**Stock Behavior:** Stock value of 255 effectively disables IAT-based OL switching, allowing the ECU to stay in closed-loop regardless of intake temperature.

**Common Modifications:**
- Could lower to ~60-80°C to trigger OL (enrichment) during extreme heat soak
- Useful for intercooler failure protection or track use in hot climates
- Most tuners leave at stock since load-based switching handles most scenarios

**When to Modify:**
- Extended track sessions with inadequate intercooler
- Operating in extreme ambient temperatures
- As additional safety layer for heat-soak conditions

**Validation:** Monitor IAT during hot operation. If experiencing knock during heat soak, consider adding IAT-based OL trigger.

# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Maximum A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Calculated Load - Calculated Load Maximum A - 2018 - LF9C102P.csv` |

## Value

**226.0000 NONE**

## Description

This scalar defines a maximum calculated load threshold (primary limit "A") above which the ECU switches from closed-loop to open-loop fuel control. High load conditions require enrichment beyond stoichiometric, making O2 sensor feedback inappropriate.

**Purpose:**
- Triggers OL mode when load exceeds capacity for CL stoichiometric targets
- Ensures enrichment is active during high-load conditions
- Works with Load Maximum B for multi-threshold load-based switching

**Value Interpretation:**
- Value of 226.0 represents ~2.26 g/rev calculated load threshold
- When calculated load exceeds 2.26 g/rev, ECU switches to OL
- This is a relatively high threshold (moderate-to-high boost)

**Operating Logic:**
Calculated Load = (MAF × 120) / RPM in g/rev. At 226% load threshold (~2.26 g/rev), this typically represents moderate boost conditions. The ECU uses this threshold to determine when enrichment (open-loop) is needed.

**Load Reference:**
- ~100 g/rev = naturally aspirated WOT
- ~150-180 g/rev = moderate boost
- ~200-250 g/rev = significant boost
- 226 g/rev threshold triggers OL during boosted operation

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum B](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-b.md)**: Secondary load threshold (255)
- **[Fuel - CL/OL Transition - Calculated Load Offset A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-offset-a-negative.md)**: Offset for this threshold
- **[Fuel - Power Enrichment - Hysteresis (Enriching)](./fuel-power-enrichment-hysteresis-enriching.md)**: Related load-based enrichment entry

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to threshold to understand OL triggering
- **Fuel Mode**: Verify OL activated when load exceeds threshold
- **Command Fuel Final (λ)**: Should show enrichment after OL switch
- **Boost Pressure**: Correlates with load; higher boost = higher load

## Tuning Notes

**Stock Behavior:** Stock threshold of 226 provides OL entry during moderate boost, ensuring enrichment before combustion temperatures become excessive.

**Common Modifications:**
- **Lower Threshold**: Earlier OL entry for more conservative (safer) tuning
- **Higher Threshold**: Extended CL operation for better emissions/economy (reduces safety margin)
- **Power Adders**: May need adjustment if peak load increases significantly

**Warning:** Setting threshold too high delays enrichment, risking lean conditions under boost. Always maintain margin below your actual peak load values.

**Validation:** Log calculated load during WOT pulls. Verify OL activates before peak load is reached.

# Fuel - CL/OL Transition - Catalyst Temp Hysteresis (Switch to Open Loop)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `OL Transition - Catalyst Temp Hysteresis (Switch to Open Loop) - 2018 - LF9C102P.csv` |

## Value

**0.0000 CELSIUS**

## Description

This scalar defines the hysteresis value for catalyst temperature when switching between closed-loop and open-loop fuel modes. Hysteresis prevents rapid cycling between modes when catalyst temperature is near the switching threshold.

**Purpose:**
- Prevents oscillation between CL and OL modes near threshold
- Creates a "dead band" where mode doesn't change
- If OL activated at 598°C, may require dropping to (598 - hysteresis) to return to CL

**Value Interpretation:**
- Value of 0.0°C means no hysteresis (immediate switching at threshold)
- Higher values create larger dead band between switching points
- Stock value of 0°C may indicate this parameter is unused or handled elsewhere

**Operating Logic:**
Works with Catalyst Temp Maximum threshold. If catalyst temp exceeds max and triggers open-loop, temp must drop below (max - hysteresis) before returning to closed-loop.

## Related Tables

- **[Fuel - CL/OL Transition - Catalyst Temp Maximum](./fuel-clol-transition-catalyst-temp-maximum-switch-to-open-loop.md)**: Temperature threshold for OL switch
- **[Fuel - Power Enrichment - Catalyst Temp Trigger](./fuel-power-enrichment-catalyst-temp-trigger.md)**: Related catalyst protection enrichment

## Related Datalog Parameters

- **Catalyst Temperature (°C)**: Monitor approach to and retreat from threshold
- **Fuel Mode**: Observe CL/OL switching behavior
- **Command Fuel Final (λ)**: See target changes during mode switches

## Tuning Notes

**Stock Behavior:** Stock value of 0°C suggests minimal hysteresis for catalyst temp-based switching.

**Common Modifications:**
- Adding hysteresis (5-10°C) can prevent rapid mode cycling during borderline conditions
- Generally left at stock unless experiencing oscillation issues

**Validation:** If Fuel Mode oscillates rapidly when catalyst temp is near threshold, consider adding hysteresis.

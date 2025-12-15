# Fuel - CL/OL Transition - Catalyst Temp Maximum (Switch to Open Loop)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `OL Transition - Catalyst Temp Maximum (Switch to Open Loop) - 2018 - LF9C102P.csv` |

## Value

**597.6776 CELSIUS**

## Description

This scalar defines the maximum catalyst temperature threshold that triggers a switch from closed-loop to open-loop fuel control. When estimated catalyst temperature exceeds ~598°C, the ECU switches to open-loop mode with enriched fueling to protect the catalytic converter.

**Purpose:**
- Protects catalyst from thermal damage by triggering enrichment
- Switches to open-loop (no O2 feedback) to allow richer AFR
- Safety mechanism for sustained high-load operation

**Value Interpretation:**
- Threshold of ~598°C provides margin before catalyst damage (~750-850°C)
- When exceeded, ECU abandons closed-loop stoichiometric targets
- Open-loop operation typically runs richer for cooling effect

**Operating Logic:**
This is a different mechanism than Power Enrichment - this controls CL/OL mode switching based on catalyst temp, while Power Enrichment controls the actual AFR targets. Both work together for catalyst protection.

## Related Tables

- **[Fuel - CL/OL Transition - Catalyst Temp Hysteresis](./fuel-clol-transition-catalyst-temp-hysteresis-switch-to-open-loop.md)**: Hysteresis for this threshold
- **[Fuel - Power Enrichment - Catalyst Temp Trigger](./fuel-power-enrichment-catalyst-temp-trigger.md)**: Related enrichment trigger (600°C)
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: AFR targets during protection

## Related Datalog Parameters

- **Catalyst Temperature (°C)**: Monitor approach to threshold
- **Fuel Mode**: Verify switch to open-loop when threshold exceeded
- **Command Fuel Final (λ)**: Should show enrichment after OL switch
- **A/F Sensor 1 (λ)**: Actual AFR during protection mode

## Tuning Notes

**Stock Behavior:** Stock threshold of ~598°C is slightly below the Power Enrichment trigger (600°C), providing layered protection.

**Common Modifications:**
- **Catless/High-Flow**: May raise threshold if catalyst protection less critical
- **Track Use**: Some raise threshold, accepting increased catalyst wear

**Warning:** Raising this threshold significantly increases catalyst damage risk during sustained high-load operation. Only modify if running catless or high-flow cats with higher temp tolerance.

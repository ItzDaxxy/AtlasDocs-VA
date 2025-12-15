# Ignition - Dynamic Advance - DAM Initial Value

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Ignition - Dynamic Advance - DAM Initial Value - 2017 - RogueWRX.csv` |

## Value

**0.1250 NONE**

## Description

This scalar defines the initial value for the Dynamic Advance Multiplier (DAM) when the ECU initializes or recovers from significant knock events. DAM is a critical knock-learning parameter that scales the dynamic timing advance.

**Purpose:**
- Sets the starting point for DAM when ECU initializes
- Defines conservative initial timing until ECU learns fuel quality
- Provides knock-safe baseline for dynamic advance system

**Value Interpretation:**
- 0.125 = 12.5% of maximum dynamic advance available initially
- DAM operates on 0-1 scale (0 = no dynamic advance, 1 = full dynamic advance)
- Low initial value ensures conservative timing until ECU learns conditions
- DAM increases toward 1.0 as ECU confirms no knock, decreases when knock detected

**DAM Learning System:**
The Dynamic Advance Multiplier (DAM) is Subaru's knock-learning system:
- Starts at initial value (0.125) after ECU reset
- Increases slowly when no knock detected
- Decreases rapidly when knock detected
- Scales all dynamic timing advance by this multiplier

## Related Tables

- **[Ignition - Dynamic Advance - Base (TGV Open)](./ignition-dynamic-advance-base-tgv-open.md)**: Base dynamic advance values (scaled by DAM)
- **[Ignition - Dynamic Advance - Base (TGV Closed)](./ignition-dynamic-advance-base-tgv-closed.md)**: Base advance for TGV closed
- **[Ignition - Dynamic Advance - Base Multiplier](./ignition-dynamic-advance-base-multiplier.md)**: Converts DAM to actual multiplier
- **[Ignition - Dynamic Advance - Adder (TGV Open)](./ignition-dynamic-advance-adder-adder-tgv-open.md)**: Additional advance added to base

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Shows current DAM value (0-1 scale)
- **Fine Knock Learn**: Per-cylinder knock correction
- **Feedback Knock Correction**: Real-time knock retard
- **Ignition Timing**: Final actual timing

## Tuning Notes

**Stock Behavior:** Stock value of 0.125 is conservative, ensuring safe timing during ECU learning phase. DAM will increase to 1.0 over time with quality fuel and no knock.

**Interpreting DAM Values:**
- DAM = 1.0: ECU has learned conditions, full dynamic advance available
- DAM = 0.5-0.9: ECU partially learned, or mild knock history
- DAM < 0.5: Significant knock events detected, ECU limiting advance
- DAM stuck at initial (0.125): Persistent knock or recent ECU reset

**Common Modifications:**
- Generally left at stock - higher values risk knock at startup
- Could lower to 0.0625 for more conservative initial timing
- Raising initial value is not recommended

**DAM Recovery:**
After ECU reset or significant knock events, DAM resets to this initial value. Under normal driving with quality fuel, DAM should recover to 1.0 within a few drive cycles.

## Warnings

⚠️ **Knock Safety**: DAM exists to protect the engine. Low DAM indicates potential knock issues.

⚠️ **ECU Reset Impact**: Clearing ECU codes resets DAM to this initial value - timing will be conservative until relearned.

**Safe Practices:**
- Monitor DAM after ECU reset or fuel changes
- If DAM won't recover to 1.0, investigate knock causes (fuel quality, intake temps, tune)
- Don't raise initial value to mask knock problems

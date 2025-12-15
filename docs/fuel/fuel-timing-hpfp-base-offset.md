# Fuel - Timing - HPFP - Base Offset

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Base Offset - 2017 - RogueWRX.csv` |

## Value

**80.0000 DEGREES**

## Description

This scalar defines a global offset applied to all HPFP valve timing calculations. It shifts both open and close timing by a fixed amount to account for mechanical or sensor offsets.

**Purpose:**
- Provides global timing adjustment for HPFP operation
- Compensates for cam position sensor offset
- Allows fine-tuning of overall HPFP timing without modifying main tables

**Value Interpretation:**
- Value of 80° represents the base timing offset
- This offset is added to (or incorporated with) open/close timing calculations
- Adjusts effective timing relative to cam position reference

**Use Case:**
Global timing offset useful for:
- Compensating for cam sensor mounting variations
- Fine-tuning after cam timing modifications (AVCS changes)
- Adjusting for different HPFP hardware characteristics

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Base close timing
- **[Fuel - Timing - HPFP - Valve Open Base](./fuel-timing-hpfp-valve-open-base.md)**: Base open timing
- **[Fuel - Timing - HPFP - Valve Close Limit (IPW)](./fuel-timing-hpfp-valve-close-limit-ipw.md)**: Close timing limits

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Result of HPFP operation
- **HPFP Duty Cycle (%)**: Pump control effort
- **Cam Position**: Reference for timing calculations

## Tuning Notes

**Stock Behavior:** Stock offset of 80° calibrated for OEM hardware alignment.

**Common Modifications:**
- Rarely modified unless HPFP hardware changed
- May need adjustment if cam timing significantly altered
- Easier to adjust than modifying entire timing tables

**Adjustment Approach:**
If HPFP unable to build pressure or runs erratic:
1. Verify all timing tables are stock
2. Small offset adjustments (±5°) can help diagnose timing issues
3. Return to stock if adjustment doesn't resolve issue

**Warning:** This affects all HPFP timing. Small changes have global effect.

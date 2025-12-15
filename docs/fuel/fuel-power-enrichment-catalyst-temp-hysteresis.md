# Fuel - Power Enrichment - Catalyst Temp Hysteresis

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Fuel - Power Enrichment - Catalyst Temp Hysteresis - 2017 - RogueWRX.csv` |

## Value

**50.0125 CELSIUS**

## Description

This scalar defines the hysteresis value for catalyst temperature-based power enrichment activation. It creates a dead band that prevents rapid cycling between enrichment states when catalyst temperature is near the trigger threshold.

**Purpose:**
- Prevents rapid oscillation of power enrichment near catalyst temp trigger
- Creates stable transition between enrichment and non-enrichment states
- Ensures enrichment doesn't repeatedly enable/disable during borderline conditions

**Value Interpretation:**
- Value of ~50°C represents hysteresis band
- If enrichment activates at 600°C trigger, it won't deactivate until temp drops to ~550°C (600 - 50)
- Larger hysteresis = more stable behavior but slower response to cooling

**Operating Logic:**
Works with Catalyst Temp Trigger (typically 600°C):
1. Enrichment activates when catalyst temp exceeds trigger (600°C)
2. Enrichment remains active until temp drops below (trigger - hysteresis) = 550°C
3. This 50°C dead band prevents rapid mode cycling

**Example Scenario:**
- Trigger = 600°C, Hysteresis = 50°C
- At 605°C: Enrichment ON
- Temp drops to 590°C: Enrichment stays ON (still above 550°C)
- Temp drops to 545°C: Enrichment OFF
- Temp rises to 580°C: Enrichment stays OFF (still below 600°C)

## Related Tables

- **[Fuel - Power Enrichment - Catalyst Temp Trigger](./fuel-power-enrichment-catalyst-temp-trigger.md)**: Activation threshold (600°C)
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: Lambda targets during enrichment
- **[Fuel - CL/OL Transition - Catalyst Temp Hysteresis](./fuel-clol-transition-catalyst-temp-hysteresis-switch-to-open-loop.md)**: Similar concept for CL/OL switching

## Related Datalog Parameters

- **Catalyst Temperature (°C)**: Compare to trigger and hysteresis range
- **Command Fuel Final (λ)**: Observe enrichment activation/deactivation
- **Fuel Mode**: Correlates with enrichment state
- **A/F Sensor 1 (λ)**: Actual AFR during transitions

## Tuning Notes

**Stock Behavior:** Stock hysteresis of ~50°C provides substantial dead band, ensuring stable enrichment behavior during typical temperature fluctuations.

**Common Modifications:**
- **Smaller Hysteresis (25-40°C)**: Faster response to catalyst cooling, but may cycle more
- **Larger Hysteresis (60-80°C)**: Very stable, but enrichment stays active longer than necessary
- Generally left at stock unless experiencing specific cycling issues

**Catless/High-Flow Cats:** With reduced thermal mass, catalyst temp may fluctuate more rapidly. May benefit from slightly larger hysteresis to prevent cycling.

**Validation:** Monitor catalyst temp and Command Fuel Final during varied driving. Verify no rapid enrichment cycling when temp is near threshold range (550-600°C).

# Fuel - Power Enrichment - Catalyst Temp Trigger

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Fuel - Power Enrichment - Catalyst Temp Trigger - 2017 - RogueWRX.csv` |

## Value

**600.0122 CELSIUS**

## Description

This scalar defines the catalyst temperature threshold that triggers protective fuel enrichment. When the estimated catalyst temperature exceeds this value (600°C / 1112°F), the ECU activates power enrichment to add fuel and cool exhaust gases, protecting the catalytic converter from overheating damage.

**Purpose:**
- Prevents catalyst meltdown from excessive exhaust gas temperatures
- The additional fuel absorbs heat through vaporization, reducing EGT
- Typical stock threshold of 600°C provides margin before catalyst damage (~800°C)

**Activation Logic:**
- Catalyst temp is calculated/estimated from exhaust conditions
- When temp exceeds this threshold, power enrichment activates regardless of other conditions
- Works in conjunction with Catalyst Temp Hysteresis to prevent rapid cycling

**Operating Context:**
Sustained high-load operation (highway cruising, towing, spirited driving) can cause catalyst temperatures to approach this threshold. The enrichment protection is a safety feature to prevent costly catalyst damage.

## Related Tables

- **[Fuel - Power Enrichment - Catalyst Temp Hysteresis](./fuel-power-enrichment-catalyst-temp-hysteresis.md)**: Hysteresis value to prevent enrichment cycling
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: The lambda targets used during catalyst protection enrichment
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Normal closed-loop targets overridden by enrichment

## Related Datalog Parameters

- **Catalyst Temperature (°C)**: Estimated/calculated catalyst temperature - monitor approach to threshold
- **Fuel Mode**: Shows when catalyst protection enrichment is active
- **Command Fuel Final (λ)**: Verify enrichment targets are being applied
- **A/F Sensor 1 (λ)**: Actual measured AFR during enrichment

## Tuning Notes

**Stock Behavior:** Stock threshold of ~600°C provides conservative protection margin before catalyst substrate damage occurs (~750-850°C).

**Common Modifications:**
- **Catless/High-Flow Cats**: May increase threshold since aftermarket cats often have higher temp tolerance, or if running catless, protection is less critical
- **Track Use**: Some tuners raise threshold to delay enrichment for power, but this increases catalyst damage risk

**Recommended Approach:**
1. Log catalyst temperature during your typical driving scenarios
2. If enrichment activates frequently during normal driving, investigate root cause (likely too lean)
3. Only raise threshold if running high-flow/catless and willing to accept increased catalyst wear

**Validation:** Monitor catalyst temps during spirited driving. Threshold should activate before temps reach damage levels.

**Warning:** Lowering this threshold unnecessarily rich AFR at high load, reducing power and increasing fuel consumption. Raising it risks catalyst damage.

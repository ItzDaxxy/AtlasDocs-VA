# Fuel - Power Enrichment - Hysteresis (Leaning)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Power Enrichment - Hysteresis (Leaning) - 2017 - RogueWRX.csv` |

## Description

This table defines the calculated load threshold at which the ECU transitions OUT OF power enrichment mode back to closed-loop operation, indexed by RPM. This is the "leaning" direction of hysteresis - the load value that must be dropped below to deactivate enrichment.

**Purpose:**
- Establishes the load threshold for exiting power enrichment
- Different thresholds at different RPM allow smooth transition back to closed-loop
- Works with Hysteresis (Enriching) table to create a hysteresis band that prevents rapid mode cycling

**Operating Logic:**
- When calculated load drops below the value from this table, power enrichment deactivates
- Enrichment remains active until load falls below this threshold (even if below Enriching threshold)
- The gap between Enriching and Leaning thresholds prevents oscillation

**Value Interpretation:**
- Values represent calculated load thresholds in g/rev
- Higher values = enrichment deactivates at higher loads (earlier exit)
- Lower values = enrichment stays active longer (later exit)
- Must be LOWER than corresponding Enriching threshold values

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 1000.0000 to 8000.0000
- **Points**: 8

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |  1000.0000 |  2000.0000 |  3000.0000 |  4000.0000 |  5000.0000 |  6000.0000 |  7000.0000 |  8000.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs linear interpolation on this 1D table using:
- **X-Axis (RPM)**: Current engine speed

**Transition Logic:**
1. ECU looks up leaning threshold from this table based on current RPM
2. Compares current calculated load to threshold
3. If load drops below threshold AND currently in enrichment → deactivate enrichment
4. Once enrichment deactivates, Hysteresis (Enriching) table governs re-entry

**Hysteresis Behavior:**
The leaning threshold is typically lower than the enriching threshold. This creates a "dead band":
- Enter enrichment: Load > Enriching threshold
- Exit enrichment: Load < Leaning threshold
- In between: Maintains current state (no switching)

**Update Rate:** Evaluated every engine cycle during power enrichment operation.

## Related Tables

- **[Fuel - Power Enrichment - Hysteresis (Enriching)](./fuel-power-enrichment-hysteresis-enriching.md)**: Entry threshold - must be higher than this table for proper hysteresis
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: Lambda targets used while enrichment is active
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Targets used after exiting enrichment

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to threshold to understand when enrichment should deactivate
- **Fuel Mode**: Verify enrichment deactivates when load drops below threshold
- **RPM**: X-axis input for threshold lookup
- **Command Fuel Final (λ)**: Observe transition from enrichment back to closed-loop targets
- **A/F Sensor 1 (λ)**: Monitor actual AFR during transition

## Tuning Notes

**Stock Behavior:** Stock thresholds allow enrichment to remain active slightly longer than entry threshold, providing smooth transition and preventing mode cycling during throttle modulation.

**Common Modifications:**
- **Lower Thresholds**: Keeps enrichment active longer for more conservative protection during throttle lift
- **Higher Thresholds**: Earlier return to closed-loop for better fuel economy (reduces safety margin)
- **RPM-Based Adjustment**: May keep lower threshold at high RPM for extended protection

**Recommended Approach:**
1. Log calculated load and fuel mode during varied driving
2. Identify where enrichment currently deactivates
3. Ensure exit threshold is 0.1-0.2 g/rev below entry threshold
4. If experiencing AFR oscillation during part-throttle, increase hysteresis gap
5. Test throttle modulation scenarios to verify no rapid cycling

**Validation:** During throttle lift from WOT, enrichment should exit smoothly without cycling. Monitor fuel mode and AFR during throttle transitions.

## Warnings

⚠️ **Premature Exit Risk**: Setting threshold too high causes early exit from enrichment, which during partial throttle lift could:
- Return to lean closed-loop targets while still under load
- Create brief lean spikes during transitions
- Increase knock risk during throttle modulation

⚠️ **Hysteresis Integrity**: Values must be LOWER than corresponding Hysteresis (Enriching) values. If thresholds are equal or reversed:
- Rapid mode cycling will occur
- AFR will oscillate between rich and lean
- Potential knock from lean excursions

**Safe Practices:**
- Maintain minimum 0.1-0.2 g/rev gap below enriching thresholds
- Test with varied throttle inputs (lift, blip, modulation)
- Verify no rapid cycling in logs

**Signs of Problems:**
- Rapid fuel mode switching: Hysteresis gap too small or reversed
- Brief lean spikes during throttle lift: Exit threshold too high
- Extended rich operation during cruise: Exit threshold too low

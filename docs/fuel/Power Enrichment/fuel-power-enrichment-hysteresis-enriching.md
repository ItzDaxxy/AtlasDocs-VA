# Fuel - Power Enrichment - Hysteresis (Enriching)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Power Enrichment - Hysteresis (Enriching) - 2017 - RogueWRX.csv` |

## Description

This table defines the calculated load threshold at which the ECU transitions INTO power enrichment mode, indexed by RPM. This is the "enriching" direction of hysteresis - the load value that must be exceeded to activate enrichment.

**Purpose:**
- Establishes the load threshold for entering power enrichment
- Different thresholds at different RPM allow optimized enrichment activation
- Works with Hysteresis (Leaning) table to create a hysteresis band that prevents rapid mode cycling

**Operating Logic:**
- When calculated load exceeds the value from this table, power enrichment activates
- Once active, enrichment stays active until load drops below the Hysteresis (Leaning) threshold
- The gap between Enriching and Leaning thresholds prevents oscillation

**Value Interpretation:**
- Values represent calculated load thresholds in g/rev
- Higher values = enrichment activates at higher loads (later)
- Lower values = enrichment activates at lower loads (earlier)

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
1. ECU looks up enrichment threshold from this table based on current RPM
2. Compares current calculated load to threshold
3. If load exceeds threshold AND currently not in enrichment → activate enrichment
4. Once enrichment is active, this table is ignored until leaning threshold is reached

**Hysteresis Behavior:**
The enriching threshold is typically higher than the leaning threshold (from Hysteresis Leaning table). This creates a "dead band" that prevents rapid switching:
- Enter enrichment: Load > Enriching threshold
- Exit enrichment: Load < Leaning threshold

**Update Rate:** Evaluated every engine cycle during closed-loop operation.

## Related Tables

- **[Fuel - Power Enrichment - Hysteresis (Leaning)](./fuel-power-enrichment-hysteresis-leaning.md)**: Exit threshold - must be lower than this table for proper hysteresis
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: Lambda targets used once enrichment activates
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Targets used before enrichment threshold is reached

## Related Datalog Parameters

- **Calculated Load (g/rev)**: Compare to threshold to understand when enrichment should activate
- **Fuel Mode**: Verify enrichment activates when load exceeds threshold
- **RPM**: X-axis input for threshold lookup
- **Command Fuel Final (λ)**: Observe transition from closed-loop to enrichment targets

## Tuning Notes

**Stock Behavior:** Stock thresholds are calibrated to activate enrichment before engine reaches conditions requiring protection, while avoiding unnecessary enrichment during normal driving.

**Common Modifications:**
- **Lower Thresholds**: Activates enrichment earlier for more conservative safety margin
- **Higher Thresholds**: Delays enrichment for leaner cruise/part-throttle operation (increases knock risk)
- **RPM-Based Adjustment**: May lower threshold at high RPM where thermal stress increases faster

**Recommended Approach:**
1. Log calculated load and fuel mode during spirited driving
2. Identify where enrichment currently activates
3. If enrichment activates too early (during cruise), can cautiously raise threshold
4. If knock occurs before enrichment, lower threshold for earlier protection
5. Maintain gap between Enriching and Leaning thresholds

**Validation:** Monitor calculated load vs fuel mode transitions. Enrichment should activate consistently at the configured threshold.

## Warnings

⚠️ **Late Enrichment Risk**: Setting threshold too high delays protective enrichment, allowing lean operation under high load which can cause:
- Detonation and knock damage
- Excessive exhaust gas temperatures
- Catalyst overheating

⚠️ **Hysteresis Integrity**: If this table is modified, ensure values remain HIGHER than corresponding Hysteresis (Leaning) values to maintain proper hysteresis band.

**Safe Practices:**
- Do not raise thresholds significantly above stock without extensive logging
- Ensure knock margin is adequate at loads below threshold
- Maintain minimum 0.1-0.2 g/rev gap between enriching and leaning thresholds

**Signs of Problems:**
- Knock events at loads below enrichment threshold: Threshold too high
- Frequent enrichment cycling: Hysteresis gap too small
- AFR fluctuation during part-throttle: May need to adjust threshold

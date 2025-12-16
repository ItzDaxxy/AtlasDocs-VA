# Fuel - Power Enrichment - Target

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Power Enrichment - Target - 2017 - RogueWRX.csv` |

## Description

This table defines the target lambda (λ) for power enrichment mode, also known as WOT (wide-open throttle) enrichment. The ECU switches to this table when operating conditions require fuel enrichment beyond normal closed-loop targets, providing additional fuel for both performance and component protection.

**Activation Conditions:**
- Throttle position exceeds power enrichment threshold
- Engine load exceeds calculated load threshold for enrichment
- Catalyst temperature monitoring may trigger enrichment for protection
- DAM (Dynamic Advance Multiplier) may influence enrichment activation

**Value Interpretation:**
- Values are in AFR_EQ (lambda equivalent): 1.0 = stoichiometric (14.7:1 AFR for gasoline)
- Values < 1.0 = rich mixture (more fuel per unit air) - typical for power enrichment
- Stock values range from ~0.78-0.85 λ at high load cells for safety margin
- Low load cells often show 1.0 (stoich) as enrichment isn't needed there

**Operating Context:**
Power enrichment serves two purposes: maximizing power output by ensuring adequate fuel is available for combustion, and protecting engine components (pistons, exhaust valves, turbo, catalytic converter) from excessive heat through the cooling effect of additional fuel.

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: RPM
- **Range**: 1750.0000 to 5750.0000
- **Points**: 20

### Y-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1031 to 2.3719
- **Points**: 24

## Cell Values

- **Unit**: AFR_EQ
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |  1750.0000 |  2000.0000 |  2375.0000 |  2500.0000 |  3000.0000 |  3500.0000 |  4000.0000 |  4500.0000 |
--------------------------------------------------------------------------------------------------------------------
    0.1031 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
    0.2063 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
    0.3094 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
    0.4125 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.2773 |     1.3438 |     1.3008 |
    0.5156 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1719 |     1.1328 |     1.3008 |
    0.6188 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1914 |
    0.7219 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0508 |     1.1484 |     1.1875 |     1.1992 |
    0.8250 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1992 |     1.2305 |
```

## Functional Behavior

The ECU performs bilinear interpolation on this table using:
- **X-Axis (RPM)**: Current engine speed from crankshaft position sensor
- **Y-Axis (Calculated Load)**: Engine load in g/rev, calculated as (MAF × 120) / RPM

**Interpolation Process:**
1. When power enrichment conditions are met, ECU switches from closed-loop to this table
2. Current RPM and calculated load determine the four surrounding cells
3. Bilinear interpolation calculates the exact lambda target
4. Injector pulse width is adjusted to achieve this target lambda
5. O2 sensor feedback is typically ignored during power enrichment (open-loop operation)

**Update Rate:** Table is queried every engine cycle while power enrichment is active.

**Transition Behavior:** The transition between closed-loop targets and power enrichment targets uses hysteresis tables to prevent rapid switching. The "Hysteresis - Enriching" and "Hysteresis - Leaning" tables control the switching thresholds.

## Related Tables

- **[Fuel - Power Enrichment - Catalyst Temp Trigger](./fuel-power-enrichment-catalyst-temp-trigger.md)**: Temperature threshold that activates catalyst protection enrichment
- **[Fuel - Power Enrichment - DAM Activation](./fuel-power-enrichment-dam-activation.md)**: DAM threshold for power enrichment activation
- **[Fuel - Power Enrichment - Hysteresis Enriching](./fuel-power-enrichment-hysteresis-enriching.md)**: Load threshold for entering enrichment
- **[Fuel - Power Enrichment - Hysteresis Leaning](./fuel-power-enrichment-hysteresis-leaning.md)**: Load threshold for exiting enrichment
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Base closed-loop targets that this table overrides

## Related Datalog Parameters

- **Command Fuel Final (λ)**: The actual lambda target being commanded - verify this shows enrichment values when expected
- **Fuel Mode**: Confirms power enrichment mode is active (vs closed-loop or other modes)
- **Throttle Position (%)**: Monitor to correlate with enrichment activation
- **Calculated Load (g/rev)**: Y-axis input - verify correct table cell is being accessed
- **RPM**: X-axis input
- **A/F Sensor 1 (λ)**: Actual measured lambda from wideband - should match commanded target
- **Catalyst Temperature**: Monitor to understand when catalyst protection enrichment activates

## Tuning Notes

**Stock Behavior:** Stock values target lambda 0.78-0.85 at high load/RPM cells, providing a substantial safety margin for component protection. Lower load cells remain at stoichiometric (1.0) since enrichment isn't needed.

**Common Modifications:**
- **E85/Flex Fuel**: E85 requires richer targets due to different stoichiometric ratio (9.76:1). Lambda 0.78-0.82 is typical for E85 WOT.
- **Higher Boost Levels**: Increased boost may require richer targets (0.75-0.80 λ) for additional safety margin
- **Leaner for Power**: Some tuners run slightly leaner (0.82-0.85 λ) for marginal power gains, but this reduces safety margin

**Recommended Approach:**
1. Log extensively under WOT conditions to understand current fuel delivery
2. Verify wideband readings match commanded targets
3. Start with stock-rich values and only lean out after verifying adequate knock margin
4. Make small changes (±0.02 λ) and verify with logging
5. Monitor EGT if available - excessive temps indicate too lean

**Validation:** Compare actual wideband readings to commanded lambda. A mismatch indicates fuel delivery issues (injector capacity, fuel pressure, MAF scaling).

## Warnings

⚠️ **Lean WOT Mixture Risks**: Running lean under boost/load is extremely dangerous:
- Lambda > 0.90 under full boost dramatically increases knock probability
- Can cause piston ringland failure, rod bearing damage, or turbo failure
- Excessive EGT can melt exhaust valves or damage turbo

⚠️ **Injector Capacity**: If injectors cannot deliver the commanded fuel quantity, actual AFR will be leaner than target. Always verify actual wideband readings against commanded values.

**Safe Operating Limits:**
- WOT under boost: Lambda 0.75-0.85 (10.0-12.5:1 AFR gasoline)
- Never exceed lambda 0.90 under significant boost
- E85: Lambda 0.75-0.82 typical

**Signs of Problems:**
- Wideband reading leaner than commanded: Injector capacity/fuel pressure issue
- Knock activity under WOT: Targets may be too lean
- Black smoke/sooty plugs: Targets excessively rich (reduces power, wastes fuel)
- High EGT readings: Running too lean, add fuel immediately

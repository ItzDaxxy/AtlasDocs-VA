# Fuel - Closed Loop - Command Fuel L

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x24 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Closed Loop - Command Fuel L - 2018 - LF9C102P.csv` |

## Description

This table defines the target lambda (λ) command for closed-loop fuel control during normal engine operation. The ECU uses this table when operating in closed-loop mode, where exhaust oxygen sensor feedback actively modulates injector pulse width to achieve the commanded air-fuel ratio.

**Activation Conditions:**
- Engine is in closed-loop fuel mode (not in power enrichment or open loop)
- Coolant temperature exceeds minimum threshold for closed-loop entry
- Calculated load and RPM are within closed-loop operating limits
- O2 sensors are warmed up and providing valid feedback

**Value Interpretation:**
- Values are in AFR_EQ (lambda equivalent): 1.0 = stoichiometric (14.7:1 AFR for gasoline, 9.76:1 for E85)
- Values > 1.0 = lean (more air per unit fuel)
- Values < 1.0 = rich (less air per unit fuel)
- Stock values cluster around 0.95-1.02 for optimal catalyst efficiency and emissions

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - RPM Fuel
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 3.1734
- **Points**: 24

### Y-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 500.0000 to 8400.0000
- **Points**: 24

## Cell Values

- **Unit**: AFR_EQ
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.1935 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |
--------------------------------------------------------------------------------------------------------------------
  500.0000 |     1.0000 |     1.0000 |     1.0586 |     1.0586 |     1.0195 |     1.0000 |     1.0000 |     1.0000 |
  600.0000 |     1.0000 |     1.0000 |     1.0195 |     1.0195 |     1.0195 |     1.0000 |     1.0000 |     1.0195 |
  700.0000 |     1.0000 |     1.0000 |     1.0117 |     1.0195 |     1.0195 |     1.0000 |     1.0000 |     1.0156 |
  800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0195 |     1.0195 |     1.0000 |     1.0000 |     1.0078 |
 1000.0000 |     1.0117 |     1.0117 |     1.0117 |     1.0117 |     1.0117 |     1.0000 |     1.0000 |     1.0000 |
 1200.0000 |     0.9609 |     0.9609 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |
 1600.0000 |     0.9492 |     0.9492 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |
 2000.0000 |     0.9805 |     0.9805 |     0.9961 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |
```

## Functional Behavior

The ECU performs bilinear interpolation on this table using:
- **X-Axis (Calculated Load)**: Engine load in g/rev, representing mass airflow per revolution
- **Y-Axis (RPM)**: Current engine speed

**Interpolation Process:**
1. ECU calculates current load from MAF and RPM: Calculated Load = (MAF × 120) / RPM
2. Finds the four surrounding cells based on current load and RPM
3. Interpolates between cells to determine target lambda
4. Short-term fuel trim (STFT) adjusts injector pulse width to achieve this target
5. Long-term fuel trim (LTFT/AF Learn) stores persistent corrections

**Update Rate:** This table is queried continuously during closed-loop operation, with the target updated every engine cycle.

**Blending:** This table may be blended with EGR target tables and lean limit adders depending on operating conditions. The CL/OL transition tables determine when the ECU switches between this closed-loop target and open-loop fueling.

## Related Tables

- **[Fuel - CL/OL Transition - CL Limits](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Defines load/RPM/temp limits that trigger switch to open loop
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: WOT enrichment target that overrides this table during power enrichment
- **[Fuel - Closed Loop - Lean Limit Adder](./fuel-closed-loop-lean-limitadder-main-lean-limitadder-tgv-closed.md)**: Protective lean limit added to this base target
- **[Fuel - Closed Loop - Target - EGR Target Base](./fuel-closed-loop-target-high-egr-target-base-tgv-closed.md)**: Alternative targets when EGR is active

## Related Datalog Parameters

- **Command Fuel Final (λ)**: The actual lambda target being commanded - verify this matches expected values from this table
- **AF Correction STFT (%)**: Short-term fuel trim - should oscillate around 0% when properly tuned
- **AF Learn 1 (%)**: Long-term fuel trim/learned correction - indicates persistent deviation from target
- **Fuel Mode**: Confirms closed-loop operation (vs open-loop or power enrichment)
- **Calculated Load (g/rev)**: X-axis input - monitor to verify correct table cell is being accessed
- **RPM**: Y-axis input
- **A/F Sensor 1 (λ)**: Actual measured lambda from wideband O2 sensor - should track commanded value

## Tuning Notes

**Stock Behavior:** Stock values target lambda 0.95-1.02 across most operating conditions, optimized for catalyst efficiency, emissions compliance, and fuel economy. Slight rich bias at low load/RPM for idle stability.

**Common Modifications:**
- **Flex Fuel Compensation**: E85 requires richer targets (lambda ~0.85-0.90) due to different stoichiometric ratio (9.76:1 vs 14.7:1 for gasoline)
- **Performance Tuning**: Slightly richer targets (0.95-0.98) at high load cells can provide a small safety margin
- **Economy Tuning**: Leaner targets (1.02-1.05) at cruise cells can improve fuel economy if knock margin allows

**Recommended Approach:**
1. Log extensively to understand where the engine operates in this table
2. Make small changes (±0.02 lambda) to targeted cells
3. Monitor fuel trims after changes - excessive STFT/LTFT indicates the change isn't appropriate
4. Verify knock behavior remains acceptable after any changes

**Validation:** Monitor AF Correction STFT - it should remain within ±10-15%. Persistent high corrections indicate the commanded target cannot be achieved or is inappropriate for conditions.

## Warnings

⚠️ **Lean Mixture Risks**: Lambda values above 1.05 under load significantly increase knock probability and can cause:
- Detonation leading to piston/ringland damage
- Excessive exhaust gas temperatures (EGT)
- Catalyst overheating and failure

⚠️ **Rich Mixture Impacts**: Excessively rich targets (lambda < 0.85) cause:
- Catalyst damage from unburned fuel
- Spark plug fouling
- Reduced power and poor fuel economy

**Safe Operating Limits:**
- Cruise/part throttle: Lambda 0.95-1.05
- Light load: Lambda 1.00-1.02
- Never exceed lambda 1.05 under boost conditions

**Signs of Problems:**
- High fuel trims (STFT > ±15%): Indicates commanded target is inappropriate or fuel delivery issues
- Knock activity with lambda > 1.0: Reduce lambda target immediately
- Black smoke/fouled plugs: Targets too rich
- Catalyst efficiency codes: Often caused by excessively lean or rich operation

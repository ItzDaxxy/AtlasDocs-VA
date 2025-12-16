# Ignition - Dynamic Advance - Base (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Dynamic Advance - Base (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This table defines the base dynamic ignition timing advance for TGV (Tumble Generator Valve) open conditions, indexed by calculated load and RPM. Dynamic advance is the timing that varies based on knock learning (DAM) - it's added to the primary timing maps when the ECU has learned that additional advance is safe.

**Purpose:**
- Provides additional timing advance when knock-free operation confirmed
- Scales with DAM (Dynamic Advance Multiplier) for knock protection
- Allows more aggressive timing on quality fuel without knock
- TGV open = higher airflow conditions (moderate to high load)

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- Range: 0° to ~8° additional advance available
- Higher values at moderate loads and lower RPM
- Zero at very low loads and highest loads (conservative)

**Dynamic Advance System:**
```
Total Dynamic Advance = Base (this table) × DAM × Base Multiplier
```
At DAM = 1.0 (fully learned), these values represent maximum available dynamic advance.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.8360
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 0.0000 to 7600.0000
- **Points**: 21

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     4.9210 |     4.9210 |     4.9210 |     4.9210 |     4.9210 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     1.0545 |     2.1090 |     2.1090 |     2.1090 |     2.1090 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     3.1635 |     3.5150 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     2.1090 |     3.1635 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.1635 |     3.8665 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     2.1090 |     3.5150 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Pattern Analysis:**
- **Very Low Load (0-0.38 g/rev)**: Zero advance - idle/cruise covered by primary maps
- **Low RPM + Moderate Load**: Higher advance values (4-5°)
- **Mid RPM + Moderate Load**: Peak advance (~6-8°)
- **High Load (>1.5 g/rev)**: Advance reduces - knock protection under boost

**Combined with Primary Timing:**
```
Final Timing = Primary Map + (Dynamic Advance × DAM × Multiplier) + Compensations - Knock Retard
```

**TGV Open Context:**
TGV open maximizes airflow. This table provides appropriate dynamic advance for these higher-flow conditions where knock behavior differs from TGV-closed operation.

**Update Rate:** Calculated every ignition event.

## Related Tables

- **[Ignition - Dynamic Advance - Base (TGV Closed)](./ignition-dynamic-advance-base-tgv-closed.md)**: Dynamic advance for TGV closed
- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: DAM starting value
- **[Ignition - Dynamic Advance - Base Multiplier](./ignition-dynamic-advance-base-multiplier.md)**: DAM to multiplier conversion
- **[Ignition - Dynamic Advance - Adder (TGV Open)](./ignition-dynamic-advance-adder-adder-tgv-open.md)**: Additional advance values
- **[Primary - TGVs Open - AVCS Enabled](./primary-tgvs-closed-avcs-disabled.md)**: Primary timing map (base before dynamic)

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Scales this table's output
- **Ignition Timing**: Final actual timing (includes dynamic advance)
- **Feedback Knock Correction**: Real-time knock retard
- **Fine Knock Learn**: Per-cylinder learned corrections
- **Calculated Load (g/rev)**: X-axis input
- **TGV Position**: Should be 100% (open) for this table

## Tuning Notes

**Stock Behavior:** Stock provides moderate dynamic advance at mid-load regions where additional timing improves efficiency without significant knock risk. Zero values at high load protect under boost.

**When Dynamic Advance Helps:**
- Part-throttle cruising with quality fuel
- Light acceleration where more advance improves response
- Fuel economy at steady-state conditions

**Common Modifications:**
- May increase values slightly with confirmed knock-free operation
- Often zeroed in high-boost applications for safety
- Can be used to tune part-throttle response

**Relationship to Primary Maps:**
Dynamic advance is ADDED to primary timing maps. If primary maps are already aggressive, dynamic advance may cause knock. Many tuners reduce or zero dynamic advance and tune all timing into primary maps for predictability.

**DAM Dependency:**
At DAM = 0.125 (initial), only 12.5% of these values apply. At DAM = 1.0, full values apply. Consider this when diagnosing timing issues.

## Warnings

⚠️ **Knock Sensitive**: Dynamic advance is the first thing reduced when knock occurs. High values increase knock sensitivity.

⚠️ **DAM Interaction**: Changes affect timing differently at different DAM values - test across DAM range.

⚠️ **Stacks with Primary**: Combined with primary maps, total timing must remain safe.

**Safe Practices:**
- Monitor knock sensors and Fine Knock Learn after modifications
- Test at both low and high DAM conditions
- Consider zeroing if running aggressive primary timing maps
- Verify timing with timing light at various DAM values

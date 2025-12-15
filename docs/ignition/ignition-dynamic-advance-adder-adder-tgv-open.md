# Ignition - Dynamic Advance - Adder - Adder (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Dynamic Advance - Adder - Adder (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This table defines additional dynamic ignition advance values that are added to the base dynamic advance for TGV open conditions. The combined value (base + adder) is then scaled by DAM to determine total dynamic advance contribution.

**Purpose:**
- Provides additional advance on top of base dynamic advance
- Allows finer tuning of dynamic advance curve
- Separate table enables independent adjustment without modifying base
- TGV open = higher airflow conditions

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- Range: 0° to ~8° additional advance
- Added to base dynamic advance values
- Higher values at mid-RPM and moderate loads

**How Adder Works:**
```
Total Dynamic Advance = (Base + Adder) × DAM × Base Multiplier
```
The adder provides more dynamic advance headroom at specific operating points.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.8360
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 0.0000 to 8000.0000
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
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     3.1635 |     3.1635 |     1.0545 |     1.0545 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     5.2725 |     6.6785 |     8.0845 |     6.3270 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     1.0545 |     3.1635 |     3.8665 |     3.8665 |     2.4605 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.0545 |     3.5150 |     2.1090 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.7575 |     2.8120 |     5.6240 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.7575 |     3.5150 |     4.5695 |     4.2180 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Pattern Analysis:**
- **Low RPM (0-800)**: Zero or minimal adder
- **1200-1600 RPM**: Peak adder values (5-8°) at moderate loads
- **Mid-High RPM**: Moderate adder values (2-5°)
- **Very Low/High Load**: Reduced adder values

**Combined Effect:**
At 1200 RPM, 0.65 g/rev load with DAM = 1.0:
- Base: ~2° + Adder: ~5° = 7° total dynamic advance

**Why Separate Adder:**
The adder table allows tuners to adjust total dynamic advance without touching the base table. This is useful for incremental tuning - add advance via adder while keeping base as reference.

**Update Rate:** Calculated every ignition event alongside base.

## Related Tables

- **[Ignition - Dynamic Advance - Base (TGV Open)](./ignition-dynamic-advance-base-tgv-open.md)**: Base values this adds to
- **[Ignition - Dynamic Advance - Adder (TGV Closed)](./ignition-dynamic-advance-adder-adder-tgv-closed.md)**: Adder for TGV closed
- **[Ignition - Dynamic Advance - Adder Multiplier](./ignition-dynamic-advance-adder-adder-multiplier.md)**: May scale adder values
- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: Scales combined output

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Scales combined base+adder
- **Ignition Timing**: Shows total timing including dynamic advance
- **Feedback Knock Correction**: Real-time knock response
- **Fine Knock Learn**: Per-cylinder corrections
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Stock Behavior:** Stock adder provides significant additional advance at mid-load regions where the engine responds well to timing. Combined with base, total dynamic advance can reach 10-12° at DAM = 1.0.

**Tuning Approach:**
- Use adder for incremental timing changes
- Keep base as known-good reference
- Zero adder if simplifying to primary maps only

**Common Modifications:**
- May reduce if experiencing knock at part-throttle
- Often zeroed when using aggressive primary maps
- Can increase for fuel economy on quality fuel

**Total Dynamic Advance:**
With both base (~5°) and adder (~8°) at peak, total available dynamic advance can exceed 13° at DAM = 1.0. This is added to primary timing - total timing can become very aggressive.

**Adder vs Base Strategy:**
Some tuners zero the adder and tune all dynamic advance into base for simplicity. Others use adder for experimental changes while preserving stock base values.

## Warnings

⚠️ **Combined with Base**: Total dynamic advance = base + adder. Don't forget base values when adjusting.

⚠️ **High Advance Risk**: Combined base+adder can produce significant timing - monitor knock carefully.

⚠️ **DAM Dependency**: Full values only apply at DAM = 1.0. Low DAM masks high combined values.

**Safe Practices:**
- Calculate total potential advance (base + adder) at key operating points
- Test at DAM = 1.0 to verify safe combined timing
- Monitor Fine Knock Learn for signs of excessive advance
- If knock occurs, reduce adder before touching base

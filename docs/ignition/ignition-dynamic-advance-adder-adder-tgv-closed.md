# Ignition - Dynamic Advance - Adder - Adder (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Dynamic Advance - Adder - Adder (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This table defines additional dynamic ignition advance values for TGV closed conditions, added to the base dynamic advance. The combined total is scaled by DAM to determine dynamic advance contribution.

**Purpose:**
- Provides additional advance on top of base dynamic advance (TGV closed)
- Enables fine-tuning without modifying base table
- TGV closed = idle and light load with tumble active
- Generally more conservative values than TGV open adder

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- Range: 0° to ~2° additional advance
- Added to base dynamic advance before DAM scaling
- More conservative than TGV Open adder

**TGV Closed Context:**
With TGV closed (tumble active), combustion is already optimized. The adder provides modest additional advance capability for these conditions.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 3.0938
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
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     1.4060 |     2.1090 |     2.1090 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     1.4060 |     2.1090 |     2.1090 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     1.4060 |     2.1090 |     2.1090 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     1.4060 |     2.1090 |     2.1090 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     1.4060 |     1.4060 |     2.1090 |     2.1090 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev (extended to 3.09 g/rev)
- **Y-Axis (RPM)**: Current engine speed

**Table Pattern Analysis:**
- **Low RPM (0-800)**: Zero adder
- **1200+ RPM**: Modest adder values (1.4-2.1°) at moderate loads
- **Very consistent**: Similar values across most RPM/load combinations
- **Low Load (<0.5 g/rev)**: Zero adder

**Compared to TGV Open Adder:**
TGV Closed adder is much more conservative:
- TGV Open: Up to 8° adder at peak
- TGV Closed: Maximum ~2.1° adder
This reflects the more critical nature of idle and light-load timing.

**Update Rate:** Calculated every ignition event alongside base.

## Related Tables

- **[Ignition - Dynamic Advance - Base (TGV Closed)](./ignition-dynamic-advance-base-tgv-closed.md)**: Base values this adds to
- **[Ignition - Dynamic Advance - Adder (TGV Open)](./ignition-dynamic-advance-adder-adder-tgv-open.md)**: Adder for TGV open
- **[Ignition - Dynamic Advance - Adder Multiplier](./ignition-dynamic-advance-adder-adder-multiplier.md)**: May scale adder values
- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: Scales combined output

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Scales combined base+adder
- **Ignition Timing**: Shows total timing
- **Feedback Knock Correction**: Real-time knock response
- **TGV Position**: Should be 0% (closed) for this table

## Tuning Notes

**Stock Behavior:** Stock adder is conservative for TGV closed conditions. Combined with base, total dynamic advance remains modest during idle and light load.

**Why Conservative:**
TGV closed operation is critical for:
- Idle stability
- Cold start behavior
- Light-load driveability
Conservative values protect these sensitive operating regions.

**Common Modifications:**
- Generally left at stock - idle stability is critical
- May reduce if idle knock issues occur
- Rarely increased - limited benefit, significant risk

**TGV Delete Impact:**
If TGV is deleted and fixed open, this table may be unused. Verify ECU behavior and which tables are active.

**Extended Load Range:**
Note this table extends to 3.09 g/rev while TGV Open only goes to 2.84 g/rev. This ensures coverage even if TGV position signal has issues at higher loads.

## Warnings

⚠️ **Idle Sensitive**: Even small changes affect idle quality and stability.

⚠️ **Cold Start Impact**: Dynamic advance affects cold-start timing behavior.

⚠️ **TGV State Dependency**: Only applies when TGVs are closed.

**Safe Practices:**
- Test idle stability after any modifications
- Verify no knock at idle and light cruise
- Check cold start behavior if modified
- If TGV deleted, verify this table isn't being used

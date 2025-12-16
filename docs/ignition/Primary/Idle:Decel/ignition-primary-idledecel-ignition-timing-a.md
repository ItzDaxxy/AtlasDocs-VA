# Ignition - Primary - Idle/Decel - Ignition Timing A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Decel - Ignition Timing A - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing during idle and deceleration conditions (variant A), indexed by RPM. It provides timing values specifically for closed-throttle operation where the engine is either idling or decelerating with throttle closed.

**Purpose:**
- Controls timing during idle (throttle closed, low RPM)
- Controls timing during deceleration (throttle closed, engine braking)
- Optimizes emissions and catalyst light-off at idle
- Provides smooth transition between idle and decel conditions

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- Typically ranges from 10-25° at idle RPM
- May retard at higher RPM during decel for emissions
- "Variant A" suggests condition-dependent selection (likely temperature or time-based)

**Idle/Decel Mode:**
The ECU uses these dedicated tables when:
- Throttle position is closed (idle switch or <3% throttle)
- Load is below idle threshold
- Condition-specific selection between A and B variants

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 500.0000 to 6375.0000
- **Points**: 16

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   500.0000 |   600.0000 |   700.0000 |   800.0000 |   900.0000 |  1000.0000 |  1200.0000 |  1400.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (RPM)**: Current engine speed

**When Active:**
This table is active when:
- Throttle is closed (idle switch active or very low TP)
- Engine is idling or decelerating
- Variant A conditions are met (vs variant B)

**Variant A vs B Selection:**
Two idle/decel tables (A and B) exist - likely selected based on:
- Engine temperature (cold vs warm)
- Time since start
- Catalyst temperature
- AVCS state or TGV position

**Typical Values:**
- Idle (500-900 RPM): 10-20° BTDC for smooth idle
- Low decel (1000-2000 RPM): May advance for emissions
- High decel (>2000 RPM): May retard to prevent popping/afterfire

**1D Table Format:**
The 0x16 dimension indicates 1D lookup with 16 RPM points. Output timing values should exist but may not display in 2D preview.

**Update Rate:** Evaluated continuously during idle/decel operation.

## Related Tables

- **[Ignition - Primary - Idle/Decel - Timing B](./ignition-primary-idledecel-ignition-timing-b.md)**: Alternate idle/decel timing table
- **[Ignition - Primary - TGVs Closed (AVCS Disabled)](./primary-tgvs-closed-avcs-disabled.md)**: Primary timing maps
- **[Ignition - Compensation - Coolant (TGV Closed)](./ignition-compensation-coolant-tgv-closed.md)**: Temperature-based timing compensation

## Related Datalog Parameters

- **RPM**: X-axis input
- **Throttle Position (%)**: Indicates idle/decel mode entry
- **Ignition Timing**: Final timing (includes idle/decel table)
- **Idle Switch**: Binary indicator of closed throttle
- **Coolant Temperature (°C)**: May affect A/B selection

## Tuning Notes

**Stock Behavior:** Stock provides appropriate timing for emissions compliance and smooth idle. Timing is typically conservative to prevent knock at idle.

**Idle Timing Considerations:**
- More advance = higher idle RPM tendency, better fuel economy
- Less advance = lower idle RPM, smoother but less efficient
- Optimal idle timing varies with cam timing, compression, and modifications

**Decel Timing:**
During deceleration, timing affects:
- Engine braking feel
- Exhaust backfire/popping prevention
- Catalyst protection during fuel cut

**Common Modifications:**
- May advance for quicker idle response with modified cams
- May retard if experiencing idle knock with high compression
- Rarely modified without specific idle quality issues

**1D Limitations:**
This table only varies with RPM - if more complex idle timing control is needed, primary maps and compensations also contribute.

## Warnings

⚠️ **Idle Quality Critical**: Changes affect idle stability and smoothness.

⚠️ **Emissions Impact**: Idle timing affects emissions test results.

⚠️ **Cold Start**: Inappropriate idle timing can cause rough cold starts.

**Safe Practices:**
- Test changes at various engine temperatures
- Monitor for idle knock before and after modifications
- Verify smooth deceleration without popping or backfire
- Check idle stability after any modifications

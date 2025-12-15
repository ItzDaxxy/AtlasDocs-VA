# Ignition - Knock Thresholds - Low Timing - Cylinder 2

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Knock Thresholds - Low Timing - Cylinder 2 - 2017 - RogueWRX.csv` |

## Description

This table defines the knock detection threshold for Cylinder 2 when timing is in the "low" (retarded) range, indexed by calculated load and RPM. It provides more sensitive knock detection for when timing is already pulled back.

**Purpose:**
- Sets knock detection sensitivity for Cylinder 2 at low/retarded timing
- Generally LOWER thresholds than high-timing table (more sensitive)
- Detects knock when ECU has already retarded timing
- Cylinder 2 = front right, monitored by right knock sensor

**Value Interpretation:**
- Values are raw counts from knock sensor signal processing
- Range: ~2048-3072 in preview
- Lower values at 1200 RPM (2048) = most sensitive
- Values generally lower than high-timing table for same RPM

**Why More Sensitive:**
When timing is already retarded and knock still occurs, it indicates a more serious issue. Lower thresholds ensure these critical events are detected.

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.2580 to 2.5800
- **Points**: 8

### Y-Axis

- **Parameter**: Timing - Compensation - RPM
- **Unit**: RPM
- **Range**: 0.0000 to 6000.0000
- **Points**: 16

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.2580 |     0.5160 |     0.7740 |     1.2900 |     1.8060 |     2.0640 |     2.3220 |     2.5800 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |
  400.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |
  800.0000 |  2432.0000 |  2432.0000 |  2432.0000 |  2432.0000 |  2432.0000 |  2432.0000 |  2432.0000 |  2432.0000 |
 1200.0000 |  2048.0000 |  2048.0000 |  2048.0000 |  2048.0000 |  2048.0000 |  2048.0000 |  2048.0000 |  2048.0000 |
 1600.0000 |  2560.0000 |  2560.0000 |  2560.0000 |  2560.0000 |  2560.0000 |  2560.0000 |  2560.0000 |  2560.0000 |
 2000.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |
 2400.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |
 2800.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Low vs High Timing Comparison:**
At same RPM:
- High timing: ~2099-3149 (less sensitive)
- Low timing: ~2048-3072 (more sensitive in critical areas)
At 1200 RPM, low timing threshold is 2048 vs 2458 for high timing - significantly more sensitive.

**When Low Timing Table is Active:**
- After knock corrections have been applied
- When DAM is reduced
- When timing is already pulled back for protection

**Update Rate:** Evaluated every combustion event on Cylinder 2.

## Related Tables

- **[Ignition - Knock Thresholds - High Timing - Cylinder 2](./ignition-knock-thresholds-high-timing-cylinder-2.md)**: Threshold when timing advanced
- **[Ignition - Knock Thresholds - Low Timing - Cylinder 1](./ignition-knock-thresholds-low-timing-cylinder-1.md)**: Cylinder 1 low-timing
- **[Ignition - Knock Thresholds - Low Timing - Cylinder 4](./ignition-knock-thresholds-low-timing-cylinder-4.md)**: Cylinder 4 (same sensor)

## Related Datalog Parameters

- **Knock Sum Cylinder 2**: Actual knock sensor reading
- **Feedback Knock Correction**: Current timing retard
- **Fine Knock Learn Cylinder 2**: Learned correction
- **DAM**: Overall knock state

## Tuning Notes

**Stock Behavior:** Stock provides more sensitive knock detection when timing is already compromised, catching any remaining knock events.

**Critical Safety Function:**
Low-timing knock detection is the last line of defense:
- If knock occurs here, something is seriously wrong
- May indicate fuel quality, heat, or mechanical issues

**Diagnostic Value:**
If Cylinder 2 frequently triggers knock at low timing:
- Check for cylinder-specific issues
- Verify fuel injector function
- Check for right-bank cooling issues

## Warnings

⚠️ **Critical Safety Table**: Last-resort knock detection. Never raise these values.

⚠️ **Knock at Low Timing = Problem**: Investigate root cause immediately.

**Safe Practices:**
- Keep thresholds at or below high-timing values
- Investigate any consistent low-timing knock events
- Address fuel, temperature, or mechanical issues rather than adjusting sensitivity

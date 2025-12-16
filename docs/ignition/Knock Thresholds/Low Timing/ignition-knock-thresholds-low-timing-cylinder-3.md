# Ignition - Knock Thresholds - Low Timing - Cylinder 3

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Knock Thresholds - Low Timing - Cylinder 3 - 2017 - RogueWRX.csv` |

## Description

This table defines the knock detection threshold for Cylinder 3 when timing is in the "low" (retarded) range, indexed by calculated load and RPM. It provides more sensitive knock detection since knock is less likely with retarded timing.

**Purpose:**
- Sets knock detection sensitivity for Cylinder 3 at low/retarded timing
- Generally LOWER thresholds than high-timing table (more sensitive)
- Used when ECU has already retarded timing (knock risk lower)
- Per-cylinder calibration for accurate detection

**Value Interpretation:**
- Values are raw counts from knock sensor signal processing
- Range: ~2202-3584 in preview
- When knock sensor signal exceeds threshold, ECU detects knock
- Values generally lower than high-timing table (more conservative)

**Why Different from High Timing:**
When timing is already retarded:
- Knock is less likely (already protected)
- But if knock still occurs, it's more concerning
- Lower threshold ensures any remaining knock is caught

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
  800.0000 |  2509.0000 |  2509.0000 |  2509.0000 |  2509.0000 |  2509.0000 |  2509.0000 |  2509.0000 |  2509.0000 |
 1200.0000 |  2202.0000 |  2202.0000 |  2202.0000 |  2202.0000 |  2202.0000 |  2202.0000 |  2202.0000 |  2202.0000 |
 1600.0000 |  3584.0000 |  3584.0000 |  3584.0000 |  3584.0000 |  3584.0000 |  3584.0000 |  3584.0000 |  3584.0000 |
 2000.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |  2816.0000 |
 2400.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |
 2800.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |  3072.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Knock Detection at Low Timing:**
When timing is retarded (via knock correction or DAM):
- ECU switches to using "low timing" threshold tables
- Generally more sensitive (lower thresholds)
- Ensures any knock at low timing is still detected

**Threshold Comparison (High vs Low):**
At same RPM/load:
- High timing: ~2611-3635 (example)
- Low timing: ~2202-3584
Values vary by RPM but low-timing detection is generally MORE sensitive.

**Why More Sensitive:**
If knock occurs when timing is already retarded:
1. Something is seriously wrong (fuel, temps, etc.)
2. Further retard may be needed
3. Low threshold catches these critical events

**Cylinder 3 Location:**
FA20DIT Cylinder 3 = rear left. Left knock sensor monitors cylinders 1 and 3.

**Update Rate:** Evaluated every combustion event on Cylinder 3.

## Related Tables

- **[Ignition - Knock Thresholds - High Timing - Cylinder 3](./ignition-knock-thresholds-high-timing-cylinder-3.md)**: Threshold when timing is advanced
- **[Ignition - Knock Thresholds - Low Timing - Cylinder 1](./ignition-knock-thresholds-low-timing-cylinder-1.md)**: Cylinder 1 low-timing threshold
- **[Ignition - Knock Thresholds - Low Timing - Cylinder 2](./ignition-knock-thresholds-low-timing-cylinder-2.md)**: Cylinder 2 threshold
- **[Ignition - Knock Thresholds - Low Timing - Cylinder 4](./ignition-knock-thresholds-low-timing-cylinder-4.md)**: Cylinder 4 threshold

## Related Datalog Parameters

- **Knock Sum Cylinder 3**: Actual knock sensor reading
- **Feedback Knock Correction**: Current timing retard
- **Fine Knock Learn Cylinder 3**: Learned correction for this cylinder
- **Ignition Timing**: Determines high/low table selection
- **DAM**: Overall knock learning state

## Tuning Notes

**Stock Behavior:** Stock low-timing thresholds are more sensitive than high-timing, catching knock even when the ECU has already applied protection.

**When Low Timing Table is Used:**
ECU selects low-timing threshold when:
- Feedback Knock Correction is active (real-time retard)
- Fine Knock Learn has accumulated corrections
- DAM is low
- Generally when timing is already pulled back

**Threshold Selection Logic:**
The transition between high and low timing tables may be:
- Based on absolute timing value
- Based on amount of knock correction active
- Hysteresis to prevent rapid switching

**Common Observations:**
If knock events occur with low-timing threshold active:
- Investigate fuel quality
- Check IAT (heat soak)
- Verify no mechanical issues
- May indicate tune is still too aggressive

## Warnings

**Critical Safety Table**: Detects knock when timing is already compromised.

**Do Not Raise**: Raising low-timing thresholds removes last-resort protection.

**Knock at Low Timing = Problem**: If knock occurs with retarded timing, address root cause.

**Safe Practices:**
- Never modify to mask persistent knock issues
- If knock occurs at low timing, investigate thoroughly
- Low-timing knock events should be rare with proper tune
- Keep these thresholds at or below high-timing values

# Ignition - Knock Thresholds - High Timing - Cylinder 1

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Knock Thresholds - High Timing - Cylinder 1 - 2017 - RogueWRX.csv` |

## Description

This table defines the knock detection threshold for Cylinder 1 when timing is in the "high" (advanced) range, indexed by calculated load and RPM. The ECU compares knock sensor signal against this threshold to determine if knock is occurring.

**Purpose:**
- Sets knock detection sensitivity for Cylinder 1 at high timing
- Higher threshold = less sensitive (fewer false knock events)
- Lower threshold = more sensitive (catches more knock, more false positives)
- Per-cylinder calibration accounts for sensor position and cylinder characteristics

**Value Interpretation:**
- Values are raw counts from knock sensor signal processing
- Range: ~2400-4000 in preview (varies with RPM)
- When knock sensor signal exceeds threshold, ECU detects knock
- Values increase with RPM due to higher baseline engine noise

**High vs Low Timing:**
Two threshold tables exist per cylinder:
- **High Timing**: Used when timing is advanced (more knock-prone)
- **Low Timing**: Used when timing is retarded (less knock-prone)
This allows adaptive sensitivity based on current knock risk.

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
    0.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |
  400.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |
  800.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |  2662.0000 |
 1200.0000 |  2970.0000 |  2970.0000 |  2970.0000 |  2970.0000 |  2970.0000 |  2970.0000 |  2970.0000 |  2970.0000 |
 1600.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |
 2000.0000 |  3482.0000 |  3482.0000 |  3482.0000 |  3482.0000 |  3482.0000 |  3482.0000 |  3482.0000 |  3482.0000 |
 2400.0000 |  3968.0000 |  3968.0000 |  3968.0000 |  3968.0000 |  3968.0000 |  3968.0000 |  3968.0000 |  3968.0000 |
 2800.0000 |  3174.0000 |  3174.0000 |  3174.0000 |  3174.0000 |  3174.0000 |  3174.0000 |  3174.0000 |  3174.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Knock Detection Process:**
1. Knock sensor detects vibrations
2. ECU filters for knock-specific frequencies (~6-8 kHz)
3. Processes signal into numerical value
4. Compares against this threshold
5. If signal > threshold → knock detected

**Threshold vs RPM Pattern:**
Values generally increase with RPM:
- Low RPM (0-800): ~2662 (lower engine noise)
- Mid RPM (1200-2000): ~2944-3482
- Higher RPM (2400): ~3968
This accounts for increased mechanical noise at higher RPM.

**Load-Independence:**
Note all values are uniform across load axis - threshold is primarily RPM-dependent for this cylinder.

**Cylinder 1 Location:**
FA20DIT Cylinder 1 = front left. Left knock sensor monitors cylinders 1 and 3.

**Update Rate:** Evaluated every combustion event on Cylinder 1.

## Related Tables

- **[Ignition - Knock Thresholds - Low Timing - Cylinder 1](./ignition-knock-thresholds-low-timing-cylinder-1.md)**: Threshold when timing is retarded
- **[Ignition - Knock Thresholds - High Timing - Cylinder 2](./ignition-knock-thresholds-high-timing-cylinder-2.md)**: Cylinder 2 threshold
- **[Ignition - Knock Thresholds - High Timing - Cylinder 3](./ignition-knock-thresholds-high-timing-cylinder-3.md)**: Cylinder 3 threshold
- **[Ignition - Knock Thresholds - High Timing - Cylinder 4](./ignition-knock-thresholds-high-timing-cylinder-4.md)**: Cylinder 4 threshold

## Related Datalog Parameters

- **Knock Sum Cylinder 1**: Actual knock sensor reading
- **Feedback Knock Correction**: Timing retard from knock events
- **Fine Knock Learn Cylinder 1**: Learned correction for this cylinder
- **Ignition Timing**: Current timing (determines high/low table selection)
- **DAM**: Overall knock learning state

## Tuning Notes

**Stock Behavior:** Stock thresholds are calibrated to minimize false knock detection while reliably catching actual knock. Values balance sensitivity with noise rejection.

**Understanding Values:**
- Higher values = less sensitive = fewer knock events detected
- Lower values = more sensitive = more events detected (including false)
- Stock is usually well-calibrated for factory components

**When to Modify:**
Generally do NOT modify unless:
- Confirmed false knock due to mechanical modifications
- After careful analysis showing threshold is inappropriately set
- Professional tuner verification

**False Knock Sources:**
- Exhaust system rattles
- Heat shields
- Fuel injector tick
- Accessory belt noise
Raising threshold can mask these, but also masks real knock.

**Per-Cylinder Variation:**
Each cylinder has its own threshold tables because:
- Distance from knock sensor differs
- Combustion characteristics vary slightly
- Sensor sensitivity varies by position

## Warnings

⚠️ **Engine Safety Critical**: Knock thresholds are the primary knock protection. Incorrect values cause engine damage.

⚠️ **Do Not Raise Blindly**: Raising thresholds masks real knock - only adjust with verified data.

⚠️ **Professional Tuning Required**: Knock threshold calibration requires proper analysis tools and expertise.

**Safe Practices:**
- Never raise thresholds to "fix" knock - fix the knock cause instead
- Only lower thresholds if confirmed false knock with safe fuel and tune
- Monitor knock events with audio analysis if available
- Document any changes thoroughly

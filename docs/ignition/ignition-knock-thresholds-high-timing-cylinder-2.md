# Ignition - Knock Thresholds - High Timing - Cylinder 2

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Knock Thresholds - High Timing - Cylinder 2 - 2017 - RogueWRX.csv` |

## Description

This table defines the knock detection threshold for Cylinder 2 when timing is in the "high" (advanced) range, indexed by calculated load and RPM. Cylinder 2 is on the right bank (front right) and is monitored by the right knock sensor.

**Purpose:**
- Sets knock detection sensitivity for Cylinder 2 at high timing
- Higher threshold = less sensitive, Lower = more sensitive
- Per-cylinder calibration accounts for sensor distance and cylinder characteristics
- Cylinder 2 = front right, monitored by right knock sensor

**Value Interpretation:**
- Values are raw counts from knock sensor signal processing
- Range: ~2099-3149 in preview
- When knock signal exceeds threshold, ECU detects knock
- Values vary with RPM due to engine noise characteristics

**Cylinder 2 Position:**
FA20DIT: Cylinder 2 = front right. Right knock sensor monitors cylinders 2 and 4. Cylinder 2 is closest to right sensor.

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
    0.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |
  400.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |
  800.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |  2867.0000 |
 1200.0000 |  2458.0000 |  2458.0000 |  2458.0000 |  2458.0000 |  2458.0000 |  2458.0000 |  2458.0000 |  2458.0000 |
 1600.0000 |  2099.0000 |  2099.0000 |  2099.0000 |  2099.0000 |  2099.0000 |  2099.0000 |  2099.0000 |  2099.0000 |
 2000.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |
 2400.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |  3149.0000 |
 2800.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |  2944.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Threshold Pattern:**
Cylinder 2 shows non-linear RPM response:
- Low RPM (0-800): ~2867
- 1200-1600 RPM: Lower values (~2458-2099) - more sensitive
- Mid-high RPM (2000+): Higher values (~2944-3149)

**Why Lower at 1200-1600 RPM:**
This RPM range may have less mechanical noise, allowing lower thresholds (higher sensitivity). Or it may be a range where knock is more concerning and requires tighter monitoring.

**Right Bank Monitoring:**
Cylinder 2 is monitored by right knock sensor along with Cylinder 4. Right bank may have different noise characteristics than left.

**Update Rate:** Evaluated every combustion event on Cylinder 2.

## Related Tables

- **[Ignition - Knock Thresholds - Low Timing - Cylinder 2](./ignition-knock-thresholds-low-timing-cylinder-2.md)**: Threshold when timing retarded
- **[Ignition - Knock Thresholds - High Timing - Cylinder 1](./ignition-knock-thresholds-high-timing-cylinder-1.md)**: Cylinder 1 threshold
- **[Ignition - Knock Thresholds - High Timing - Cylinder 4](./ignition-knock-thresholds-high-timing-cylinder-4.md)**: Cylinder 4 (same sensor)

## Related Datalog Parameters

- **Knock Sum Cylinder 2**: Actual knock sensor reading
- **Feedback Knock Correction**: Timing retard from knock
- **Fine Knock Learn Cylinder 2**: Learned correction
- **DAM**: Overall knock state

## Tuning Notes

**Stock Behavior:** Stock thresholds are calibrated for Cylinder 2's specific characteristics relative to right knock sensor position.

**Cylinder 2 Notes:**
- Front right position
- Closest to right knock sensor
- May have different thermal characteristics than left bank

**Common Issues:**
If Cylinder 2 shows frequent knock events:
- Check fuel injector function
- Verify equal fuel distribution
- May indicate right-bank specific issue

## Warnings

⚠️ **Engine Safety Critical**: Knock thresholds protect the engine. Don't modify blindly.

⚠️ **Per-Cylinder Calibration**: Each cylinder's thresholds are specific to its characteristics.

**Safe Practices:**
- Never raise thresholds to mask knock
- Compare all cylinder knock activity for diagnosis
- Address root causes rather than adjusting sensitivity

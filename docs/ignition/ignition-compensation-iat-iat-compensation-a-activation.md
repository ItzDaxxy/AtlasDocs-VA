# Ignition - Compensation - IAT - IAT Compensation A Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Compensation - IAT - IAT Compensation A Activation - 2017 - RogueWRX.csv` |

## Description

This 2D table defines the activation percentage for IAT (Intake Air Temperature) timing compensation variant A, indexed by calculated load and RPM. It scales the base IAT compensation to vary its effect across different operating conditions.

**Purpose:**
- Controls where and how much IAT compensation applies
- Allows RPM and load-dependent scaling of temperature compensation
- Negative values reduce or negate the base compensation
- Values in percent determine effective IAT compensation strength

**Value Interpretation:**
- Values in percent (%)
- -100% = Completely disables IAT compensation at that point
- -25% to -60% = Significantly reduces base compensation
- Negative values counteract base IAT compensation
- Pattern varies strategically by RPM and load

**Pattern Analysis:**
The preview shows mostly negative values:
- Low load areas: -100% (compensation disabled)
- Mid-high load areas: -25% to -65% (compensation reduced)
This reduces IAT compensation where it may be less needed or could cause driveability issues.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 3.0938
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8400.0000
- **Points**: 22

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -25.0000 |   -25.0000 |   -25.0000 |   -25.0000 |
  800.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -25.0000 |   -25.0000 |   -25.0000 |   -25.0000 |
 1200.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -25.0000 |   -25.0000 |   -25.0000 |   -25.0000 |
 1600.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -50.0000 |   -50.0000 |   -50.0000 |   -50.0000 |
 2000.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -54.6875 |   -54.6875 |
 2400.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -37.5000 |   -37.5000 |
 2800.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -65.6250 |   -42.9688 |   -37.5000 |
 3200.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |   -32.8125 |   -32.8125 |   -32.8125 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Activation Calculation:**
```
Effective IAT Compensation = Base IAT Compensation × (1 + Activation%/100)
```
With negative activation values, the base compensation is reduced or eliminated:
- Base = -3° retard, Activation = -100%
- Effective = -3° × (1 - 1.00) = 0° (no compensation)
- Base = -3° retard, Activation = -50%
- Effective = -3° × (1 - 0.50) = -1.5° retard

**Why Reduce IAT Compensation:**
IAT compensation may be selectively reduced because:
- High load/boost: Other protections more important
- Low load: IAT effect minimal
- Specific RPM ranges: Calibration preference
- To prevent excessive timing retard under certain conditions

**Table Pattern:**
- Low load: Often -100% (disabled)
- Mid load: Variable reduction (-25% to -65%)
- RPM dependent: Different needs at different engine speeds

**Update Rate:** Calculated continuously alongside IAT compensation.

## Related Tables

- **[Ignition - Compensation - IAT - Compensation A](./ignition-compensation-iat-iat-compensation-a.md)**: Base IAT compensation scaled by this table
- **[Ignition - Compensation - IAT - Compensation B Activation](./ignition-compensation-iat-iat-compensation-b-activation.md)**: Variant B activation
- **[Ignition - Compensation - IAT - Compensation B](./ignition-compensation-iat-iat-compensation-b.md)**: Variant B base compensation

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **IAT (Intake Air Temperature)**: Drives base compensation
- **Ignition Timing**: Shows final timing with scaled compensation
- **Manifold Pressure**: May influence A/B selection

## Tuning Notes

**Stock Behavior:** Stock reduces or disables IAT compensation in specific operating regions, likely to balance knock protection with driveability and performance.

**Understanding Negative Values:**
The negative percentages reduce IAT compensation:
- They don't add timing
- They reduce the retard from the base IAT table
- -100% completely disables IAT compensation at that point
- -50% means only 50% of base IAT retard applies

**Why This Design:**
IAT compensation activation allows precise control:
- Full compensation where critical (high boost, hot temps)
- Reduced compensation for driveability (part throttle, cruise)
- Disabled where unnecessary (low load, cool temps)

**Common Modifications:**
- Generally left at stock
- Could increase negative values to reduce IAT retard (test carefully for knock)
- Could reduce negative values to apply more IAT protection
- Requires understanding of base IAT compensation table

**Variant A Context:**
Multiple IAT variants (A and B) exist with separate activation tables. The ECU likely selects between them based on operating conditions, allowing different IAT strategies for different scenarios.

## Warnings

**Complex Interaction**: This table modifies another table's output - changes have indirect effects.

**Knock Protection**: Reducing IAT compensation (more negative activation) can cause knock if IAT is elevated.

**Heat Soak Risk**: On hot days or after hard driving, reducing IAT compensation removes important protection.

**Safe Practices:**
- Understand base IAT compensation before modifying activation
- Monitor IAT and knock events during testing
- Don't reduce IAT protection to mask heat soak issues
- Test across various ambient temperatures and driving conditions

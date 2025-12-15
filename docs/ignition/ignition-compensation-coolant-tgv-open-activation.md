# Ignition - Compensation - Coolant - TGV Open Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Ignition - Compensation - Coolant - TGV Open Activation - 2017 - RogueWRX.csv` |

## Description

This 2D table defines the activation percentage for coolant temperature timing compensation under TGV open conditions, indexed by calculated load and RPM. It scales the base coolant compensation to vary its effect across different operating conditions.

**Purpose:**
- Controls where and how much coolant compensation applies
- Allows RPM and load-dependent scaling of temperature compensation
- Negative values reduce or negate the base compensation
- Zero = no compensation at that operating point

**Value Interpretation:**
- Values in percent (%)
- 0% = No coolant compensation applied
- -13% = Reduces base compensation by 13%
- -33% to -60% = Significantly reduces compensation at higher RPM
- Negative values counteract positive base compensation

**Pattern Analysis:**
The preview shows negative values that increase with RPM:
- Low RPM (500-3500): 0% or -13% (minimal reduction)
- Mid RPM (4000): -33%
- High RPM (4500+): -47% to -60%
This reduces cold compensation at high RPM where it's less needed.

## Axes

### X-Axis

- **Parameter**: Timing - Compensation - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 2.8380
- **Points**: 16

### Y-Axis

- **Parameter**: Timing - Compensation - RPM
- **Unit**: RPM
- **Range**: 500.0000 to 6375.0000
- **Points**: 22

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -13.0000 |
 1000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -13.0000 |
 2500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -13.0000 |
 3000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -13.0000 |
 3500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -13.0000 |
 4000.0000 |   -33.0000 |   -33.0000 |   -33.0000 |   -33.0000 |   -33.0000 |   -33.0000 |   -33.0000 |   -33.0000 |
 4500.0000 |   -47.0000 |   -47.0000 |   -47.0000 |   -47.0000 |   -47.0000 |   -47.0000 |   -47.0000 |   -47.0000 |
 5000.0000 |   -60.0000 |   -60.0000 |   -60.0000 |   -60.0000 |   -60.0000 |   -60.0000 |   -60.0000 |   -60.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Activation Calculation:**
```
Effective Compensation = Base Compensation × (1 + Activation%/100)
```
With negative activation values, the base compensation is reduced:
- Base = +5° advance, Activation = -60%
- Effective = 5° × (1 - 0.60) = 2° advance

**Why Reduce at High RPM:**
At high RPM:
- Engine generates more heat (less cold)
- Combustion is faster (less advance needed)
- Knock risk increases with advanced timing
The negative values reduce cold compensation where it's less beneficial.

**Table Pattern:**
- Low RPM: Minimal reduction (cold compensation applies fully)
- High RPM: Significant reduction (less cold compensation needed)
- Load axis: Relatively uniform, suggesting load is less critical than RPM for this compensation

**Update Rate:** Calculated continuously alongside coolant compensation.

## Related Tables

- **[Ignition - Compensation - Coolant - TGV Open](./ignition-compensation-coolant-tgv-open.md)**: Base compensation scaled by this table
- **[Ignition - Compensation - Coolant - TGV Closed Activation](./ignition-compensation-coolant-tgv-closed-activation.md)**: TGV closed equivalent

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Coolant Temperature (°C)**: Drives base compensation
- **Ignition Timing**: Shows final timing with scaled compensation
- **TGV Position**: Should be open for this table

## Tuning Notes

**Stock Behavior:** Stock reduces cold compensation at high RPM where the engine warms quickly and knock risk is higher. Low RPM retains full cold compensation for idle and cruise quality.

**Why This Design:**
Cold compensation is most important at:
- Idle (low RPM, low load): Full compensation helps stability
- Light cruise (moderate RPM/load): Some compensation for efficiency
Cold compensation is less needed at:
- High RPM: Engine heats up, faster combustion
- High load under boost: Risk of knock

**Common Modifications:**
- Generally left at stock
- Could increase negative values if experiencing cold knock at high RPM
- Could reduce negative values for more cold timing at high RPM (test carefully)

**Understanding Negative Values:**
The negative percentages can be confusing:
- They don't add retard
- They reduce the cold advance from the base table
- -60% means only 40% of base cold advance applies

## Warnings

⚠️ **Complex Interaction**: This table modifies another table's output - changes have indirect effects.

⚠️ **High RPM Cold Knock**: Reducing the negative values (allowing more cold advance at high RPM) can cause knock.

⚠️ **TGV State**: Only applies when TGVs are open.

**Safe Practices:**
- Understand base compensation before modifying activation
- Test cold operation at various RPM ranges
- Monitor knock during cold high-RPM operation

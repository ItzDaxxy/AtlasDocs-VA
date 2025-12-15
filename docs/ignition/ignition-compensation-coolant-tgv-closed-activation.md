# Ignition - Compensation - Coolant - TGV Closed Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Ignition - Compensation - Coolant - TGV Closed Activation - 2017 - RogueWRX.csv` |

## Description

This 2D table defines the activation percentage for coolant temperature timing compensation under TGV closed conditions, indexed by calculated load and RPM. It scales the base coolant compensation to vary its effect across different operating conditions.

**Purpose:**
- Controls where and how much coolant compensation applies with TGVs closed
- Allows RPM and load-dependent scaling of temperature compensation
- Zero values indicate no modification to base compensation
- TGV closed typically occurs at idle and light load

**Value Interpretation:**
- Values in percent (%)
- 0% = No scaling (base compensation applies directly)
- Preview shows all zeros = base coolant compensation used as-is
- Non-zero values would scale the base compensation up or down

**Pattern Analysis:**
The preview shows all zero values across visible operating range:
- No activation scaling applied
- Base coolant compensation table used directly
- Simplified calibration approach

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
  500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4500.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 5000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Activation Calculation:**
```
Effective Compensation = Base Compensation × (1 + Activation%/100)
```
With zero activation values, the base compensation passes through unchanged:
- Base = +5° advance, Activation = 0%
- Effective = 5° × (1 + 0) = 5° advance

**All Zeros Pattern:**
Stock calibration uses no activation scaling for TGV closed:
- Base coolant compensation applies directly
- No RPM or load-dependent modification
- Simpler than TGV open which has negative activation values

**TGV Closed Context:**
TGVs (Tumble Generator Valves) are closed at:
- Idle
- Light load
- Low RPM
These conditions benefit from full coolant compensation for cold starts and warm-up.

**Comparison to TGV Open:**
- TGV Open Activation: Has negative values reducing compensation at high RPM
- TGV Closed Activation: All zeros (no modification)
This suggests closed TGVs benefit from consistent coolant compensation.

**Update Rate:** Calculated continuously alongside coolant compensation.

## Related Tables

- **[Ignition - Compensation - Coolant - TGV Closed](./ignition-compensation-coolant-tgv-closed.md)**: Base compensation scaled by this table
- **[Ignition - Compensation - Coolant - TGV Open Activation](./ignition-compensation-coolant-tgv-open-activation.md)**: TGV open equivalent
- **[Ignition - Compensation - Coolant - TGV Open](./ignition-compensation-coolant-tgv-open.md)**: TGV open base compensation

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Coolant Temperature (°C)**: Drives base compensation
- **Ignition Timing**: Shows final timing with compensation
- **TGV Position**: Should be closed for this table

## Tuning Notes

**Stock Behavior:** Stock applies no activation scaling - base coolant compensation is used directly across all operating points with TGVs closed.

**All Zeros Meaning:**
Zero activation means:
- Base coolant table applied as-is
- No RPM or load modification
- Full cold compensation at all conditions
- Simpler calibration strategy

**Why No Scaling:**
TGV closed conditions may not need scaling because:
- Idle and light load are primary use cases
- Cold compensation important for driveability
- Knock risk lower at these operating points
- Consistent compensation preferred for smooth operation

**Common Modifications:**
- Usually left at stock (all zeros)
- Could add negative values to reduce cold compensation at specific points
- Could add positive values to increase compensation
- Generally unnecessary - base table handles compensation well

**Comparison to TGV Open:**
TGV open activation reduces compensation at high RPM because:
- Engine heats quickly under load
- Knock risk increases
TGV closed doesn't need this because operating conditions are gentler.

## Warnings

**Cold Start Important**: TGV closed includes cold start and warm-up - don't compromise cold compensation.

**Idle Stability**: Changes could affect idle quality, especially when cold.

**TGV State**: Only applies when TGVs are closed (idle, light load).

**Safe Practices:**
- Leave at stock zeros unless specific need identified
- Test cold start and warm-up if modifying
- Monitor idle stability across temperature ranges
- Understand base compensation table before adding activation scaling

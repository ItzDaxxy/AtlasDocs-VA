# Ignition - Dynamic Advance - Base Multiplier

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x17 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Dynamic Advance - Base Multiplier - 2017 - RogueWRX.csv` |

## Description

This 1D table converts the Dynamic Advance Multiplier (DAM) value into an actual multiplier applied to the dynamic advance tables. It allows non-linear scaling of dynamic advance based on DAM learning state.

**Purpose:**
- Converts DAM value (0-1) to actual timing multiplier
- Allows customization of how DAM affects timing
- Provides non-linear response if needed (aggressive or conservative)

**Value Interpretation:**
- X-axis: DAM value from 0 (no learned advance) to 1 (full learned advance)
- Output: Multiplier applied to dynamic advance base tables
- Linear relationship = 1:1 mapping (DAM 0.5 = 50% advance)
- Could be shaped for different DAM response characteristics

**How It Works:**
```
Effective Multiplier = Base Multiplier[DAM]
Dynamic Advance = Base Table Value × Effective Multiplier
```

## Axes

### X-Axis

- **Parameter**: Timing - Dynamic Advance - DAM
- **Unit**: NONE (0-1 scale)
- **Range**: 0.0000 to 1.0000
- **Points**: 17

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.1250 |     0.1875 |     0.2500 |     0.3125 |     0.3750 |     0.4375 |     0.5000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (DAM)**: Current Dynamic Advance Multiplier value

**Multiplier Application:**
The output multiplier is applied to the dynamic advance base tables. A typical stock calibration uses linear mapping:
- DAM = 0.0 → Multiplier = 0.0 (no dynamic advance)
- DAM = 0.5 → Multiplier = 0.5 (50% dynamic advance)
- DAM = 1.0 → Multiplier = 1.0 (full dynamic advance)

**Non-Linear Options:**
The table allows non-linear responses:
- Conservative: Lower multiplier at mid-DAM values
- Aggressive: Higher multiplier at mid-DAM values
- Threshold: No advance until DAM reaches certain value

**Update Rate:** Calculated whenever dynamic advance is computed.

## Related Tables

- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: Starting DAM value
- **[Ignition - Dynamic Advance - Base (TGV Open)](./ignition-dynamic-advance-base-tgv-open.md)**: Base values multiplied by this
- **[Ignition - Dynamic Advance - Base (TGV Closed)](./ignition-dynamic-advance-base-tgv-closed.md)**: TGV closed base values
- **[Ignition - Dynamic Advance - Adder (TGV Open)](./ignition-dynamic-advance-adder-adder-tgv-open.md)**: Additional advance values

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Input to this table
- **Ignition Timing**: Shows effect of dynamic advance
- **Fine Knock Learn**: Per-cylinder corrections

## Tuning Notes

**Stock Behavior:** Stock typically uses linear 1:1 mapping - DAM value directly corresponds to advance multiplier.

**Common Modifications:**
- Usually left linear for predictable behavior
- Could add threshold to require higher DAM before advance activates
- Could make more conservative for knock-prone applications

**DAM Recovery Correlation:**
Since this table defines how DAM translates to actual timing, understanding the relationship helps interpret DAM changes. A DAM of 1.0 should result in full dynamic advance availability.

**1D Table Format:**
Note the 0x17 dimension indicates this is a 1D lookup with 17 points across the DAM range. Output values should be displayed in the table but may not render in 2D preview format.

## Warnings

⚠️ **Knock System Interface**: This table is part of the knock protection system - modifications affect engine protection.

⚠️ **Non-Linear Effects**: Non-linear mapping complicates DAM interpretation in datalogs.

**Safe Practices:**
- Keep linear relationship unless specific need for non-linear response
- Understand how DAM changes affect actual timing through this multiplier
- Don't use this to mask knock issues - address root causes instead

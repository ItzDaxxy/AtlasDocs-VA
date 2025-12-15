# Ignition - Dynamic Advance - Adder - Adder Multiplier

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x17 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Dynamic Advance - Adder - Adder Multiplier - 2017 - RogueWRX.csv` |

## Description

This 1D table converts the Dynamic Advance Multiplier (DAM) value into a multiplier specifically for the dynamic advance adder tables. It allows the adder to have a different DAM response than the base dynamic advance.

**Purpose:**
- Converts DAM value (0-1) to multiplier for adder tables specifically
- Allows independent scaling of adder vs base dynamic advance
- Can make adder activate faster or slower than base as DAM recovers

**Value Interpretation:**
- X-axis: DAM value from 0 (no advance) to 1 (full advance)
- Output: Multiplier applied to adder table values only
- Typically linear (1:1) but could be shaped differently than base multiplier

**Separate Adder Control:**
Having separate multipliers for base and adder allows:
- Base advance to scale linearly with DAM
- Adder to activate faster (more aggressive) or slower (more conservative)
- Different knock-recovery behaviors for different timing components

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
```
Effective Adder = Adder Table Value × Adder Multiplier[DAM]
Total Dynamic Advance = (Base × Base Multiplier) + (Adder × Adder Multiplier)
```

**Relationship to Base Multiplier:**
Both multipliers convert DAM to a scaling factor, but apply independently:
- Base Multiplier × Base Table values
- Adder Multiplier × Adder Table values
This separation allows fine control over how each component responds to DAM.

**1D Table Format:**
The 0x17 dimension indicates a 1D lookup with 17 points across DAM range. Output values may not display in standard 2D preview format.

**Update Rate:** Calculated whenever dynamic advance is computed.

## Related Tables

- **[Ignition - Dynamic Advance - Base Multiplier](./ignition-dynamic-advance-base-multiplier.md)**: Base dynamic advance multiplier
- **[Ignition - Dynamic Advance - Adder (TGV Open)](./ignition-dynamic-advance-adder-adder-tgv-open.md)**: Adder values scaled by this multiplier
- **[Ignition - Dynamic Advance - Adder (TGV Closed)](./ignition-dynamic-advance-adder-adder-tgv-closed.md)**: Adder values scaled by this multiplier
- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: Starting DAM value

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Input to this table
- **Ignition Timing**: Shows effect of dynamic advance (base + adder)
- **Fine Knock Learn**: Per-cylinder knock corrections

## Tuning Notes

**Stock Behavior:** Stock typically uses linear 1:1 mapping similar to base multiplier, making adder scale directly with DAM.

**Advanced Strategies:**
- **Faster adder activation**: Make adder multiplier higher than base at mid-DAM - adder contributes earlier during DAM recovery
- **Conservative adder**: Make adder multiplier lower - adder only fully active at high DAM values
- **Threshold behavior**: Zero output until DAM reaches certain level

**Common Modifications:**
- Usually left linear and matching base multiplier
- Could be adjusted for specific knock-recovery behaviors
- Advanced tuning technique - not commonly modified

**Interaction with Base Multiplier:**
Since both multipliers shape the DAM response, changes should be considered together. A conservative adder multiplier can offset an aggressive base multiplier.

## Warnings

⚠️ **Knock System Interface**: Part of knock protection - modifications affect engine safety.

⚠️ **Complex Interaction**: Changes interact with base multiplier and both adder tables.

⚠️ **1D Table Format**: Actual values may not display in 2D preview.

**Safe Practices:**
- Keep relationship to base multiplier understood
- Test across full DAM range after modifications
- Monitor knock carefully - adder can contribute significant timing

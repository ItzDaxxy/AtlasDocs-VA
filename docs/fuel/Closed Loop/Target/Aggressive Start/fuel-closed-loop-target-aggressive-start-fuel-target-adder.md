# Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder - 2018 - LF9C102P.csv` |

## Description

This table defines an additional fuel target adder during Aggressive Start conditions, indexed by calculated load and RPM. It provides extra enrichment on top of the base Aggressive Start targets.

**Purpose:**
- Adds enrichment to Aggressive Start base targets
- Allows location-specific additional enrichment
- Currently set to 0.0 across table (no additional enrichment)

**Value Interpretation:**
- Values represent lambda adder (enrichment amount)
- 0.0 = no additional enrichment (use base Aggressive Start targets only)
- Positive values would add further enrichment
- Stock table is all zeros - adder functionality available but unused

## Axes

### X-Axis

- **Parameter**: Fuel - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 2.5800
- **Points**: 16

### Y-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: RPM
- **Range**: 700.0000 to 6400.0000
- **Points**: 16

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  700.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Adder Application:**
```
Final Aggressive Start Target = Base Target + Adder (this table)
```

Since all values are 0.0, the base Aggressive Start targets are used directly without modification.

**Why All Zeros:**
Stock calibration determined base Aggressive Start targets are sufficient. This table provides flexibility to add enrichment at specific RPM/load points if needed.

**Update Rate:** Calculated during Aggressive Start operation.

## Related Tables

- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target](./fuel-closed-loop-target-aggressive-start-fuel-target.md)**: Base targets (modified by this adder)
- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder Activation](./fuel-closed-loop-target-aggressive-start-fuel-target-adder-activation.md)**: Controls when adder is active
- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Max Activation](./fuel-closed-loop-target-aggressive-start-coolant-max-activation.md)**: Temperature conditions

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Final lambda target
- **Coolant Temperature (°C)**: Aggressive Start activation condition

## Tuning Notes

**Stock Behavior:** Stock table is all zeros - no additional enrichment beyond base Aggressive Start targets.

**Potential Use Cases:**
- If cold starts are rough at specific RPM/load, could add enrichment there
- Provides fine-tuning capability without changing base targets
- More targeted than modifying entire Aggressive Start table

**Common Modifications:**
- Generally left at zero if base targets are adequate
- Could be used to address specific cold-start stumble issues

## Warnings

⚠️ **Stacks with Base**: Any non-zero values add to already-rich Aggressive Start targets.

⚠️ **Spark Plug Fouling**: Adding more enrichment to already-rich cold operation risks fouling.

**Safe Practices:**
- Only add enrichment if specific cold-start issues exist
- Make small adjustments
- Monitor for over-rich conditions

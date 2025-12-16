# Fuel - Closed Loop - Lean Limit/Adder - Main - Lean Limit/Adder (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | LAMBDA |
| **Source File** | `Adder (TGV Open) - 2018 - LF9C102P.csv` |

## Description

This table defines a lean limit adder for closed-loop operation with TGV (Tumble Generator Valves) open, indexed by calculated load and coolant temperature. It provides enrichment during cold operation and at higher loads.

**Purpose:**
- Adds enrichment to closed-loop targets under specific conditions
- Cold-temperature enrichment during warm-up
- Load-based enrichment for protection

**Value Interpretation:**
- Values in lambda (added to base target to create richer mixture)
- 0.0 = no enrichment adder
- 0.3675 / 0.7344 = significant enrichment (makes mixture richer)
- Higher values at cold temps and higher loads

**Understanding the Adder:**
This value is subtracted from lambda target to create richer mixture:
- Base target: 1.0λ
- Adder: 0.7344
- Effective target: ~0.27λ (very rich - likely calculation differs)

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 0.9030
- **Points**: 8

### Y-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

## Cell Values

- **Unit**: LAMBDA
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.8385 |     0.9030 |
--------------------------------------------------------------------------------------------------------------------
  -40.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
  -30.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
  -20.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
  -10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |     0.7344 |     0.7344 |
   10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.3675 |     0.3675 |     0.7344 |
   20.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |
   30.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev (limited range 0.129-0.903)
- **Y-Axis (Coolant Temp)**: Engine coolant temperature

**Adder Application:**
The value modifies the effective lambda target to provide enrichment:
- Active during cold operation (-40 to -10°C): High enrichment across all loads
- Transitions through warm-up: Enrichment decreases as temp increases
- Warm operation (30°C+): Only high-load enrichment remains

**Table Pattern:**
- Cold (-40 to -20°C): 0.7344 across all loads
- Cold-warm transition (-10 to 20°C): Progressive reduction
- Warm (30°C+): Only highest load (0.903 g/rev) retains enrichment

**Update Rate:** Calculated continuously during closed-loop operation.

## Related Tables

- **[Fuel - Closed Loop - Lean Limit/Adder - Main (TGV Closed)](./fuel-closed-loop-lean-limitadder-main-lean-limitadder-tgv-closed.md)**: Same function when TGV closed
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open)](./fuel-closed-loop-target-low-egr-target-base-tgv-open.md)**: Base lambda targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **Coolant Temperature (°C)**: Y-axis input
- **Command Fuel Final (λ)**: Resulting target with adder
- **TGV Position**: Should be open when this table active

## Tuning Notes

**Stock Behavior:** Stock provides cold-start enrichment and high-load protection through this adder mechanism.

**Cold Start Function:**
At very cold temps, significant enrichment is added to compensate for poor fuel vaporization. This decreases as engine warms.

**Common Modifications:**
- Generally left at stock for proper warm-up behavior
- May adjust if cold-start is too rich or too lean
- High-load enrichment at warm temps protects during part-throttle boost

## Warnings

⚠️ **Cold Operation Critical**: This adder ensures proper cold operation. Incorrect values cause cold-start issues.

⚠️ **Combined with Base Targets**: Final lambda = Base Target modified by this adder. Changes compound.

**Safe Practices:**
- Test cold starts at various temperatures if modifying
- Verify smooth warm-up behavior

# Fuel - Closed Loop - Lean Limit/Adder - Alternate (maybe high load) - Lean Limit/Adder (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | LAMBDA |
| **Source File** | `Adder (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

This table defines an alternate lean limit adder for closed-loop operation with TGV (Tumble Generator Valves) closed, indexed by calculated load and coolant temperature. Unlike the main lean limit adder, this table includes negative values at warmer temperatures, suggesting it provides slightly leaner targets under specific high-load conditions.

**Purpose:**
- Alternate enrichment adder for specific operating conditions
- Cold-temperature enrichment during warm-up (similar to main adder)
- Allows slightly leaner operation at warm temps (-0.0507λ adjustment)
- Likely active during sustained higher-load closed-loop operation

**Value Interpretation:**
- Positive values (0.7344, 0.3675) = enrichment (richer mixture)
- Zero values = no modification to base targets
- Negative values (-0.0507) = lean adjustment (leaner mixture)
- This table uniquely allows both enrichment AND lean adjustment

**"Alternate" Table Context:**
The "alternate (maybe high load)" naming suggests this table is selected under different conditions than the main lean limit adder - possibly during sustained moderate-load operation where the ECU prioritizes fuel economy over cold-start protection.

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
   10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.3675 |     0.3675 |     0.3675 |
   20.0000 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |
   30.0000 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |    -0.0507 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (Coolant Temp)**: Engine coolant temperature

**Table Pattern Analysis:**
- **Extreme Cold (-40 to -20°C)**: 0.7344λ enrichment across all loads
- **Cold Transition (-10 to 0°C)**: Enrichment only at higher loads
- **Cool (10°C)**: Reduced enrichment (0.3675) at higher loads
- **Warm (20°C+)**: NEGATIVE values (-0.0507) = slight lean adjustment

**Key Difference from Main Adder:**
The main lean limit adder has zero values at warm temps. This alternate table has -0.0507λ, allowing slightly leaner operation. This suggests:
- Main adder: Used during warm-up and normal operation
- Alternate adder: Used during sustained operation where leaner targets acceptable

**Update Rate:** Calculated continuously during closed-loop operation with TGV closed under alternate conditions.

## Related Tables

- **[Fuel - Closed Loop - Lean Limit/Adder - Alternate (TGV Open)](./fuel-closed-loop-lean-limitadder-alternate-maybe-high-load-lean-limitadder-tgv-open.md)**: Same function when TGV open
- **[Fuel - Closed Loop - Lean Limit/Adder - Main (TGV Closed)](./fuel-closed-loop-lean-limitadder-main-lean-limitadder-tgv-closed.md)**: Primary lean limit adder
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-low-egr-target-base-tgv-closed.md)**: Base lambda targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **Coolant Temperature (°C)**: Y-axis input
- **Command Fuel Final (λ)**: Resulting target with adder
- **TGV Position**: Should be 0% (closed) when this table active

## Tuning Notes

**Stock Behavior:** Stock provides temperature-based enrichment similar to main adder, plus slight lean adjustment at warm temps for improved fuel economy under sustained operation.

**Unique Feature - Lean Adjustment:**
The -0.0507λ at warm temps makes final targets slightly leaner. On a base target of 1.0λ, this would create ~1.05λ (slightly lean). This improves fuel economy during sustained closed-loop operation.

**Common Modifications:**
- Could increase negative values for more fuel economy (risk: lean misfire)
- Could zero-out negative values to match main adder behavior
- Cold enrichment values usually left at stock

**When This Table is Active:**
Exact activation conditions are ECU-internal, but likely involves:
- Sustained operation at moderate loads
- Stable closed-loop control active
- Engine fully warmed and stable

## Warnings

⚠️ **Lean Adjustment Risk**: Negative values create leaner-than-stoich targets. Too lean causes misfire.

⚠️ **Table Selection Unknown**: Exact conditions that select this table vs main adder are ECU-internal.

⚠️ **TGV State Dependency**: Only applies when TGVs are closed (tumble position).

**Safe Practices:**
- Don't increase negative values beyond -0.1λ
- Test for misfire at part-throttle cruise conditions
- Monitor long-term fuel trims for signs of excessive lean

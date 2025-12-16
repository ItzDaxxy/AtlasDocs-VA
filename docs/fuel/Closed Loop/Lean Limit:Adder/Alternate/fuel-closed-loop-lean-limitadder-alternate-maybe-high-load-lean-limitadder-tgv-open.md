# Fuel - Closed Loop - Lean Limit/Adder - Alternate (maybe high load) - Lean Limit/Adder (TGV Open)

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

This table defines an alternate lean limit adder for closed-loop operation with TGV (Tumble Generator Valves) open, indexed by calculated load and coolant temperature. Unlike the main lean limit adder, this table includes negative values at warmer temperatures, allowing slightly leaner targets under specific sustained operating conditions.

**Purpose:**
- Alternate enrichment adder for specific operating conditions
- Cold-temperature enrichment during warm-up (similar to main adder)
- Allows slightly leaner operation at warm temps (-0.0507λ adjustment)
- Active during sustained higher-load closed-loop operation with TGV open

**Value Interpretation:**
- Positive values (0.7344, 0.3675) = enrichment (richer mixture)
- Zero values = no modification to base targets
- Negative values (-0.0507) = lean adjustment (leaner mixture)
- This table uniquely allows both enrichment AND lean adjustment

**TGV Open Context:**
When TGVs are open (higher loads, WOT), airflow is maximized. This alternate table provides appropriate fuel adjustments for sustained TGV-open operation, balancing cold-start needs with warm-operation fuel economy.

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
- **Cold Transition (-10 to 0°C)**: Enrichment only at higher loads (≥0.645 g/rev)
- **Cool (10°C)**: Reduced enrichment (0.3675) at higher loads
- **Warm (20°C+)**: NEGATIVE values (-0.0507) = slight lean adjustment

**Identical to TGV Closed Version:**
This table has identical values to the TGV Closed alternate adder, suggesting the alternate operating mode doesn't differentiate based on TGV position - it applies the same adjustments regardless of tumble valve state.

**Key Difference from Main Adder:**
The main lean limit adder (TGV Open) has zero values at warm temps. This alternate table has -0.0507λ at warm temps, allowing slightly leaner-than-stoich targets for improved fuel economy.

**Update Rate:** Calculated continuously during closed-loop operation with TGV open under alternate conditions.

## Related Tables

- **[Fuel - Closed Loop - Lean Limit/Adder - Alternate (TGV Closed)](./fuel-closed-loop-lean-limitadder-alternate-maybe-high-load-lean-limitadder-tgv-closed.md)**: Same function when TGV closed
- **[Fuel - Closed Loop - Lean Limit/Adder - Main (TGV Open)](./fuel-closed-loop-lean-limitadder-main-lean-limitadder-tgv-open.md)**: Primary lean limit adder
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open)](./fuel-closed-loop-target-low-egr-target-base-tgv-open.md)**: Base lambda targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **Coolant Temperature (°C)**: Y-axis input
- **Command Fuel Final (λ)**: Resulting target with adder
- **TGV Position**: Should be 100% (open) when this table active

## Tuning Notes

**Stock Behavior:** Stock provides temperature-based enrichment similar to main adder, plus slight lean adjustment at warm temps for improved fuel economy during sustained TGV-open operation.

**Lean Adjustment Purpose:**
The -0.0507λ at warm temps nudges final targets slightly lean of stoichiometric. Combined with a 1.0λ base target, this yields ~1.05λ - slightly lean but within catalytic converter efficiency window.

**Common Modifications:**
- TGV delete: May need to adjust if TGV position fixed
- Could increase negative values for more fuel economy (test carefully)
- Could zero-out negative values if running slightly rich is preferred
- Cold enrichment values usually left at stock

**When This Table is Active:**
Exact activation conditions are ECU-internal, but likely:
- Sustained moderate-to-higher load operation
- Stable closed-loop control established
- Engine fully warmed
- May be time-based or stability-based selection

## Warnings

⚠️ **Lean Adjustment Risk**: Negative values create leaner-than-stoich targets. Excessive lean causes misfire and catalyst damage.

⚠️ **Table Selection Uncertainty**: Exact conditions for alternate vs main adder are not fully documented.

⚠️ **TGV Delete Consideration**: If TGV deleted (fixed open), only TGV Open tables may be relevant.

**Safe Practices:**
- Don't increase negative values significantly beyond stock
- Test for misfire at cruise conditions
- Monitor catalyst efficiency if modifying lean adjustments
- Verify smooth part-throttle operation

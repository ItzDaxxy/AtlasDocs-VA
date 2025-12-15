# Fuel - Closed Loop - Lean Limit/Adder - Main - Lean Limit/Adder (TGV Closed)

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

This table defines a lean limit adder for closed-loop operation with TGV (Tumble Generator Valves) closed, indexed by calculated load and coolant temperature. Provides cold-start enrichment and load-based protection when TGVs are in tumble-generating position.

**Purpose:**
- Adds enrichment during cold operation with TGV closed
- Temperature-based enrichment during warm-up
- Load-based enrichment at higher loads

**Value Interpretation:**
- Values in lambda (enrichment adder)
- 0.0 = no enrichment adder
- 0.3675 / 0.7344 = enrichment amounts
- Active at cold temps and certain load conditions

**TGV Closed Context:**
When TGVs are closed (idle, light load), tumble improves mixing. This table provides appropriate enrichment for these conditions during warm-up.

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
  -10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |     0.7344 |
   10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.3675 |     0.3675 |     0.7344 |
   20.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |
   30.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.7344 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (Coolant Temp)**: Engine coolant temperature

**Comparison to TGV Open Table:**
Similar structure but slightly different activation. At -10°C:
- TGV Open: Enrichment only at loads ≥0.645 g/rev
- TGV Closed: Enrichment at loads ≥0.516 g/rev
This suggests TGV closed operation needs enrichment at slightly lower loads.

**Update Rate:** Calculated continuously during closed-loop operation with TGV closed.

## Related Tables

- **[Fuel - Closed Loop - Lean Limit/Adder - Main (TGV Open)](./fuel-closed-loop-lean-limitadder-main-lean-limitadder-tgv-open.md)**: Same function when TGV open
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-low-egr-target-base-tgv-closed.md)**: Base lambda targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **Coolant Temperature (°C)**: Y-axis input
- **Command Fuel Final (λ)**: Resulting target with adder
- **TGV Position**: Should be 0% when this table active

## Tuning Notes

**Stock Behavior:** Stock provides temperature and load-based enrichment appropriate for TGV-closed combustion characteristics.

**TGV State Consideration:**
With TGV closed (better tumble), combustion may be more stable, but cold fuel atomization still challenges. Enrichment ensures adequate combustible mixture.

**Common Modifications:**
- TGV delete: This table may be irrelevant if TGV position fixed at open
- Generally left at stock for proper cold operation

## Warnings

⚠️ **TGV State Dependency**: Only applies when TGVs are closed.

⚠️ **Cold Start Critical**: Affects cold idle and light-load operation.

**Safe Practices:**
- Verify TGV operation correlates with table selection
- Test cold start and warm-up with modifications

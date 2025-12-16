# Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | LAMBDA |
| **Source File** | `Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

This table defines the closed-loop lambda target for Low EGR conditions with TGV (Tumble Generator Valves) in closed position, indexed by calculated load and RPM. These targets are used during low-load operation when TGVs are closed to enhance tumble for better combustion.

**Purpose:**
- Sets lambda targets for closed-loop fuel control
- Specific to Low EGR conditions with TGV closed
- Optimized for tumble-enhanced combustion at low loads

**Value Interpretation:**
- Values in lambda (λ)
- λ = 1.0 = stoichiometric (14.7:1 AFR gasoline)
- Some values at 1.001-1.002 = very slightly lean of stoichiometric
- Higher load values ~0.979 = mild enrichment

**TGV State:**
- TGV Closed = 0% open (tumble generation active)
- Used at idle and light loads for improved atomization
- Different targets than TGV open due to different combustion characteristics

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1294 to 2.5880
- **Points**: 16

### Y-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 700.0000 to 6400.0000
- **Points**: 16

## Cell Values

- **Unit**: LAMBDA
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1294 |     0.2588 |     0.3882 |     0.5176 |     0.6470 |     0.7764 |     0.9058 |     1.0352 |
--------------------------------------------------------------------------------------------------------------------
  700.0000 |     0.9979 |     0.9979 |     1.0020 |     1.0000 |     0.9990 |     0.9980 |     0.9990 |     0.9990 |
  800.0000 |     0.9979 |     0.9979 |     1.0020 |     1.0000 |     0.9990 |     0.9980 |     0.9990 |     0.9990 |
 1200.0000 |     1.0014 |     1.0014 |     1.0014 |     1.0000 |     0.9990 |     0.9980 |     0.9990 |     0.9990 |
 1600.0000 |     1.0007 |     1.0007 |     1.0000 |     1.0000 |     0.9990 |     0.9931 |     0.9931 |     0.9793 |
 2000.0000 |     1.0007 |     1.0000 |     1.0000 |     0.9970 |     0.9970 |     0.9931 |     0.9931 |     0.9793 |
 2400.0000 |     0.9980 |     0.9945 |     0.9945 |     0.9959 |     0.9959 |     0.9931 |     0.9931 |     0.9793 |
 2800.0000 |     0.9980 |     0.9945 |     0.9945 |     0.9959 |     0.9959 |     0.9931 |     0.9931 |     0.9793 |
 3200.0000 |     0.9980 |     0.9945 |     0.9945 |     0.9959 |     0.9959 |     0.9931 |     0.9931 |     0.9793 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Selection:**
This table is used when:
- Low EGR conditions are met
- TGVs are in closed position (tumble active)
- Engine is in closed-loop fuel control mode

**TGV Closed Benefits:**
When TGVs are closed:
- Air flow through smaller opening creates tumble
- Better fuel atomization and mixing
- Improved combustion at low loads
- May allow slightly different AFR targets

**Update Rate:** Calculated continuously during closed-loop operation.

## Related Tables

- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open)](./fuel-closed-loop-target-low-egr-target-base-tgv-open.md)**: Targets when TGV open
- **[Fuel - Closed Loop - Target - High EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-high-egr-target-base-tgv-closed.md)**: High EGR targets
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Primary closed-loop targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Resulting lambda target
- **A/F Sensor 1 (λ)**: Actual measured lambda
- **TGV Position**: Should be 0% when this table active

## Tuning Notes

**Stock Behavior:** Stock targets optimized for emissions and efficiency with tumble-enhanced combustion.

**Table Comparison (TGV Closed vs Open):**
With TGV closed (better mixing), some operating points run slightly lean (1.001-1.002λ) compared to TGV open. This reflects the improved combustion efficiency.

**Common Modifications:**
- TGV delete: This table becomes less relevant
- Generally left at stock for proper idle and light-load behavior

**TGV Delete Considerations:**
If TGVs removed/disabled, this table may still be referenced. Consider:
- Table may be unused if TGV position fixed at "open"
- Verify ECU is using correct table after TGV modifications

## Warnings

⚠️ **TGV Operation**: This table only applies when TGVs are closed. Verify TGV operation if experiencing issues.

⚠️ **Lean at Light Load**: Slightly lean targets (>1.0λ) acceptable at very light loads but monitor for misfires.

**Safe Practices:**
- Verify TGV operation matches expected table selection
- Keep idle targets near stoichiometric
- Monitor fuel trims for unexpected behavior

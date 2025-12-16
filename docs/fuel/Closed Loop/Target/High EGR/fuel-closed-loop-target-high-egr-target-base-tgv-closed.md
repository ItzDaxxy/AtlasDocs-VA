# Fuel - Closed Loop - Target - High EGR - Target Base (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | LAMBDA |
| **Source File** | `Fuel - Closed Loop - Target - High EGR - Target Base (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

This table defines the closed-loop lambda target for High EGR conditions with TGV (Tumble Generator Valves) in closed position, indexed by calculated load and RPM. These targets are used during low-load High EGR operation with tumble enhancement.

**Purpose:**
- Sets lambda targets for High EGR with TGV closed
- Optimized for tumble-enhanced combustion during EGR operation
- Used at idle and light loads where TGVs are closed

**Value Interpretation:**
- Values in lambda (λ)
- Values at 1.001-1.002 = very slightly lean of stoichiometric
- Values ~0.979 at higher loads = mild enrichment

**TGV Closed with EGR:**
When TGVs are closed and EGR is active:
- Enhanced tumble improves mixing of EGR-diluted charge
- May allow slightly lean targets due to better combustion
- Targets optimized for this specific combination

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
  700.0000 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     0.9990 |     0.9990 |
  800.0000 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     1.0010 |     0.9990 |     0.9990 |
 1200.0000 |     1.0010 |     1.0007 |     1.0000 |     0.9979 |     0.9986 |     0.9986 |     0.9990 |     0.9990 |
 1600.0000 |     1.0019 |     1.0007 |     1.0000 |     0.9979 |     0.9986 |     0.9986 |     0.9931 |     0.9793 |
 2000.0000 |     0.9997 |     0.9997 |     0.9986 |     0.9966 |     0.9979 |     0.9979 |     0.9931 |     0.9793 |
 2400.0000 |     0.9952 |     0.9952 |     0.9966 |     0.9959 |     0.9986 |     0.9972 |     0.9931 |     0.9793 |
 2800.0000 |     0.9952 |     0.9952 |     0.9966 |     0.9959 |     0.9986 |     0.9972 |     0.9931 |     0.9793 |
 3200.0000 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9931 |     0.9793 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Selection:**
This table is used when:
- High EGR flow conditions detected
- TGVs are closed (tumble active)
- Engine in closed-loop mode

**Combined Effect:**
TGV closed + EGR active:
- Tumble helps mix EGR with fresh air
- Better atomization in EGR-diluted charge
- May tolerate slightly lean mixture (1.001λ)

**Update Rate:** Calculated continuously during CL operation.

## Related Tables

- **[Fuel - Closed Loop - Target - High EGR - Target Base (TGV Open)](./fuel-closed-loop-target-high-egr-target-base-tgv-open.md)**: High EGR, TGV open
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-low-egr-target-base-tgv-closed.md)**: Low EGR, TGV closed
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Primary CL targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Resulting lambda target
- **TGV Position**: Should be 0% when this table active
- **EGR Duty Cycle (%)**: Indicates High EGR state

## Tuning Notes

**Stock Behavior:** Stock targets allow slightly lean operation at low loads with TGV closed due to improved mixing.

**Comparison to Low EGR:**
High EGR with TGV closed shows similar patterns to Low EGR TGV closed - slightly lean at idle, enriching at load.

**Common Modifications:**
- Generally left at stock unless EGR/TGV system modified
- TGV delete: This table may not be used
- EGR delete: This table irrelevant

## Warnings

⚠️ **Combined State**: This table only applies when BOTH High EGR AND TGV closed conditions exist.

⚠️ **Lean at Idle**: Slightly lean targets (1.001λ) require good combustion stability.

**Safe Practices:**
- Verify both EGR and TGV state when troubleshooting
- Monitor for misfires at light loads

# Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | LAMBDA |
| **Source File** | `Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open) - 2018 - LF9C102P.csv` |

## Description

This table defines the closed-loop lambda target for Low EGR conditions with TGV (Tumble Generator Valves) in open position, indexed by calculated load and RPM. These targets are used during normal warmed-up operation when the TGVs are open for maximum airflow.

**Purpose:**
- Sets lambda targets for closed-loop fuel control
- Specific to Low EGR operating conditions
- Used when TGVs are in open (full flow) position

**Value Interpretation:**
- Values in lambda (λ)
- λ = 1.0 = stoichiometric (14.7:1 AFR gasoline)
- Values ~0.995-0.998 = very slightly rich of stoichiometric
- Values ~0.963-0.979 = mild enrichment at higher loads

**TGV State:**
- TGV Open = 100% open for maximum airflow
- Open TGVs used during higher load/RPM operation
- Different targets than TGV closed to optimize combustion

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
  700.0000 |     0.9980 |     0.9980 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |
  800.0000 |     0.9980 |     0.9980 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |
 1200.0000 |     0.9980 |     0.9980 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |     0.9950 |
 1600.0000 |     0.9970 |     0.9970 |     0.9950 |     0.9931 |     0.9945 |     0.9945 |     0.9950 |     0.9950 |
 2000.0000 |     0.9970 |     0.9970 |     0.9931 |     0.9883 |     0.9903 |     0.9931 |     0.9952 |     0.9952 |
 2400.0000 |     0.9970 |     0.9970 |     0.9931 |     0.9903 |     0.9945 |     0.9959 |     0.9931 |     0.9931 |
 2800.0000 |     0.9950 |     0.9950 |     0.9931 |     0.9903 |     0.9945 |     0.9660 |     0.9633 |     0.9633 |
 3200.0000 |     0.9950 |     0.9950 |     0.9931 |     0.9903 |     0.9945 |     0.9660 |     0.9633 |     0.9633 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Selection:**
This table is used when:
- Low EGR conditions are met
- TGVs are in open position
- Engine is in closed-loop fuel control mode

**Lambda Target Application:**
The ECU uses this target for closed-loop feedback:
1. Look up target lambda from this table
2. Compare actual lambda (O2 sensor)
3. Adjust fuel trims to achieve target

**Update Rate:** Calculated continuously during closed-loop operation.

## Related Tables

- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-low-egr-target-base-tgv-closed.md)**: Targets when TGV closed
- **[Fuel - Closed Loop - Target - High EGR - Target Base (TGV Open)](./fuel-closed-loop-target-high-egr-target-base-tgv-open.md)**: High EGR targets
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Primary closed-loop targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Resulting lambda target
- **A/F Sensor 1 (λ)**: Actual measured lambda
- **TGV Position**: Should be open when this table active

## Tuning Notes

**Stock Behavior:** Stock targets provide emissions-compliant and efficient operation across the load/RPM range.

**Table Pattern:**
- Low load: Very close to stoichiometric (~0.998λ)
- Mid load: Slight enrichment (~0.993λ)
- High load: More enrichment (~0.963λ) for power and protection

**Common Modifications:**
- **Stoichiometric Focus**: Keeping 1.0λ at low load maintains catalyst efficiency
- **Power Focus**: Slightly richer at high load for cooling/power
- Generally left near stock for emissions compliance

## Warnings

⚠️ **Catalyst Health**: Running too rich in CL degrades catalyst over time.

⚠️ **Emission Compliance**: Modifying CL targets affects emissions.

**Safe Practices:**
- Keep low-load targets near stoichiometric for catalyst efficiency
- Mild enrichment at high load is acceptable
- Monitor long-term fuel trims for validation

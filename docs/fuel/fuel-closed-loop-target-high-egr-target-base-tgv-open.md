# Fuel - Closed Loop - Target - High EGR - Target Base (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | LAMBDA |
| **Source File** | `Fuel - Closed Loop - Target - High EGR - Target Base (TGV Open) - 2018 - LF9C102P.csv` |

## Description

This table defines the closed-loop lambda target for High EGR conditions with TGV (Tumble Generator Valves) in open position, indexed by calculated load and RPM. These targets are used when EGR flow is elevated.

**Purpose:**
- Sets lambda targets for closed-loop fuel control during High EGR
- Specific to conditions when EGR is actively flowing
- Used when TGVs are open for maximum airflow

**Value Interpretation:**
- Values in lambda (λ)
- λ = 1.0 = stoichiometric (14.7:1 AFR gasoline)
- Values ~0.998 = very near stoichiometric
- Values ~0.979 at higher loads = mild enrichment

**High EGR Conditions:**
EGR (Exhaust Gas Recirculation) is used to:
- Reduce NOx emissions
- Lower combustion temperatures
- Improve part-throttle efficiency
Different lambda targets may be needed with EGR active.

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
  700.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9960 |     0.9960 |
  800.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9960 |     0.9960 |
 1200.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9960 |     0.9960 |
 1600.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9960 |     0.9960 |
 2000.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9960 |     0.9960 |
 2400.0000 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9980 |     0.9793 |     0.9793 |
 2800.0000 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9862 |     0.9793 |     0.9793 |
 3200.0000 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9960 |     0.9793 |     0.9793 |     0.9793 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Selection:**
This table is used when:
- High EGR flow conditions are detected
- TGVs are in open position
- Engine is in closed-loop fuel control mode

**EGR Impact on Fueling:**
With EGR active, the intake charge contains exhaust gas. This:
- Displaces some fresh air
- Changes effective AFR calculation
- May warrant different lambda targets

**Update Rate:** Calculated continuously during closed-loop operation with High EGR.

## Related Tables

- **[Fuel - Closed Loop - Target - High EGR - Target Base (TGV Closed)](./fuel-closed-loop-target-high-egr-target-base-tgv-closed.md)**: High EGR, TGV closed targets
- **[Fuel - Closed Loop - Target - Low EGR - Target Base (TGV Open)](./fuel-closed-loop-target-low-egr-target-base-tgv-open.md)**: Low EGR targets
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Primary closed-loop targets

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Resulting lambda target
- **A/F Sensor 1 (λ)**: Actual measured lambda
- **EGR Duty Cycle (%)**: Indicates EGR flow amount

## Tuning Notes

**Stock Behavior:** Stock targets optimized for emissions with EGR active. Values stay near stoichiometric for catalyst efficiency.

**Table Pattern:**
The table shows uniform targets at low loads (~0.998λ), transitioning to slightly richer at higher loads (~0.979λ).

**Common Modifications:**
- EGR delete: These tables become less relevant
- Generally left at stock if EGR system functional
- Emissions compliance requires proper EGR fueling

## Warnings

⚠️ **EGR System Interaction**: This table assumes EGR is flowing. Targets may be inappropriate if EGR disabled.

⚠️ **Emission Compliance**: EGR is emissions equipment. Modifications affect emissions.

**Safe Practices:**
- Verify EGR state when troubleshooting fueling issues
- Keep targets near stoichiometric for catalyst health

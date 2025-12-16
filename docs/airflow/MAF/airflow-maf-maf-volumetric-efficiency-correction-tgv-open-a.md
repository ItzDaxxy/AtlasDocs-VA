# Airflow - MAF - MAF Volumetric Efficiency Correction (TGV Open) A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - MAF - MAF Volumetric Efficiency Correction (TGV Open) A - 2018 - LF9C102P.csv` |

## Description

Applies a volumetric efficiency (VE) correction factor when the Tumble Generator Valves (TGVs) are in the OPEN position. TGVs are butterfly valves in the intake runners that modify airflow characteristics for emissions and combustion efficiency.

When TGVs are open, the intake runners have maximum cross-sectional area, providing the highest flow capacity. This table compensates for the specific airflow behavior with TGVs open, which occurs during higher load and RPM conditions where maximum airflow is needed.

Values are in PERCENT representing the VE under TGV-open conditions. The ECU selects between TGV-open and TGV-closed VE tables based on the current TGV position.

## Axes

### X-Axis

- **Parameter**: Airflow - Turbo - Manifold Absolute Pressure
- **Unit**: PSI
- **Range**: 3.0216 to 34.7487
- **Points**: 16

### Y-Axis

- **Parameter**: Engine - RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7600.0000
- **Points**: 22

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     3.0216 |     4.5324 |     5.2878 |     6.0433 |     7.5541 |     9.0649 |    12.0865 |    15.1081 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    93.0084 |    73.4100 |    76.9745 |    85.5255 |    94.0796 |   106.9061 |    96.2158 |   100.4944 |
  800.0000 |    66.2506 |    65.1428 |    64.8254 |    64.5874 |    64.2548 |    64.0198 |    66.3452 |    75.1404 |
 1200.0000 |    62.8357 |    65.4968 |    66.2567 |    66.8274 |    67.6239 |    66.1804 |    72.1222 |    87.4817 |
 1600.0000 |    66.5741 |    69.8761 |    70.8191 |    71.5271 |    72.3816 |    72.7081 |    73.8922 |    82.8583 |
 2000.0000 |    70.1263 |    69.9463 |    69.8914 |    69.8547 |    70.1538 |    71.3745 |    74.3683 |    81.3538 |
 2400.0000 |    74.8688 |    74.9786 |    75.0122 |    75.0366 |    75.7721 |    76.6235 |    77.6123 |    81.8512 |
 2800.0000 |    68.8293 |    71.2494 |    71.9391 |    72.4579 |    73.0804 |    73.3307 |    72.8912 |    79.5349 |
 3200.0000 |    68.6188 |    70.6055 |    71.1731 |    71.6003 |    72.4854 |    73.4528 |    74.0021 |    80.4047 |
```

## Functional Behavior

The ECU performs 2D interpolation using MAP and RPM when TGVs are open:

1. **TGV State Check**: ECU determines TGV position
2. **If TGVs Open**: Use this table
3. **Table Lookup**: 2D interpolation for VE percentage
4. **Airflow Correction**: Applied to MAF reading

**TGV Operation:**
- TGVs OPEN: Maximum flow, used at higher loads
- TGVs CLOSED: Restricted flow, creates tumble for emissions
- ECU controls TGV position based on operating conditions

**Typical TGV-Open Conditions:**
- Higher RPM (above ~2500-3500 RPM)
- Higher load/throttle position
- Boost conditions

## Related Tables

- **Airflow - MAF - MAF VE Correction (TGV Closed) A**: VE when TGVs closed
- **Airflow - MAF - MAF VE Correction B**: Alternative VE table
- **AVCS - TGV Control**: TGV position control
- **Fuel - Target AFR**: Uses corrected airflow

## Related Datalog Parameters

- **MAP (PSI/kPa)**: X-axis input
- **Engine RPM**: Y-axis input
- **TGV Position**: Determines table selection
- **MAF (g/s)**: Input to be corrected

## Tuning Notes

**Common Modifications:**
- TGV delete requires recalibration
- Intake modifications need TGV-open VE adjustment
- This table used for most high-load operation

**TGV Delete Tuning:**
- With TGVs deleted, this table used exclusively
- Copy to TGV-closed table or blend tables
- Ensure consistent VE across operating range

**Considerations:**
- TGV-open represents maximum intake flow potential
- Values typically higher than TGV-closed at same MAP/RPM
- Critical for full-load fueling accuracy

## Warnings

- Incorrect VE causes AFR errors at high load
- TGV delete requires comprehensive retuning
- Lean conditions at boost are engine-damaging
- Verify AFR across full operating range after changes

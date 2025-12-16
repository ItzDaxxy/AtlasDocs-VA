# Airflow - MAF - MAF Volumetric Efficiency Correction B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - MAF - MAF Volumetric Efficiency Correction B - 2018 - LF9C102P.csv` |

## Description

Applies a volumetric efficiency (VE) correction factor to the calculated airflow based on manifold pressure and RPM. This table compensates for the difference between theoretical airflow (based on MAF sensor reading) and actual cylinder filling efficiency.

Values are in PERCENT representing the VE - how efficiently the engine fills its cylinders. At low MAP (vacuum), VE is lower due to throttling losses. At higher MAP (boost), VE can exceed 100% due to forced induction. The FA20DIT typically shows VE values from ~55% at low load/idle to 85%+ at high boost.

This is one of multiple VE correction tables - "B" variant may be used under specific operating conditions or as an alternative calibration.

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
  400.0000 |    54.2755 |    63.0310 |    65.5304 |    67.7734 |    70.0317 |    71.4630 |    73.0316 |    73.9014 |
  800.0000 |    54.2755 |    63.0310 |    65.5304 |    67.7734 |    70.0317 |    71.4630 |    73.0316 |    73.9014 |
 1200.0000 |    57.5592 |    65.8539 |    68.2251 |    70.4132 |    72.4915 |    74.6277 |    75.3357 |    74.8840 |
 1600.0000 |    64.8987 |    70.6970 |    76.7242 |    78.0792 |    81.9550 |    82.3212 |    83.1146 |    84.6924 |
 2000.0000 |    64.5996 |    69.5679 |    72.2260 |    74.7345 |    77.3285 |    79.3671 |    81.1310 |    84.1888 |
 2400.0000 |    64.5996 |    73.3978 |    75.6409 |    78.5797 |    81.9733 |    84.5581 |    86.0504 |    87.4969 |
 2800.0000 |    59.9976 |    66.6992 |    69.7327 |    73.2483 |    77.5757 |    80.4596 |    82.3395 |    83.4473 |
 3200.0000 |    62.0972 |    66.6992 |    69.3512 |    70.1721 |    76.5045 |    78.0487 |    82.2052 |    83.6060 |
```

## Functional Behavior

The ECU performs 2D interpolation using MAP and RPM:

1. **Inputs**: Manifold Absolute Pressure (PSI), Engine RPM
2. **Table Lookup**: 2D interpolation for VE percentage
3. **Airflow Correction**: Calculated Mass = MAF × (VE/100)

**VE Calculation Purpose:**
```
Corrected Airflow = MAF Reading × VE Correction Factor
```

**VE Patterns:**
- Low MAP + Low RPM: Lower VE (~55-65%)
- High MAP + Mid RPM: Higher VE (~80-85%)
- Boost conditions: VE can exceed 100%

## Related Tables

- **Airflow - MAF - MAF VE Correction (TGV Open) A**: TGV-specific VE
- **Airflow - MAF - MAF VE Correction (TGV Closed) A**: TGV closed VE
- **Sensors - Mass Airflow**: MAF sensor calibration
- **Fuel - Target AFR**: Uses corrected airflow for fueling

## Related Datalog Parameters

- **MAP (PSI/kPa)**: X-axis input
- **Engine RPM**: Y-axis input
- **MAF (g/s)**: Raw MAF sensor reading
- **Calculated Load**: Derived from corrected airflow

## Tuning Notes

**Common Modifications:**
- Adjust for intake modifications that change airflow characteristics
- Tune alongside fuel trims to achieve stoichiometric at cruise
- Required recalibration with intake/turbo upgrades

**VE Tuning Process:**
1. Log fuel trims at various MAP/RPM points
2. Adjust VE to bring trims toward zero
3. Positive trim = increase VE, Negative trim = decrease VE
4. Iterate until trims are within ±5%

**Considerations:**
- VE affects both fueling and load calculation
- Incorrect VE causes consistent AFR errors
- VE changes with intake/exhaust modifications

## Warnings

- Incorrect VE causes lean or rich conditions
- Lean conditions at high boost are extremely dangerous
- Always verify AFR after VE modifications
- VE should be tuned at steady-state conditions
- Monitor knock when increasing VE values

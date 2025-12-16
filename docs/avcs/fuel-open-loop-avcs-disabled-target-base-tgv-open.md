# Fuel - Open Loop - AVCS Disabled - Target Base (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Disabled - Target Base (TGV Open) - 2017 - RogueWRX.csv` |

## Description

Defines open-loop fuel targets (AFR equivalence ratio) for conditions when AVCS is DISABLED AND TGVs are OPEN. This combination typically occurs during warm-up if TGVs open before AVCS activates, or during AVCS system faults at higher loads.

Values are in AFR Equivalence Ratio where 1.0 = stoichiometric (14.7:1 AFR). The table shows similar values to other fuel tables, with stoichiometric at low loads and richer at high loads.

AVCS-disabled with TGV-open is a fallback condition where cam timing is fixed but intake restriction is removed for higher airflow needs.

## Axes

### X-Axis

- **Parameter**: CALC LOAD
- **Unit**: G_PER_REV
- **Range**: 0.9058 to 2.9762
- **Points**: 20

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 9200.0000
- **Points**: 24

## Cell Values

- **Unit**: AFR_EQ
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.9058 |     1.0352 |     1.2293 |     1.2940 |     1.5528 |     1.8116 |     2.0704 |     2.3292 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
  800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
 1200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
 1600.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.2773 |     1.3438 |     1.3008 |
 2000.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1719 |     1.1328 |     1.3008 |
 2400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1914 |
 2800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0508 |     1.1484 |     1.1875 |     1.1992 |
 3200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1992 |     1.2305 |
```

## Functional Behavior

The ECU performs 2D interpolation based on calculated load and RPM:

1. **AVCS Check**: AVCS system is DISABLED
2. **TGV Check**: TGVs are in OPEN position
3. **Table Selection**: Use this AVCS-disabled TGV-open fuel map
4. **Target Lookup**: 2D interpolation for target AFR equivalence
5. **Fueling**: Injector pulse width calculated to achieve target

**AVCS Disabled + TGV Open:**
- May occur during warm-up transition
- AVCS fault with high load demand
- Cams fixed, but TGVs opened for airflow

## Related Tables

- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)**: AVCS enabled variant
- **Fuel - Open Loop - AVCS Disabled - Target Base (TGV Closed)**: TGV closed variant
- **Ignition - Primary - AVCS Disabled - TGV Open**: Companion timing table

## Related Datalog Parameters

- **Target AFR**: Output from this table
- **Actual AFR**: Measured via wideband
- **AVCS Status**: Disabled for this table
- **TGV Position**: Open for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Fallback Operation:**
- Used when AVCS cannot actuate
- Fixed cam timing limits optimization
- TGVs open for maximum airflow

**Diagnostic Considerations:**
- Frequent use indicates AVCS issue
- Check oil pressure and AVCS solenoids
- AVCS fault codes should be investigated

## Warnings

- Prolonged AVCS-disabled operation is suboptimal
- Power and efficiency reduced without AVCS
- Check for AVCS fault codes if persistent
- Cold weather extends AVCS-disabled operation
- AVCS solenoid or wiring faults require repair

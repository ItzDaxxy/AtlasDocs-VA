# Fuel - Open Loop - AVCS Enabled - Target Base (Low DAM)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Enabled - Target Base (Low DAM) - 2017 - RogueWRX.csv` |

## Description

Defines open-loop fuel targets (AFR equivalence ratio) for conditions when AVCS is enabled AND DAM (Dynamic Advance Multiplier) is low due to detected knock. This is a protective fuel map that provides richer targets when the engine is experiencing knock.

Values are in AFR Equivalence Ratio where 1.0 = stoichiometric (14.7:1 AFR) and values >1.0 indicate richer mixtures. The table shows richer targets (1.3-1.4) at higher loads, providing knock protection through additional fuel.

This table is activated when DAM drops below the threshold specified in "Low DAM Threshold" - typically triggered by sustained knock activity requiring protective enrichment.

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
  400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
  800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
 1200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1016 |     1.3984 |     1.3984 |     1.3984 |     1.3984 |
 1600.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1172 |     1.1602 |     1.1797 |     1.3008 |     1.3008 |
 2000.0000 |     1.0000 |     1.0000 |     1.0508 |     1.1172 |     1.2109 |     1.2500 |     1.2813 |     1.3086 |
 2400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1094 |     1.1406 |     1.3008 |     1.3008 |     1.3789 |
 2800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0195 |     1.1016 |     1.1914 |     1.2891 |     1.3984 |
 3200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0313 |     1.1172 |     1.1992 |     1.2813 |     1.3516 |
```

## Functional Behavior

The ECU performs 2D interpolation based on calculated load and RPM:

1. **DAM Check**: ECU monitors Dynamic Advance Multiplier
2. **AVCS Check**: AVCS must be enabled
3. **Table Selection**: If DAM below threshold, use this table
4. **Target Lookup**: 2D interpolation for target AFR equivalence
5. **Fueling**: Injector pulse width calculated to achieve target

**Low DAM Protection:**
- DAM drops when knock is detected
- Low DAM = sustained knock activity
- Richer fuel provides knock protection
- Additional cooling effect from extra fuel

## Related Tables

- **Fuel - Open Loop - AVCS Enabled - Low DAM Threshold**: Activates this table
- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)**: Standard table
- **Ignition - Primary - AVCS Enabled**: Timing also affected by DAM

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Triggers table selection
- **Target AFR**: Output from this table
- **Actual AFR**: Measured via wideband
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Low DAM Strategy:**
- Richer than standard fuel targets
- Provides knock protection margin
- Additional fuel cools combustion

**Stock Threshold Note:**
- Stock DAM threshold is 1.0 (effectively never activated)
- Lower threshold to enable this protection (e.g., 0.9)
- Provides safety net during knock events

**Typical Values:**
- Higher equivalence ratio than standard
- More enrichment at high load/boost
- Conservative for engine protection

## Warnings

- Low DAM indicates knock is being detected
- Address root cause of knock (fuel, timing, boost)
- This table provides protection, not a solution
- Monitor knock count and DAM regularly
- Persistent low DAM requires investigation

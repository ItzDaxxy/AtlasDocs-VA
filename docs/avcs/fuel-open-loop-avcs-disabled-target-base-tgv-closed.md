# Fuel - Open Loop - AVCS Disabled - Target Base (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Disabled - Target Base (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

Defines open-loop fuel targets (AFR equivalence ratio) for conditions when AVCS is DISABLED AND TGVs are CLOSED. AVCS may be disabled during cold start, warm-up, or when AVCS system faults are present.

Values are in AFR Equivalence Ratio where 1.0 = stoichiometric (14.7:1 AFR). The table shows similar values to the AVCS-enabled TGV-closed table, indicating fueling strategy is consistent regardless of AVCS status for these operating conditions.

AVCS-disabled conditions typically occur during cold start before oil pressure is sufficient to actuate the AVCS solenoids, or if the AVCS system has detected a fault.

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

1. **AVCS Check**: AVCS system is DISABLED (cold start or fault)
2. **TGV Check**: TGVs are in CLOSED position
3. **Table Selection**: Use this AVCS-disabled TGV-closed fuel map
4. **Target Lookup**: 2D interpolation for target AFR equivalence
5. **Fueling**: Injector pulse width calculated to achieve target

**AVCS Disabled Conditions:**
- Cold start (insufficient oil pressure)
- AVCS system fault codes present
- Warm-up period before AVCS activation
- Cams at default (0°) position

## Related Tables

- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed)**: AVCS enabled variant
- **Fuel - Open Loop - AVCS Disabled - Target Base (TGV Open)**: TGV open variant
- **Ignition - Primary - AVCS Disabled - TGV Closed**: Companion timing table

## Related Datalog Parameters

- **Target AFR**: Output from this table
- **Actual AFR**: Measured via wideband
- **AVCS Status**: Disabled for this table
- **TGV Position**: Closed for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**AVCS Disabled Strategy:**
- Used during cold start warm-up
- Cams at default position (no advance/retard)
- Fueling compensates for fixed cam timing

**Cold Start Considerations:**
- AVCS typically enables after ~30-60 seconds
- Oil pressure required for AVCS actuation
- Fueling must work without cam timing benefits

## Warnings

- Affects cold start fueling
- AVCS disabled limits engine efficiency
- Check AVCS status if table always active
- AVCS fault codes require diagnosis
- Cold weather extends AVCS-disabled period

# Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

Defines open-loop fuel targets (AFR equivalence ratio) for conditions when AVCS is enabled AND TGVs are CLOSED. This table is used during idle, light load, cold start, and cruise conditions where TGVs restrict intake flow to create tumble.

Values are in AFR Equivalence Ratio where 1.0 = stoichiometric (14.7:1 AFR) and values >1.0 indicate richer mixtures. The table shows stoichiometric targets (1.0) at low loads transitioning to richer targets (1.2-1.4) at higher loads for knock protection.

TGV-closed operation prioritizes emissions and fuel efficiency, with fueling optimized for the tumbling charge motion created by closed TGVs.

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

1. **AVCS Check**: AVCS system must be enabled
2. **TGV Check**: TGVs are in CLOSED position
3. **Table Selection**: Use this TGV-closed fuel map
4. **Target Lookup**: 2D interpolation for target AFR equivalence
5. **Fueling**: Injector pulse width calculated to achieve target

**TGV Closed Fueling:**
- Stoichiometric (1.0) at low loads
- Richer at high loads for protection
- Optimized for tumble combustion
- Emissions-focused at light load

## Related Tables

- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)**: TGV open variant
- **Fuel - Open Loop - AVCS Disabled - Target Base (TGV Closed)**: AVCS disabled variant
- **Ignition - Primary - AVCS Enabled - TGV Closed**: Companion timing table

## Related Datalog Parameters

- **Target AFR**: Output from this table
- **Actual AFR**: Measured via wideband
- **TGV Position**: Closed for this table
- **AVCS Status**: Enabled for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**TGV Closed Strategy:**
- Light load cells are stoichiometric for emissions
- Higher load cells richer for knock protection
- Tumble improves combustion efficiency

**Emissions Considerations:**
- TGV-closed operation during emissions testing
- Stoichiometric cells critical for catalyst efficiency
- Changes can affect emissions compliance

## Warnings

- TGV-closed fueling affects emissions
- Low-load cells must remain stoichiometric for catalyst
- Changes impact cold start and idle
- Verify AFR at all TGV-closed conditions
- TGV delete requires table reconsideration

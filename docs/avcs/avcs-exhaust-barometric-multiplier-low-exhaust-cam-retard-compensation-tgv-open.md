# AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Provides altitude-specific compensation for exhaust cam retard at LOW barometric pressure (high altitude) when TGVs are open. Unlike the sea-level compensation tables which are all zeros, this table contains NEGATIVE values that actively reduce exhaust cam retard at altitude.

The negative compensation values (-10° to -51° in the low-mid RPM range) reduce valve overlap at altitude. This accounts for the different exhaust scavenging dynamics and turbo behavior at higher elevations where air density is lower.

This is one of the few compensation tables with non-zero values in the stock calibration, indicating that altitude compensation for exhaust cam timing is actively used by the ECU.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1935 to 2.8380
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7200.0000
- **Points**: 18

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1935 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1100.0000 |     0.0000 |   -10.0014 |   -15.0007 |   -13.0010 |    -8.0016 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |   -25.0021 |   -37.0032 |   -33.0037 |   -19.0029 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |   -34.0036 |   -40.0055 |   -40.0055 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |   -34.0036 |   -51.0067 |   -42.0052 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |   -34.0036 |   -28.0016 |   -29.0043 |   -23.0023 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU uses this as an active altitude compensation:

1. **Barometric Check**: Low barometric pressure detected
2. **Base Target**: ECU gets base exhaust cam retard
3. **Compensation**: Negative values SUBTRACT from retard target
4. **Result**: Less exhaust retard at altitude

**Active Compensation:**
- Unlike sea-level tables (all zeros), this is active
- Negative values reduce exhaust cam retard
- Maximum reduction around -51° at specific RPM/load
- Effect concentrated in low-mid RPM range

**Formula:**
```
Altitude_Exhaust_Target = Base_Target + Negative_Compensation
```

## Related Tables

- **AVCS - Exhaust - Baro High - Compensation (TGV Open)**: Sea level (all zeros)
- **AVCS - Exhaust - Baro Low - Exhaust Cam Target (TGV Open)**: Base target
- **AVCS - Intake - Baro Low - Compensation**: Intake cam altitude compensation

## Related Datalog Parameters

- **AVCS Exhaust Target (°)**: Final target after compensation
- **Barometric Pressure (kPa)**: Triggers altitude compensation
- **Calculated Load (g/rev)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Understanding Altitude Compensation:**
- Negative values reduce exhaust retard at altitude
- Less overlap may suit thin air scavenging dynamics
- Stock calibration actively compensates 1200-2400 RPM range

**Altitude Tuning:**
- May need adjustment for altitude-frequent drivers
- Coordinate with intake cam altitude compensation
- Test at actual altitude conditions

**Pattern Analysis:**
- Zero at idle/very low RPM (stability priority)
- Maximum negative in low-mid RPM (spool range)
- Returns to zero at high RPM

## Warnings

- Active table - changes affect altitude operation
- Coordinate with intake cam altitude tables
- Test at actual altitude conditions
- Don't reduce altitude compensation without testing
- Monitor turbo behavior at altitude

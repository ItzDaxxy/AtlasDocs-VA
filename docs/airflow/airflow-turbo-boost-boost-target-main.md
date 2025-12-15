# Airflow - Turbo - Boost - Boost Target Main

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 19x16 |
| **Data Unit** | BAR |
| **Source File** | `Airflow - Turbo - Boost - Boost Target Main - 2018 - LF9C102P.csv` |

## Description

The primary boost target table that defines desired boost pressure based on requested torque and engine RPM. This is the main table controlling how much boost the turbocharger should produce at any given operating point.

Values are in BAR (gauge pressure relative to atmospheric):
- Negative values indicate vacuum (below atmospheric pressure)
- Zero is atmospheric pressure
- Positive values indicate boost pressure

The ECU uses this table to determine target manifold pressure, then commands the wastegate duty cycle to achieve that target. The boost control system (PI controller) works to minimize the error between actual and target boost.

## Axes

### X-Axis

- **Parameter**: Boost Control - Boost Targets/Limits - Requested Torque
- **Unit**: NM
- **Range**: 0.0000 to 420.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 800.0000 to 7600.0000
- **Points**: 19

## Cell Values

- **Unit**: BAR
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |   140.0000 |   160.0000 |   180.0000 |   200.0000 |   220.0000 |   240.0000 |   260.0000 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |    -0.5019 |    -0.0752 |    -0.0275 |    -0.0275 |    -0.0275 |    -0.0275 |    -0.0275 |    -0.0275 |
 1200.0000 |    -0.6619 |    -0.0219 |     0.0315 |     0.0635 |     0.0955 |     0.0955 |     0.0955 |     0.0955 |
 1600.0000 |    -0.7792 |    -0.0432 |     0.0101 |     0.0635 |     0.1381 |     0.2235 |     0.3621 |     0.3621 |
 2000.0000 |    -0.8219 |    -0.1179 |    -0.0454 |     0.0377 |     0.1267 |     0.2240 |     0.3515 |     0.4795 |
 2400.0000 |    -0.9189 |    -0.1658 |    -0.0752 |     0.0503 |     0.1594 |     0.2678 |     0.3572 |     0.4466 |
 2800.0000 |    -0.9088 |    -0.1285 |    -0.0219 |     0.0741 |     0.1915 |     0.2981 |     0.3966 |     0.5115 |
 3200.0000 |    -0.9195 |    -0.1285 |    -0.0219 |     0.0635 |     0.1595 |     0.2448 |     0.3301 |     0.4627 |
 3600.0000 |    -0.9285 |    -0.2139 |    -0.1285 |    -0.0219 |     0.0955 |     0.1808 |     0.2661 |     0.3835 |
```

## Functional Behavior

The ECU performs 2D interpolation using requested torque and RPM:

1. **Torque Request**: Driver input via accelerator pedal generates torque request
2. **Table Lookup**: ECU interpolates based on torque (X) and RPM (Y)
3. **Compensation**: Base target modified by IAT and barometric compensations
4. **Limit Check**: Final target compared against Boost Limit Base
5. **Control Output**: PI controller adjusts wastegate duty to achieve target

**Boost Control Loop:**
Target (this table) → Error = Target - Actual → PI Controller → Wastegate Duty → Actual Boost

## Related Tables

- **Airflow - Turbo - Boost - Boost Limit Base**: Maximum allowable boost
- **Airflow - Turbo - Boost - Barometric Compensation**: Altitude adjustment
- **Airflow - Turbo - Boost - IAT Compensation**: Hot intake air adjustment
- **Airflow - Turbo - Wastegate - Duty Initial/Maximum**: Wastegate control
- **Airflow - Turbo - PI Control**: Closed-loop boost control gains

## Related Datalog Parameters

- **Target Boost (psi/bar)**: Output from this table (after compensation)
- **Actual Boost (psi/bar)**: Measured manifold pressure
- **Boost Error**: Difference between target and actual
- **Wastegate Duty (%)**: Control output to achieve target
- **Requested Torque (Nm)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Understanding the Table:**
- Low torque request (left columns): Part throttle, cruise - shows vacuum/low boost
- High torque request (right columns): Full throttle - shows peak boost targets
- Low RPM (top rows): Turbo lag region, targets limited by turbo capability
- Mid-high RPM: Peak boost capability region

**Common Modifications:**
- Increase peak boost targets for more power (requires supporting mods)
- Adjust boost curve shape for different turbo characteristics
- Lower targets for reliability or fuel economy

**Modification Strategy:**
1. Start with conservative increases (+0.1 bar at a time)
2. Monitor knock, AFR, and EGT during testing
3. Ensure fuel system can support increased airflow
4. Verify turbo is capable of requested boost levels

**Stock Peak Boost:** ~0.9-1.0 bar (13-15 psi) at peak

## Warnings

- **CRITICAL**: Excessive boost causes engine damage (rod failure, ringland failure)
- Ensure fuel system, intercooler, and engine internals support target boost
- Higher boost requires richer AFR targets for safety
- Monitor knock feedback - any sustained knock requires reduced targets
- Turbo surge can occur if targets exceed turbo capability at low RPM
- Always verify with datalogging before street driving
- Consider altitude - boost targets may need reduction at elevation

# Throttle - Target Throttle - Alternate - B (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Alternate - B (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This is a secondary alternate target throttle table used when TGVs are CLOSED. As the deepest layer of throttle table redundancy (Alternate B + TGV Closed), this table serves as a failsafe within a failsafe, activated only under specific combinations of alternate mode selection and closed TGV operation. It defines throttle plate angles that account for restricted airflow while maintaining vehicle operation in degraded states.

## Axes

### X-Axis

- **Parameter**: Throttle - Requested Torque Ratio
- **Unit**: PERCENT
- **Range**: 0.0000 to 1.0000
- **Points**: 24

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 7800.0000
- **Points**: 22

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.0431 |     0.0863 |     0.1294 |     0.1725 |     0.2157 |     0.2627 |     0.3059 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     0.6744 |     1.3489 |     2.0233 |     2.6978 |     3.3722 |     4.0467 |     4.7211 |
 1200.0000 |     0.0000 |     1.1124 |     2.2248 |     3.3356 |     4.4480 |     5.5604 |     6.6728 |     7.7836 |
 1600.0000 |     0.0000 |     1.6175 |     3.2334 |     4.8508 |     6.4668 |     8.0919 |     9.7353 |    11.3085 |
 2000.0000 |     0.0000 |     2.5772 |     5.1545 |     7.3228 |     9.2027 |    11.1070 |    12.9427 |    14.6899 |
 2400.0000 |     0.0000 |     2.7222 |     5.4658 |     7.9377 |    10.1137 |    11.9081 |    13.7255 |    15.5627 |
 2800.0000 |     0.0000 |     3.6866 |     6.7704 |     9.1142 |    10.8476 |    12.6009 |    14.5052 |    16.1135 |
 3200.0000 |     0.0000 |     4.3687 |     8.0537 |    10.1030 |    11.7754 |    13.6065 |    15.3933 |    16.5362 |
 3600.0000 |     0.0000 |     5.5116 |     8.7434 |    10.9133 |    12.6772 |    14.4915 |    16.1624 |    17.3922 |
```

## Functional Behavior

The ECU interpolates this table using RPM and requested torque ratio when Alternate B mode is active and TGVs are closed. Like all TGV Closed tables, values must be higher than TGV Open counterparts to compensate for airflow restriction. This table represents the most conservative/failsafe throttle mapping in the ECU's hierarchy, potentially activated during multiple simultaneous fault conditions.

## Related Tables

- Throttle - Target Throttle - Alternate - B (TGV Open)
- Throttle - Target Throttle - Alternate - A (TGV Closed)
- Throttle - Target Throttle - Main - B (TGV Closed)
- All other Target Throttle table variants

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Throttle Table Selector/Mode
- Error Codes/Fault Status

## Tuning Notes

This is the most conservative table in the throttle system:
- Rarely if ever used in normal operation - reserved for severe fault conditions
- Typically calibrated very conservatively to ensure vehicle remains controllable
- Often copied from Alternate A TGV Closed or Main B TGV Closed tables
- Must balance TGV airflow restriction with failsafe operation requirements
- Difficult to test activation conditions without inducing multiple faults
If modifying, prioritize safety and predictability over performance - this table exists for emergency operation.

## Warnings

Most critical failsafe table in the throttle system:
- May only activate under severe multiple-fault scenarios
- Incorrect calibration could render vehicle inoperable when needed most
- Must properly compensate for closed TGV airflow restriction
- Too aggressive values could be dangerous in already-compromised vehicle states
- Too conservative values could prevent vehicle from reaching safe location
- Corrupted table could cause complete loss of throttle control in failsafe mode
Never delete or zero this table. Maintain conservative, functional calibration even if you never observe it being used. This is your last line of defense for maintaining vehicle control.

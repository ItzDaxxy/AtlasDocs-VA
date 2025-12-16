# Airflow - Turbo - Wastegate - Wastegate Duty Maximum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 17x14 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate Duty Maximum - 2018 - LF9C102P.csv` |

## Description

Defines the maximum wastegate duty cycle allowed based on requested torque and RPM. This table sets an upper limit on how much the wastegate solenoid can be commanded, regardless of what the boost control system requests.

Higher duty = more wastegate closure = more boost. This table caps the maximum duty to prevent over-boost conditions even if the Initial Duty + PI correction would command higher values.

The stock values show 10% minimum at low torque requests, increasing to higher percentages (40-60%+) at high torque requests where more boost is demanded.

## Axes

### X-Axis

- **Parameter**: Boost Control - Requested Torque
- **Unit**: NM
- **Range**: 200.0000 to 400.0000
- **Points**: 14

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 2000.0000 to 8000.0000
- **Points**: 17

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   200.0000 |   220.0000 |   240.0000 |   260.0000 |   280.0000 |   300.0000 |   320.0000 |   340.0000 |
--------------------------------------------------------------------------------------------------------------------
 2000.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    25.0000 |    35.0000 |
 2400.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    31.0000 |    44.0000 |
 2800.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    17.0000 |    29.0000 |    41.0000 |
 3200.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    20.0000 |    34.0000 |    44.0000 |
 3600.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    17.0000 |    33.0000 |    49.0000 |
 4000.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    18.0000 |    32.0000 |    45.0000 |
 4400.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    18.0000 |    34.0000 |    42.0000 |
 4800.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    21.0000 |    38.0000 |    52.0000 |    56.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using torque request and RPM:

1. **Torque/RPM Reading**: ECU monitors both values
2. **Table Lookup**: 2D interpolation determines maximum duty
3. **Duty Clamping**: Final Duty = MIN(Calculated Duty, Maximum)
4. **Output**: Clamped duty sent to wastegate solenoid

**Final Wastegate Duty = MIN(Initial + Compensations + PI, Maximum)**

## Related Tables

- **Airflow - Turbo - Wastegate - Duty Initial**: Base feedforward duty
- **Airflow - Turbo - Wastegate - IAT/Baro Compensation**: Duty adjustments
- **Airflow - Turbo - PI Control**: Closed-loop corrections
- **Airflow - Turbo - Boost - Target Main**: What boost is requested

## Related Datalog Parameters

- **Wastegate Duty (%)**: Final commanded duty
- **Wastegate Duty Maximum (%)**: Output from this table
- **Requested Torque (Nm)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Common Modifications:**
- Increase for larger turbo requiring more duty to spool
- May need higher values for external wastegate setups
- Coordinate with Initial Duty table for proper boost control

**Considerations:**
- Stock values are conservative for reliability
- Higher values needed for high-boost applications
- Ensure solenoid can handle commanded duty

## Warnings

- Excessive maximum duty can cause dangerous over-boost
- Setting too high removes boost control headroom
- Boost spikes can occur before PI control can react
- Monitor boost closely when increasing maximum values
- Verify turbo can handle resulting boost levels

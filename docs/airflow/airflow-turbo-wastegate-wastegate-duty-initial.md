# Airflow - Turbo - Wastegate - Wastegate Duty Initial

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 17x14 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate Duty Initial - 2018 - LF9C102P.csv` |

## Description

Defines the base (feedforward) wastegate duty cycle based on requested torque and RPM. This is the initial duty cycle the ECU commands to the wastegate solenoid before the PI controller makes closed-loop adjustments.

The wastegate controls boost by bleeding exhaust pressure away from the turbine. Higher duty cycle = more wastegate closure = more exhaust to turbine = more boost. Lower duty cycle = wastegate opens = less boost.

This table provides the "starting point" for boost control - if properly calibrated, it gets the wastegate close to the correct position immediately, allowing the PI controller to make only small corrections for fine-tuning. Values range from 0% (wastegate fully open, minimum boost) to higher percentages that hold the wastegate closed for target boost.

## Axes

### X-Axis

- **Parameter**: REQ TORQUE
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
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    15.0000 |    25.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    21.0000 |    34.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     7.0000 |    19.0000 |    31.0000 |
 3200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    10.0000 |    24.0000 |    34.0000 |
 3600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     7.0000 |    23.0000 |    39.0000 |
 4000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     8.0000 |    22.0000 |    35.0000 |
 4400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     8.0000 |    24.0000 |    32.0000 |
 4800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |    11.0000 |    28.0000 |    42.0000 |    46.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using requested torque and RPM:

1. **Torque/RPM Lookup**: ECU interpolates based on current torque request and RPM
2. **Initial Duty Output**: This value becomes the base wastegate command
3. **Compensation Applied**: IAT and barometric compensations modify the base
4. **PI Correction Added**: Closed-loop PI controller adds/subtracts based on boost error
5. **Final Duty**: Clamped to Wastegate Duty Maximum before output to solenoid

**Total Wastegate Duty = Initial (this table) × Compensations + PI Correction**

The table shows 0% at low torque requests (wastegate open, no boost needed) and increasing values at higher torque/RPM where boost is requested.

## Related Tables

- **Airflow - Turbo - Wastegate - Duty Maximum**: Upper limit for wastegate duty
- **Airflow - Turbo - Wastegate - IAT Compensation**: Temperature-based duty adjustment
- **Airflow - Turbo - Wastegate - Barometric Compensation**: Altitude adjustment
- **Airflow - Turbo - Wastegate - PWM Frequency**: Solenoid control frequency
- **Airflow - Turbo - Boost - Target Main**: The boost target this duty works to achieve
- **Airflow - Turbo - PI Control**: Closed-loop corrections added to initial duty

## Related Datalog Parameters

- **Wastegate Duty (%)**: Final commanded duty cycle
- **Wastegate Initial Duty (%)**: Output from this table specifically
- **Target Boost**: What the duty is trying to achieve
- **Actual Boost**: Measured manifold pressure
- **Requested Torque (Nm)**: X-axis input
- **Engine RPM**: Y-axis input

## Tuning Notes

**Purpose of Initial Duty:**
- Good initial duty = faster boost response, less PI correction needed
- Poor initial duty = sluggish boost, PI controller works harder, potential overshoot

**Common Modifications:**
- Increase values for larger turbo that needs more duty to spool
- Decrease values if experiencing boost overshoot
- Adjust curve shape to match turbo's efficiency characteristics
- Fine-tune for smoother boost buildup

**Tuning Strategy:**
1. Set PI gains to zero temporarily
2. Adjust this table until boost roughly matches target (open-loop)
3. Re-enable PI control for fine-tuning
4. Iterate between initial duty and PI gains for optimal response

**Larger Turbo Considerations:**
- May need higher initial duty across the board
- Response at low RPM is critical for spool characteristics
- May need to extend table values beyond stock range

## Warnings

- Excessive initial duty can cause dangerous boost spikes before PI can correct
- Too low initial duty causes sluggish boost response
- Always verify boost stays within safe limits during testing
- Monitor for boost creep (boost rising when it shouldn't)
- Ensure Maximum Duty table is properly configured as safety limit
- Test across full RPM range - behavior varies with exhaust flow
- Hot weather and high altitude require lower effective duty (compensations handle this)

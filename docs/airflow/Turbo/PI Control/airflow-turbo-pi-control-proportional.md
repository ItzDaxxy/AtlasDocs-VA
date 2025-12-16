# Airflow - Turbo - PI Control - Proportional

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Proportional - 2018 - LF9C102P.csv` |

## Description

Defines the proportional gain (P-term) of the closed-loop boost control PI controller based on boost error. The proportional term provides immediate correction proportional to the current error between target and actual boost.

Boost Error = Target Boost - Actual Boost (in Pascals)
- Negative error: Actual boost exceeds target (over-boost condition)
- Positive error: Actual boost below target (under-boost condition)

The output percentage adjusts wastegate duty: positive values increase duty (close wastegate = more boost), negative values decrease duty (open wastegate = less boost). This provides instantaneous response to boost deviations.

## Axes

### X-Axis

- **Parameter**: Boost Error
- **Unit**: PASCAL
- **Range**: -27000.0000 to 21000.0000
- **Points**: 9

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM | -27000.0000 | -13000.0000 | -5000.0000 | -3000.0000 |     0.0000 |  3000.0000 |  5000.0000 | 11000.0000 |
----------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using boost error:

1. **Error Calculation**: Boost Error = Target - Actual (Pascals)
2. **Table Lookup**: Interpolate P-term correction from error
3. **Duty Adjustment**: P-term added to wastegate duty

**PI Control Formula:**
```
Wastegate Duty = Initial Duty + P-term + I-term + Compensations
```

**Response Characteristics:**
- Large negative error (over-boost): Strong negative correction
- Small error near zero: Minimal correction
- Large positive error (under-boost): Strong positive correction

## Related Tables

- **Airflow - Turbo - PI Control - Integral Positive**: I-term for under-boost
- **Airflow - Turbo - PI Control - Integral Negative**: I-term for over-boost
- **Airflow - Turbo - PI Control - PI Activation Threshold**: When PI engages
- **Airflow - Turbo - Wastegate - Duty Initial**: Feedforward base duty
- **Airflow - Turbo - Boost - Target Main**: Target boost values

## Related Datalog Parameters

- **Boost Error (Pa/kPa)**: X-axis input
- **Wastegate Duty (%)**: Output including this correction
- **Target Boost (bar)**: Used for error calculation
- **Actual Boost (bar)**: Used for error calculation

## Tuning Notes

**Common Modifications:**
- Increase gain for faster boost response
- Decrease gain to reduce boost oscillation
- Tune in conjunction with I-terms for stability

**P-Term Tuning Guidelines:**
- Too high: Boost oscillation, overshoot
- Too low: Sluggish response, slow to reach target
- Start conservative, increase until slight overshoot, then back off

**Considerations:**
- P-term alone cannot eliminate steady-state error
- I-term required to reach and hold exact target
- Balance P and I for stability without oscillation

## Warnings

- Excessive P-gain causes boost oscillation and instability
- P-term responds instantly to noise in boost signal
- Oscillating boost stresses turbo and engine
- Test changes under controlled conditions
- Monitor boost carefully when adjusting PI parameters

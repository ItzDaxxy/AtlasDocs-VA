# Airflow - Turbo - PI Control - Integral Positive

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Positive - 2018 - LF9C102P.csv` |

## Description

Defines the positive integral gain (I-term) of the closed-loop boost control PI controller for under-boost conditions (actual boost below target). The integral term accumulates error over time to eliminate steady-state offset.

This table is used when Boost Error is positive (Target > Actual). The I-term slowly increases wastegate duty to bring actual boost up to target. Unlike the P-term which responds instantly, the I-term builds up gradually, providing the "memory" that allows the system to reach and hold exact target values.

Values are in PERCENT per sample period - larger values mean faster integral accumulation and quicker correction of sustained under-boost.

## Axes

### X-Axis

- **Parameter**: Boost Error
- **Unit**: PASCAL
- **Range**: 0.0000 to 32000.0000
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
       RPM |     0.0000 |  1000.0000 |  3000.0000 |  5000.0000 | 11000.0000 | 16000.0000 | 21000.0000 | 27000.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation and accumulation:

1. **Error Detection**: Boost Error > 0 (under-boost)
2. **Table Lookup**: Interpolate I-gain from error magnitude
3. **Accumulation**: I-term += Lookup Value (each sample)
4. **Duty Adjustment**: Accumulated I-term added to wastegate duty

**Integral Accumulation:**
```
If (Target > Actual):
    I-term = I-term + Integral_Positive_Lookup(Error)
```

**Steady-State Correction:**
- P-term alone cannot hold exact target (requires constant error)
- I-term accumulates until error reaches zero
- Provides "trim" to feedforward duty

## Related Tables

- **Airflow - Turbo - PI Control - Proportional**: Instantaneous P-term
- **Airflow - Turbo - PI Control - Integral Negative**: I-term for over-boost
- **Airflow - Turbo - PI Control - Integral Positive Limit**: Maximum I-term
- **Airflow - Turbo - PI Control - Integral Positive IAT Compensation**: IAT adjustment

## Related Datalog Parameters

- **Boost Error (Pa/kPa)**: X-axis input (positive values)
- **Wastegate Duty (%)**: Includes accumulated I-term
- **PI Integral Sum**: Accumulated integral value
- **Target Boost**: For error calculation

## Tuning Notes

**Common Modifications:**
- Increase for faster elimination of steady-state error
- Decrease to reduce overshoot and oscillation
- Tune after P-term is stable

**I-Term Tuning Guidelines:**
- Too high: Integral windup, overshoot, oscillation
- Too low: Slow to reach target, persistent offset
- Start low, increase until target is held without overshoot

**Considerations:**
- I-term has "memory" - takes time to wind up and down
- Integral windup can cause overshoot after target change
- I-term limits prevent excessive accumulation

## Warnings

- High I-gain causes integral windup and dangerous overshoot
- I-term accumulates during tip-in, can over-boost on target change
- Monitor I-term accumulation in datalogs
- I-term should be tuned after P-term is stable
- Oscillation indicates P or I too aggressive

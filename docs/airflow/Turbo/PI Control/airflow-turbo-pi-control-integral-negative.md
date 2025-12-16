# Airflow - Turbo - PI Control - Integral Negative

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x9 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Negative - 2018 - LF9C102P.csv` |

## Description

Defines the negative integral gain (I-term) of the closed-loop boost control PI controller for over-boost conditions (actual boost above target). This table is critical for safety - it determines how quickly the system responds to reduce boost when actual exceeds target.

This table is used when Boost Error is negative (Actual > Target). The I-term accumulates to reduce wastegate duty, opening the wastegate to bring boost back down. Values in this table determine how aggressively the system corrects over-boost - typically more aggressive than positive integral to prioritize safety.

Values are in PERCENT per sample period - negative values decrease wastegate duty to reduce boost.

## Axes

### X-Axis

- **Parameter**: Boost Error
- **Unit**: PASCAL
- **Range**: -32000.0000 to 0.0000
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
       RPM | -32000.0000 | -27000.0000 | -21000.0000 | -16000.0000 | -11000.0000 | -5000.0000 | -3000.0000 | -1000.0000 |
-------------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation and accumulation:

1. **Error Detection**: Boost Error < 0 (over-boost)
2. **Table Lookup**: Interpolate I-gain from error magnitude
3. **Accumulation**: I-term += Lookup Value (negative, reducing duty)
4. **Duty Adjustment**: Accumulated I-term reduces wastegate duty

**Integral Accumulation:**
```
If (Actual > Target):
    I-term = I-term + Integral_Negative_Lookup(Error)
```

**Over-Boost Protection:**
- Negative I-term reduces wastegate duty
- Lower duty = wastegate opens more = less boost
- Accumulates until boost returns to target

## Related Tables

- **Airflow - Turbo - PI Control - Proportional**: Instantaneous P-term
- **Airflow - Turbo - PI Control - Integral Positive**: I-term for under-boost
- **Airflow - Turbo - PI Control - Integral Negative Limit**: Maximum negative I-term
- **Airflow - Turbo - PI Control - Integral Negative IAT Compensation**: IAT adjustment

## Related Datalog Parameters

- **Boost Error (Pa/kPa)**: X-axis input (negative values)
- **Wastegate Duty (%)**: Reduced by accumulated I-term
- **PI Integral Sum**: Accumulated integral value
- **Actual Boost**: Over-boost monitoring

## Tuning Notes

**Common Modifications:**
- Stock values typically more aggressive than positive side
- May need adjustment for different wastegate/turbo combinations
- Ensure rapid response to over-boost for safety

**I-Term Tuning Guidelines:**
- Should respond quickly to over-boost conditions
- More aggressive than positive I-term (safety priority)
- Avoid excessive oscillation while maintaining protection

**Considerations:**
- Over-boost correction is safety-critical
- Aggressive negative I helps prevent boost spikes
- Balance with stability - don't cause oscillation

## Warnings

- Weak negative I-term can allow sustained over-boost
- Over-boost risks engine damage and blown head gaskets
- Do not reduce negative I-term aggressiveness without good reason
- Test at all RPM/load points to verify no over-boost
- Boost cut is last-resort protection - PI should prevent over-boost

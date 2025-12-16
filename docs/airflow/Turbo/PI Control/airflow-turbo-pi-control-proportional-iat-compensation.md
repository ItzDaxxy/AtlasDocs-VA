# Airflow - Turbo - PI Control - Proportional IAT Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Proportional IAT Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts the proportional gain (P-term) of the boost PI controller based on Intake Air Temperature. Hot intake air changes boost system behavior - turbo efficiency decreases and air density drops, affecting how the boost control system should respond.

Values are in PERCENT - typically applied as a multiplier to the base P-term. At hot IAT, the P-term may be reduced to prevent over-reaction to boost errors when the system is already operating in a compromised thermal state.

This compensation ensures consistent boost control behavior across varying temperature conditions.

## Axes

### X-Axis

- **Parameter**: Boost Control - Wastegate - IAT
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    35.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using IAT:

1. **IAT Reading**: ECU reads intake air temperature
2. **Table Lookup**: Interpolate P-term compensation percentage
3. **P-Term Adjustment**: Compensated P = Base P × (1 + Compensation%)

**Temperature Effects on Boost Control:**
- Cold IAT: Denser air, more predictable boost response
- Hot IAT: Less dense air, altered turbo behavior
- Compensation adapts P-gain to temperature conditions

## Related Tables

- **Airflow - Turbo - PI Control - Proportional**: Base P-term modified by this
- **Airflow - Turbo - PI Control - Integral Positive/Negative IAT Compensation**: I-term IAT adjustment
- **Airflow - Turbo - Wastegate - IAT Compensation**: Wastegate duty IAT adjustment

## Related Datalog Parameters

- **IAT (°C)**: X-axis input
- **Wastegate Duty (%)**: Final output including P-term
- **Boost Error (Pa)**: P-term input
- **Target/Actual Boost**: Error calculation

## Tuning Notes

**Common Modifications:**
- May reduce P-term at hot IAT to prevent oscillation
- Could increase at cold IAT if response is sluggish
- Coordinate with other IAT compensation tables

**Considerations:**
- Hot IAT changes boost system dynamics
- P-term may need reduction to maintain stability at high temps
- Stock values provide reasonable baseline

## Warnings

- Hot IAT dramatically affects boost control behavior
- Don't remove compensation without understanding effects
- Test at various IAT conditions
- Monitor for boost oscillation at temperature extremes

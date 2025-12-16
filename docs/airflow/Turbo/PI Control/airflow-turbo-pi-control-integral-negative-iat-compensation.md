# Airflow - Turbo - PI Control - Integral Negative IAT Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Negative IAT Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts the negative integral gain (I-term for over-boost) of the boost PI controller based on Intake Air Temperature. This table is safety-critical as it affects how quickly the system responds to over-boost conditions at different temperatures.

Values are in PERCENT - applied as a modifier to the base negative I-term. At hot IAT conditions where knock risk is elevated, the negative I-term may be made more aggressive (more negative) to ensure rapid over-boost correction.

This compensation ensures consistent over-boost protection across varying temperature conditions.

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
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using IAT:

1. **IAT Reading**: ECU reads intake air temperature
2. **Table Lookup**: Interpolate I-term compensation percentage
3. **I-Term Adjustment**: Compensated I-gain = Base I × (1 + Compensation%)

**Temperature Effects on Negative I-Term:**
- Cold IAT: Standard over-boost correction rate
- Hot IAT: May increase correction aggressiveness (more negative)
- Critical for safety at high temperatures where knock risk is elevated

## Related Tables

- **Airflow - Turbo - PI Control - Integral Negative**: Base I-term modified by this
- **Airflow - Turbo - PI Control - Proportional IAT Compensation**: P-term IAT adjustment
- **Airflow - Turbo - PI Control - Integral Negative Limit**: Maximum negative I-term
- **Airflow - Turbo - Boost - IAT Compensation**: Target boost IAT adjustment

## Related Datalog Parameters

- **IAT (°C)**: X-axis input
- **PI Integral Sum**: Accumulated I-term value
- **Wastegate Duty (%)**: Reduced by negative I-term
- **Actual Boost**: Over-boost monitoring

## Tuning Notes

**Common Modifications:**
- May make more aggressive at hot IAT for safety
- Stock values typically prioritize safety over smooth control
- Coordinate with boost target IAT compensation

**Considerations:**
- Hot IAT + over-boost = elevated knock risk
- Aggressive negative I-term helps protect engine
- Safety takes priority over smooth boost delivery

## Warnings

- Do not reduce negative I-term aggressiveness at hot IAT
- Over-boost at high IAT dramatically increases knock risk
- Hot air is less dense and more knock-prone
- Ensure rapid over-boost correction at all temperatures
- Test across full IAT range

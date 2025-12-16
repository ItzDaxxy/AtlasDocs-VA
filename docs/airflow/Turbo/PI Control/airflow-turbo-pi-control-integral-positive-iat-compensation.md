# Airflow - Turbo - PI Control - Integral Positive IAT Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Positive IAT Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts the positive integral gain (I-term for under-boost) of the boost PI controller based on Intake Air Temperature. The I-term accumulation rate may need modification at different temperatures to maintain stable boost control.

Values are in PERCENT - applied as a modifier to the base positive I-term. At hot IAT conditions, the I-term may be reduced to slow the accumulation rate, preventing integral windup when the system is thermally compromised and boost targets may be intentionally reduced.

This compensation ensures consistent I-term behavior across varying temperature conditions.

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
2. **Table Lookup**: Interpolate I-term compensation percentage
3. **I-Term Adjustment**: Compensated I-gain = Base I × (1 + Compensation%)

**Temperature Effects on I-Term:**
- Cold IAT: Normal I-term accumulation
- Hot IAT: May reduce I-term to prevent windup during thermal derating
- Coordinates with boost target IAT compensation

## Related Tables

- **Airflow - Turbo - PI Control - Integral Positive**: Base I-term modified by this
- **Airflow - Turbo - PI Control - Proportional IAT Compensation**: P-term IAT adjustment
- **Airflow - Turbo - PI Control - Integral Positive Limit**: Maximum I-term value
- **Airflow - Turbo - Boost - IAT Compensation**: Target boost IAT adjustment

## Related Datalog Parameters

- **IAT (°C)**: X-axis input
- **PI Integral Sum**: Accumulated I-term value
- **Wastegate Duty (%)**: Includes I-term contribution
- **Boost Error (Pa)**: I-term input

## Tuning Notes

**Common Modifications:**
- May reduce I-gain at hot IAT to prevent aggressive accumulation
- Coordinate with boost target IAT compensation
- If boost target is reduced at hot IAT, I-term may also need reduction

**Considerations:**
- Hot IAT conditions often have reduced boost targets
- I-term trying to chase reduced target needs less aggressive gain
- Prevents integral windup during heat-soak recovery

## Warnings

- Integral windup can cause boost overshoot when conditions change
- Coordinate with other IAT compensation tables
- Test at various temperature conditions
- Monitor I-term accumulation in datalogs

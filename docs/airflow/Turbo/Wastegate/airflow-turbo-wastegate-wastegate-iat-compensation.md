# Airflow - Turbo - Wastegate - Wastegate IAT Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate IAT Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts wastegate duty based on Intake Air Temperature (IAT). Hot intake air affects boost behavior and increases knock risk, so this table modifies wastegate control accordingly.

Values are in PERCENT - typically negative values at hot IAT reduce wastegate duty, allowing boost reduction to protect the engine during heat-soak conditions.

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
2. **Table Lookup**: Interpolates duty compensation percentage
3. **Duty Adjustment**: Applied as modifier to wastegate duty

**Temperature Compensation:**
- Cold IAT: May increase duty (more boost available)
- Normal IAT: No adjustment (0%)
- Hot IAT: Decrease duty (reduce boost for safety)

## Related Tables

- **Airflow - Turbo - Wastegate - Duty Initial**: Base duty modified by this
- **Airflow - Turbo - Wastegate - Baro Compensation**: Altitude adjustment
- **Airflow - Turbo - Boost - IAT Compensation**: Target adjustment

## Related Datalog Parameters

- **IAT (°C)**: X-axis input
- **Wastegate Duty (%)**: Final commanded duty
- **Target Boost**: Current boost target

## Tuning Notes

**Common Modifications:**
- Reduce hot IAT compensation with upgraded intercooler
- May add cold IAT duty increase for cold weather performance
- Coordinate with boost IAT compensation

**Considerations:**
- Hot IAT = denser charge heating = more knock risk
- Upgraded intercooler allows less conservative values
- Cold IAT allows safe boost increase

## Warnings

- Hot IAT significantly increases knock risk
- Don't reduce hot IAT compensation without intercooler upgrades
- Heat-soak can spike IAT quickly
- Monitor knock and boost when adjusting

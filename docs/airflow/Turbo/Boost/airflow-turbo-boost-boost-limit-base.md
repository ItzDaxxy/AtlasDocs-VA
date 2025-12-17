# Airflow - Turbo - Boost - Boost Limit Base

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x19 |
| **Data Unit** | BAR |
| **Source File** | `Airflow - Turbo - Boost - Boost Limit Base - 2018 - LF9C102P.csv` |

## Description

Defines the maximum allowable boost pressure (safety limit) based on engine RPM. This table sets an absolute ceiling for manifold pressure that the ECU will not allow the boost control system to exceed, regardless of what the Target Boost table requests.

**IMPORTANT: Values are in PSI (gauge pressure), not BAR.**

The Boost Limit acts as the final safety check in the boost control system, protecting the engine from dangerous over-boost conditions that could cause mechanical failure.

**Boost Control Hierarchy:**
1. Boost Target (what you want)
2. Boost Limit (what you're allowed) - this table
3. Actual boost is MIN(Target, Limit)

## Axes

### X-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 800.0000 to 8000.0000
- **Points**: 19

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PSI (gauge pressure)
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |  3200.0000 |  3600.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using engine RPM:

1. **RPM Reading**: ECU monitors current engine RPM
2. **Table Lookup**: Interpolates maximum allowable boost
3. **Limit Application**: Final target = MIN(Target Boost, Boost Limit)
4. **Protection Active**: If boost approaches limit, wastegate opens

**Safety Override:**
The ECU will actively reduce boost (open wastegate, reduce timing, cut fuel) if actual boost exceeds this limit.

## Related Tables

- **Airflow - Turbo - Boost - Boost Target Main**: Desired boost (limited by this table)
- **Airflow - Turbo - Wastegate - Duty Initial/Maximum**: Wastegate control
- **Airflow - Turbo - PI Control**: Closed-loop boost control

## Related Datalog Parameters

- **Boost Limit (bar/psi)**: Output from this table
- **Target Boost**: May be limited by this value
- **Actual Boost**: Measured manifold pressure
- **Engine RPM**: X-axis input

## Tuning Notes

**Common Modifications:**
- Increase limits for higher boost targets on modified engines
- Must be higher than Target Boost tables for targets to be achieved
- Should match hardware capability (turbo, head gasket, internals)

**Considerations:**
- This is a safety limit - always maintain margin above targets
- Set 10-15% above target boost for control headroom
- Consider altitude effects on achievable boost

## Warnings

- **CRITICAL SAFETY TABLE**: Setting too high removes protection
- Excessive boost causes catastrophic engine failure
- Head gasket failure common at high boost
- Rod failure and ringland failure possible
- Always verify engine internals support requested boost levels
- Never exceed turbo compressor map limits
- Monitor knock closely when raising boost limits

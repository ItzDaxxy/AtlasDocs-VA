# Throttle - Requested Torque - Limits - Requested Torque IAT Limit

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 14x12 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Requested Torque IAT Limit - 2017 - RogueWRX.csv` |

## Description

Limits maximum torque request based on Intake Air Temperature (IAT) and engine RPM. Hot intake air is less dense and more prone to knock, so this table reduces allowable torque when IAT rises to protect the engine.

The table shows torque limits increasing with temperature up to a point (warmer air requires more throttle for same torque), then potentially decreasing at very high IAT as a protection measure. Cold air (-40 to 0°C) shows lower limits likely to prevent issues during cold start/warm-up, while normal operating temperatures (20-40°C) allow full torque.

This table provides automatic derating during heat-soak conditions common in turbocharged vehicles, where intercooler efficiency drops and IAT rises significantly.

## Axes

### X-Axis

- **Parameter**: IAT
- **Unit**: CELSIUS
- **Range**: -40.0000 to 70.0000
- **Points**: 12

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7600.0000
- **Points**: 14

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |   120.0000 |   120.0000 |   120.0000 |   120.0000 |   160.0000 |   160.0000 |   160.0000 |   160.0000 |
  800.0000 |   120.0000 |   120.0000 |   120.0000 |   125.0000 |   160.0000 |   160.0000 |   160.0000 |   160.0000 |
 1200.0000 |   130.0000 |   130.0000 |   145.0000 |   145.0000 |   185.0000 |   200.0000 |   215.0000 |   215.0000 |
 1600.0000 |   140.0000 |   140.0000 |   150.0000 |   150.0000 |   230.0000 |   240.0000 |   250.0000 |   250.0000 |
 1800.0000 |   150.0000 |   175.0000 |   195.0000 |   210.0000 |   275.0000 |   288.0000 |   300.0000 |   300.0000 |
 2000.0000 |   160.0000 |   210.0000 |   240.0000 |   270.0000 |   300.0000 |   325.0000 |   350.0000 |   350.0000 |
 2300.0000 |   205.0000 |   240.0000 |   240.0000 |   281.2500 |   300.0000 |   339.5000 |   350.0000 |   350.0000 |
 2400.0000 |   220.0000 |   240.0000 |   250.0000 |   285.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using IAT and RPM:

1. **IAT Monitoring**: ECU reads intake air temperature sensor
2. **RPM Reading**: ECU monitors engine RPM
3. **Table Lookup**: 2D interpolation determines maximum torque
4. **Torque Limiting**: Requested torque capped at this value

**Temperature Protection:**
- Cold IAT: Limited torque during warm-up
- Normal IAT (20-40°C): Full torque available
- Hot IAT (50°C+): Torque progressively reduced
- Extreme IAT (70°C+): Maximum derating applied

## Related Tables

- **Airflow - Turbo - Boost - IAT Compensation**: Boost target adjustment
- **Airflow - Turbo - Wastegate - IAT Compensation**: Wastegate duty adjustment
- **Ignition - IAT Compensation**: Timing adjustment for IAT
- **Throttle - Requested Torque - Limits - Maximum A/B/C**: Other torque limits

## Related Datalog Parameters

- **IAT (°C)**: Intake air temperature reading
- **Requested Torque (Nm)**: Before IAT limiting
- **Limited Torque (Nm)**: After all limits applied
- **Engine RPM**: Y-axis input

## Tuning Notes

**Understanding the Table:**
- Cold columns show warm-up protection
- Hot columns (50-70°C) show heat-soak protection
- Values increase with RPM for higher RPM torque capability

**Common Modifications:**
- Increase hot IAT limits with upgraded intercooler
- Adjust cold limits if experiencing cold weather drivability issues
- May need reduction for aggressive turbo setups that heat-soak quickly

**Considerations:**
- This is primarily an engine protection table
- Hot intake air increases knock tendency
- Upgraded intercooler allows less conservative limits

## Warnings

- Hot IAT dramatically increases knock risk
- Raising hot IAT limits without intercooler upgrades is dangerous
- Heat-soak during traffic or hard driving can spike IAT rapidly
- Always datalog IAT and knock during testing
- Consider water-methanol injection for consistent IAT control

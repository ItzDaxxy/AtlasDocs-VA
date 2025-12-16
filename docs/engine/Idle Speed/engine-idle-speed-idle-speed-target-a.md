# Engine - Idle Speed - Idle Speed Target A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | RPM |
| **Source File** | `Engine - Idle Speed - Idle Speed Target A - 2018 - LF9C102P.csv` |

## Description

Defines the target idle RPM based on coolant temperature. This is one of multiple idle speed target tables (A through J) that the ECU uses to determine desired idle speed under various conditions. The ECU selects between these tables based on operating state (A/C on/off, electrical load, transmission state, etc.).

Table A is typically the base idle target for normal operating conditions without additional loads. Higher RPM targets at cold temperatures help the engine warm up faster, overcome increased friction, and maintain stable combustion. As coolant temperature increases, the target RPM decreases to improve fuel economy and reduce emissions.

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: RPM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using coolant temperature to determine the target idle RPM:

1. **Temperature Reading**: ECU reads current coolant temperature from ECT sensor
2. **Table Lookup**: Interpolates between temperature breakpoints to find target RPM
3. **Idle Control**: Adjusts electronic throttle body and/or idle air control to achieve target
4. **Closed-Loop Control**: Uses PID control to maintain actual RPM near target

Typical values range from:
- ~1200-1500 RPM at cold temperatures (-40°C to 0°C)
- ~900-1000 RPM during warm-up (10°C to 60°C)
- ~700-800 RPM at normal operating temperature (80°C+)

## Related Tables

- **Engine - Idle Speed - Target B through J**: Alternate idle targets for different conditions
- **Engine - Idle Speed - Coolant/Baro Compensation A/B**: Additional compensation tables
- **Throttle - Idle Air Control**: Works with target to achieve desired RPM
- **Fuel - Idle AFR Target**: Fuel delivery targets at idle

## Related Datalog Parameters

- **Target Idle RPM**: The commanded idle speed from this table
- **Actual Idle RPM**: Measured engine speed at idle
- **Coolant Temperature (°C)**: X-axis input for table lookup
- **Idle Control Duty (%)**: Throttle position to achieve target
- **A/C Clutch Status**: May select alternate idle table

## Tuning Notes

**Common Modifications:**
- Increase idle RPM by 50-100 RPM if experiencing rough idle with cams or intake modifications
- Lower warm idle RPM for quieter operation (risk: stalling with A/C or electrical loads)
- Adjust cold idle RPM to improve cold-start stability

**Considerations:**
- Higher idle = more fuel consumption, more heat, faster warm-up
- Lower idle = better fuel economy but may cause stalling under load
- Modified camshafts often require higher idle to overcome increased overlap
- Aftermarket intakes may affect idle airflow characteristics

## Warnings

- Setting idle too low can cause stalling, especially with A/C, power steering load, or electrical accessories
- Setting idle too high wastes fuel and increases wear
- Changes affect emissions - catalyst light-off timing depends on proper warm-up
- Monitor for hunting or surging after modifications
- Ensure other idle tables (B-J) are modified consistently to prevent inconsistent behavior

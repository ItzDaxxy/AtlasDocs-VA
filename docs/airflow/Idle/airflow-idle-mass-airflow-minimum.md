# Airflow - Idle - Mass Airflow Minimum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | G_PER_SEC |
| **Source File** | `Airflow - Idle - Mass Airflow Minimum - 2018 - LF9C102P.csv` |

## Description

Defines the minimum mass airflow (g/s) allowed by the ECU at various RPM and coolant temperature conditions. This table sets a floor on calculated airflow, preventing the ECU from computing unrealistically low airflow values that could cause fueling or control issues.

This minimum ensures stable idle and deceleration behavior. Even if the MAF sensor reads very low, the ECU will not use an airflow value below this minimum for its calculations. This prevents issues like tip-in hesitation from overly lean transient fueling.

Values are in G_PER_SEC (grams per second). The table shows relatively consistent minimums across temperature, varying primarily with RPM.

## Axes

### X-Axis

- **Parameter**: Idle Control - Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Idle Control - RPM
- **Unit**: NONE
- **Range**: 0.0000 to 7800.0000
- **Points**: 21

## Cell Values

- **Unit**: G_PER_SEC
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |     3.7500 |
  400.0000 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |
  800.0000 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |     2.7500 |
 1200.0000 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |     3.2500 |
 1600.0000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |     4.5000 |
 2000.0000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |     5.5000 |
 2400.0000 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |     7.6250 |
 2800.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |     8.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation and applies as a minimum:

1. **Inputs**: Coolant Temperature, Engine RPM
2. **Table Lookup**: 2D interpolation for minimum airflow
3. **Minimum Enforcement**: Used Airflow = MAX(Calculated, Minimum)

**Application Logic:**
```
If (Calculated_Airflow < Minimum_Airflow):
    Use Minimum_Airflow
Else:
    Use Calculated_Airflow
```

**Purpose:**
- Prevents unrealistically low airflow calculations
- Ensures minimum fueling for engine stability
- Improves deceleration fuel cut recovery

## Related Tables

- **Sensors - Mass Airflow**: MAF sensor calibration
- **Engine - Idle Speed Target**: Commanded idle RPM
- **Fuel - Injector Scaling**: Fueling from airflow
- **Airflow - MAF - VE Correction**: Airflow calculation

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **Engine RPM**: Y-axis input (during idle/low-load)
- **MAF (g/s)**: Compared against minimum
- **Calculated Load**: Uses enforced minimum

## Tuning Notes

**Common Modifications:**
- May need adjustment with cam changes affecting idle airflow
- Larger injectors may need higher minimums
- Affects tip-in response from closed throttle

**Considerations:**
- Too high: Over-rich at idle/decel
- Too low: May not prevent calculation errors
- Stock values appropriate for most applications

**Interaction with Fuel Cut:**
- During decel fuel cut, airflow can be very low
- Minimum helps smooth fuel cut recovery
- Prevents lean hesitation on tip-in

## Warnings

- Excessive minimum causes rich idle conditions
- Too low minimum may cause tip-in hesitation
- Monitor AFR at idle after modifications
- Verify smooth decel fuel cut recovery

# Throttle - Target Throttle - Main - A (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Main - A (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This table defines the target throttle plate opening angle based on the requested torque ratio and engine RPM when the Tumble Generator Valves (TGV) are in the CLOSED position. The TGV Closed state is used during low to moderate airflow conditions, typically at lower engine loads and RPM ranges where enhanced air tumble is desired for improved combustion efficiency and emissions. The closed TGVs create a swirling motion in the intake charge, improving low-end torque and throttle response. The ECU uses this table to translate the driver's torque demand into a specific throttle plate position optimized for the tumble flow condition.

## Axes

### X-Axis

- **Parameter**: Throttle - Requested Torque Ratio
- **Unit**: PERCENT
- **Range**: 0.0000 to 1.0000
- **Points**: 24

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 7800.0000
- **Points**: 22

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.0431 |     0.0863 |     0.1294 |     0.1725 |     0.2157 |     0.2627 |     0.3059 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     0.4608 |     0.9216 |     1.3825 |     1.8433 |     2.3041 |     2.7634 |     3.4668 |
 1200.0000 |     0.0000 |     1.0773 |     2.1546 |     3.2319 |     4.3091 |     5.1118 |     5.9159 |     6.7323 |
 1600.0000 |     0.0000 |     0.4761 |     2.1592 |     4.1672 |     5.6031 |     7.0359 |     8.4535 |     9.8711 |
 2000.0000 |     0.0000 |     0.2853 |     5.0919 |     7.0176 |     7.7867 |     9.4469 |    11.1086 |    12.7184 |
 2400.0000 |     0.0000 |     0.9079 |     3.1281 |     5.6886 |     8.2551 |    10.2190 |    11.7693 |    13.3196 |
 2800.0000 |     0.0000 |     1.4893 |     4.3961 |     7.5044 |     9.4865 |    11.3481 |    12.9381 |    14.4183 |
 3200.0000 |     0.0000 |     2.8550 |     5.5573 |     8.2216 |    10.1015 |    11.8578 |    13.3455 |    14.7921 |
 3600.0000 |     0.0000 |     2.4369 |     5.5848 |     8.7068 |    10.5898 |    12.3354 |    13.7713 |    15.1385 |
```

## Functional Behavior

The ECU performs 2D interpolation using the current engine RPM (Y-axis) and the requested torque ratio (X-axis) to determine the target throttle plate angle when TGVs are closed. The ECU automatically switches between this table and the TGV Open variant based on operating conditions. Because the TGVs restrict airflow when closed, the throttle typically needs to open more to achieve the same torque output compared to the TGV Open condition. This compensates for the reduced effective intake area and maintains consistent engine response across TGV position changes.

## Related Tables

- Throttle - Target Throttle - Main - A (TGV Open)
- Throttle - Target Throttle - Main - B (TGV Open)
- Throttle - Target Throttle - Main - B (TGV Closed)
- Throttle - Requested Torque - In-Gear tables
- Throttle - Requested Torque - Out-of-Gear tables

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position

## Tuning Notes

When tuning this table, consider the airflow restriction caused by closed TGVs. Common modifications include:
- Increasing throttle opening values slightly more than the TGV Open table to compensate for restricted flow
- Smoothing transitions to reduce perceptible changes when TGVs switch position during driving
- Adjusting the crossover points between TGV states for better drivability
- For vehicles with TGV deletes, this table becomes unused and only the TGV Open tables are active
When increasing boost or making power modifications, ensure the increased throttle opening doesn't cause the engine to request more airflow than the closed TGVs can supply, which can cause hunting or instability.

## Warnings

Improper modifications to this table can result in dangerous driving conditions:
- Excessive throttle opening with closed TGVs can cause airflow restriction and engine instability
- Mismatched values between TGV Open/Closed tables will cause jerking or surging during TGV transitions
- Over-aggressive throttle response can cause traction loss, especially in lower gears
- Inconsistent calibration with Requested Torque tables may trigger limp mode or error codes
- TGV position conflicts can confuse the ECU and cause drivability issues
Always test TGV transition points thoroughly and validate that throttle response remains predictable across the full operating range. Monitor for any TGV-related error codes after modifications.

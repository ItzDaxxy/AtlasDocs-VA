# Throttle - Target Throttle - Main - A (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Main - A (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This table defines the target throttle plate opening angle based on the requested torque ratio and engine RPM when the Tumble Generator Valves (TGV) are in the OPEN position. The TGV Open state is used during high airflow conditions, typically at higher engine loads and RPM ranges where maximum airflow is desired. The ECU uses this table to translate the driver's torque demand (derived from accelerator pedal position) into a specific throttle plate position to achieve the requested engine output.

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
  800.0000 |     0.0000 |     0.5005 |     1.0025 |     1.5030 |     2.0050 |     2.5055 |     3.1159 |     3.8880 |
 1200.0000 |     0.0000 |     1.1444 |     2.2873 |     3.4318 |     4.5747 |     5.7145 |     6.6743 |     7.6661 |
 1600.0000 |     0.0000 |     1.5625 |     3.1861 |     4.8905 |     6.0365 |     7.2023 |     8.5954 |     9.9870 |
 2000.0000 |     0.0000 |     2.1744 |     4.2542 |     6.0960 |     7.9026 |     9.6223 |    11.2230 |    12.5673 |
 2400.0000 |     0.0000 |     1.6175 |     4.2939 |     6.4271 |     8.4184 |    10.0603 |    11.5145 |    13.0236 |
 2800.0000 |     0.0000 |     2.4811 |     4.9622 |     7.1595 |     9.2515 |    10.9667 |    12.5994 |    14.1573 |
 3200.0000 |     0.0000 |     2.5025 |     5.5390 |     8.2002 |    10.0679 |    11.8563 |    13.2113 |    14.8638 |
 3600.0000 |     0.0000 |     1.3962 |     4.9332 |     8.4535 |    10.1823 |    11.9112 |    13.3242 |    14.6715 |
```

## Functional Behavior

The ECU performs 2D interpolation using the current engine RPM (Y-axis) and the requested torque ratio (X-axis) to determine the target throttle plate angle. The requested torque ratio is calculated from the driver's accelerator pedal position and various torque request tables. The ECU then commands the electronic throttle body to move to the calculated position. This table works in conjunction with the TGV position - when TGVs are open, this table is active and provides the throttle mapping optimized for maximum airflow scenarios. The values are unitless and represent the throttle opening angle in a normalized format.

## Related Tables

- Throttle - Target Throttle - Main - A (TGV Closed)
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

Modifications to this table are typically made to adjust throttle response characteristics. Increasing values will result in a more aggressive throttle response (throttle opens more for a given pedal input), while decreasing values creates a more conservative, smoother response. Common modifications include:
- Smoothing the transition between low and mid torque request ranges to reduce abrupt throttle response
- Adjusting low RPM/low load areas to improve drivability and reduce tip-in harshness
- Matching values to the TGV Closed variant for consistency across TGV transitions
- Scaling values proportionally when increasing boost or modifying the engine's torque output capability
Always ensure changes are synchronized with corresponding Requested Torque tables to maintain proper drive-by-wire calibration.

## Warnings

Improper modifications to this table can result in dangerous driving conditions. Excessive throttle opening values can cause:
- Uncontrolled acceleration and loss of vehicle control
- Over-boost conditions that may damage the engine
- Inconsistent throttle response that makes the vehicle unpredictable
- Throttle tip-in surge or bucking that can affect traction and stability
- Potential conflicts with traction control and stability systems
Never increase throttle opening values beyond what the engine can safely handle based on your turbo, fuel, and engine modifications. Always validate changes with careful datalogging and testing in controlled conditions. Ensure the Requested Torque tables are properly calibrated to match any throttle changes.

# Throttle - Target Throttle - Alternate - A (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Alternate - A (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This is an alternate target throttle table used when TGVs are CLOSED. As part of the Alternate table set, this provides backup calibration for failsafe modes, error conditions, or alternative operating modes. When TGVs are closed and the ECU is operating in alternate mode, this table determines throttle plate angles optimized for tumble flow conditions while maintaining safe, predictable behavior in potentially degraded operating states.

## Axes

### X-Axis

- **Parameter**: Throttle - Requested Torque Ratio
- **Unit**: PERCENT
- **Range**: 0.0000 to 1.0000
- **Points**: 24

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 8000.0000
- **Points**: 22

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.0431 |     0.0863 |     0.1294 |     0.1725 |     0.2157 |     0.2627 |     0.3059 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0443 |     0.7156 |     1.3855 |     2.0554 |     2.7268 |
 1000.0000 |     0.0000 |     0.4898 |     0.9796 |     1.4908 |     2.2644 |     3.0182 |     3.7720 |     4.4984 |
 1200.0000 |     0.0000 |     0.9796 |     1.9577 |     2.9374 |     3.8132 |     4.6509 |     5.4887 |     6.2715 |
 1400.0000 |     0.0000 |     1.3596 |     2.7207 |     3.9307 |     4.8295 |     6.1097 |     7.1794 |     8.0995 |
 1600.0000 |     0.0000 |     1.7395 |     3.4806 |     4.9195 |     6.1006 |     7.2007 |     8.4001 |    10.1900 |
 1800.0000 |     0.0000 |     2.0401 |     4.0406 |     5.8000 |     7.1000 |     9.1997 |    11.0002 |    11.9997 |
 2000.0000 |     0.0000 |     2.3407 |     5.2995 |     6.9001 |     8.7999 |    11.0002 |    12.6009 |    14.0002 |
 2400.0000 |     0.0000 |     3.5294 |     6.2501 |     8.5206 |    10.4204 |    12.0806 |    13.8003 |    15.5001 |
```

## Functional Behavior

The ECU interpolates this table using RPM and requested torque ratio when operating in alternate mode with TGVs closed. Like all TGV Closed tables, values are typically higher than TGV Open equivalents to compensate for restricted airflow. The table provides failsafe throttle control that maintains drivability even when primary systems are compromised, while respecting the airflow limitations of closed TGVs.

## Related Tables

- Throttle - Target Throttle - Alternate - A (TGV Open)
- Throttle - Target Throttle - Alternate - B tables
- Throttle - Target Throttle - Main - A (TGV Closed)
- Throttle - Requested Torque tables

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Throttle Table Selector/Mode
- Error Codes/Fault Status

## Tuning Notes

This table must balance failsafe conservatism with TGV airflow restrictions:
- Values must compensate for closed TGV airflow restriction while remaining safe
- Coordinate with Alternate A TGV Open to ensure smooth TGV transitions in alternate mode
- Often calibrated conservatively for safe operation in degraded modes
- May be copied from Main A TGV Closed if failsafe distinction is not needed
- For TGV delete applications, this table is not used
Test that transitions between alternate and main tables, as well as TGV position changes, remain smooth and predictable.

## Warnings

Critical failsafe table - improper calibration can compromise vehicle safety:
- Must account for airflow restriction without causing engine instability
- Excessive throttle opening with closed TGVs can cause severe drivability issues
- Too conservative values may make vehicle undriveable if alternate mode activates
- Mismatched TGV Open/Closed alternate tables cause harsh transitions in failsafe mode
- Empty or corrupted table can trigger limp mode
Maintain functional calibration even in alternate mode. Validate behavior across all TGV positions and table switching scenarios.

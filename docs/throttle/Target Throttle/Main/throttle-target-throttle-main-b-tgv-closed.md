# Throttle - Target Throttle - Main - B (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Main - B (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This is a secondary target throttle table used when the Tumble Generator Valves (TGV) are in the CLOSED position. The "Main B" designation indicates this table is used under specific operating conditions that differ from "Main A", such as different driving modes or transmission states. When active, this table defines throttle plate opening angles optimized for tumble flow conditions with closed TGVs. The ECU switches between this and the Main A TGV Closed table based on vehicle operating mode.

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
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0839 |     0.7492 |     1.4145 |     2.0798 |     2.7451 |
 1000.0000 |     0.0000 |     0.4883 |     0.9766 |     1.5076 |     2.2492 |     2.9847 |     3.7186 |     4.4694 |
 1200.0000 |     0.0000 |     0.9766 |     1.9547 |     2.9313 |     3.7476 |     4.5533 |     5.3590 |     6.1936 |
 1400.0000 |     0.0000 |     1.3306 |     2.6596 |     3.8697 |     4.9699 |     6.0807 |     7.0603 |     8.2002 |
 1600.0000 |     0.0000 |     1.6800 |     3.3600 |     4.8203 |     6.1997 |     7.2999 |     8.9998 |    10.7103 |
 1800.0000 |     0.0000 |     1.9898 |     3.9002 |     5.4597 |     7.2007 |     9.3996 |    11.0002 |    12.8008 |
 2000.0000 |     0.0000 |     2.2904 |     5.2003 |     6.7994 |     8.9998 |    11.7998 |    13.6004 |    16.2005 |
 2400.0000 |     0.0000 |     3.6500 |     6.2196 |     8.5801 |    10.8598 |    13.0800 |    15.1705 |    17.7996 |
```

## Functional Behavior

The ECU interpolates this table using RPM and requested torque ratio when operating in the mode that selects Main B tables with TGVs closed. Like all TGV Closed tables, the throttle opening values typically need to be higher than TGV Open equivalents to compensate for restricted airflow. The ECU manages smooth transitions between Main A and Main B, as well as between TGV Open and Closed states.

## Related Tables

- Throttle - Target Throttle - Main - A (TGV Closed)
- Throttle - Target Throttle - Main - B (TGV Open)
- Throttle - Target Throttle - Alternate tables
- Throttle - Requested Torque tables

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Active Throttle Table Selector

## Tuning Notes

This table should be tuned in coordination with Main B TGV Open to ensure smooth TGV transitions:
- Values typically need to be higher than TGV Open to compensate for airflow restriction
- Maintain proportional relationships with Main A TGV Closed table
- Test transitions between Main A/B and TGV Open/Closed states
- For TGV delete applications, this table is typically not used
Consider making Main A and Main B identical if the switching logic behavior is not well understood or not needed for your application.

## Warnings

Improper calibration can cause:
- Harsh transitions when switching between table sets or TGV positions
- Airflow restriction issues with closed TGVs if throttle opens too much
- Inconsistent throttle response across operating modes
- Engine instability or hunting during mode transitions
- Potential conflicts with traction control systems
Validate all four combinations (Main A/B and TGV Open/Closed) work harmoniously. Monitor for TGV error codes and mode switching behavior during testing.

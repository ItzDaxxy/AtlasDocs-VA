# Throttle - Target Throttle - Main - B (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Main - B (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This is a secondary or alternate target throttle table used when the Tumble Generator Valves (TGV) are in the OPEN position. The "Main B" designation indicates this is likely used under specific operating conditions or modes that differ from the "Main A" table, such as different driving modes, transmission states, or environmental conditions. The ECU selects between Main A and Main B tables based on additional switching logic. Like the A variant, this table defines throttle plate opening angles for high airflow conditions when TGVs are open.

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
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.5997 |     1.3001 |     2.0005 |     2.6993 |
 1200.0000 |     0.0000 |     1.0605 |     2.1302 |     3.1907 |     4.0101 |     4.8295 |     5.6504 |     6.4500 |
 1600.0000 |     0.0000 |     1.7105 |     3.4195 |     4.7395 |     5.8198 |     6.9001 |     7.9698 |     9.0394 |
 2000.0000 |     0.0000 |     2.9603 |     5.3605 |     7.1595 |     9.5003 |    10.8995 |    12.3003 |    13.8003 |
 2400.0000 |     0.0000 |     3.0503 |     5.9907 |     8.9998 |    10.4997 |    12.3003 |    13.8994 |    14.9996 |
 2800.0000 |     0.0000 |     3.7003 |     6.8605 |    10.6004 |    11.7998 |    13.8003 |    15.8007 |    17.0001 |
 3200.0000 |     0.0000 |     4.4602 |     7.7897 |    10.2098 |    11.7708 |    13.2204 |    14.8699 |    16.4706 |
 3600.0000 |     0.0000 |     6.6896 |     9.1005 |    11.3497 |    12.9809 |    14.5098 |    15.8495 |    17.1405 |
```

## Functional Behavior

The ECU uses 2D interpolation to determine the target throttle angle based on RPM and requested torque ratio. The switching logic between Main A and Main B tables may be based on factors such as transmission mode selection, cruise control state, or other vehicle operating conditions. Both tables serve the same fundamental purpose but may have different calibration characteristics to optimize for specific driving scenarios. When this table is active, it overrides the Main A table.

## Related Tables

- Throttle - Target Throttle - Main - A (TGV Open)
- Throttle - Target Throttle - Main - B (TGV Closed)
- Throttle - Target Throttle - Alternate tables
- Throttle - Requested Torque - In-Gear tables
- Throttle - Requested Torque - Out-of-Gear tables

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Active Throttle Table Selector (if available)

## Tuning Notes

When tuning the Main B table, it's important to understand when the ECU switches to this table versus Main A:
- Compare values to Main A to identify the intended behavior differences
- Maintain consistency with the switching logic to avoid abrupt transitions
- If the distinction between A and B tables is unclear, they can often be calibrated identically
- Some tuners choose to make both A and B tables identical to simplify calibration
- Observe datalogs during different driving conditions to determine when each table is active
Modifications should maintain proportionality with the Requested Torque tables and be validated across all operating conditions where this table is active.

## Warnings

Incorrect calibration of this table can cause:
- Sudden changes in throttle response when switching between Main A and Main B tables
- Confusion during troubleshooting if the table selection logic is not understood
- Over-boost or lean conditions if throttle opening exceeds safe limits
- Drivability issues if Main A and Main B have drastically different characteristics
- Potential for unintended throttle behavior in specific driving modes
Always identify the switching conditions before making modifications. Test thoroughly in all operating modes to ensure consistent and safe throttle behavior. Document which conditions activate this table for future reference.

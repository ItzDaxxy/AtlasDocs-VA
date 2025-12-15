# Throttle - Target Throttle - Alternate - A (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Alternate - A (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This is an alternate target throttle table set used when TGVs are OPEN. "Alternate" tables typically serve as backup or secondary calibration sets that the ECU switches to under specific conditions such as failsafe modes, specific error conditions, reduced power modes, or alternative drive modes. This provides redundancy and allows the ECU to maintain drivability even when certain sensors or systems are compromised. When active, this table determines throttle plate angles for high airflow conditions with open TGVs.

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
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.5982 |     1.3001 |     2.0005 |     2.7008 |
 1000.0000 |     0.0000 |     0.5310 |     1.0636 |     1.5946 |     2.3056 |     3.0655 |     3.8254 |     4.5777 |
 1200.0000 |     0.0000 |     1.0636 |     2.1256 |     3.1891 |     4.0116 |     4.8310 |     5.6504 |     6.4546 |
 1400.0000 |     0.0000 |     1.3901 |     2.7695 |     3.9597 |     4.8295 |     5.8701 |     6.8101 |     7.7501 |
 1600.0000 |     0.0000 |     1.7105 |     3.4195 |     4.7395 |     5.8198 |     6.9001 |     8.0003 |     9.1997 |
 1800.0000 |     0.0000 |     2.3301 |     4.3900 |     5.9495 |     7.3106 |     8.9006 |    10.2007 |    11.5999 |
 2000.0000 |     0.0000 |     2.9603 |     5.3605 |     7.1595 |     9.1997 |    10.4997 |    11.9997 |    13.4997 |
 2400.0000 |     0.0000 |     3.0503 |     5.9907 |     8.6000 |    10.6004 |    11.7998 |    13.2006 |    15.1995 |
```

## Functional Behavior

The ECU interpolates this table using RPM and requested torque ratio when the alternate table set is active. Switching to alternate tables may occur during sensor failures, reduced performance modes, or specific operating conditions. The interpolation method is identical to the Main tables, but the values may be more conservative to ensure safe operation in compromised conditions. The table remains inactive unless specific conditions trigger the alternate table selection.

## Related Tables

- Throttle - Target Throttle - Alternate - A (TGV Closed)
- Throttle - Target Throttle - Alternate - B (TGV Open)
- Throttle - Target Throttle - Alternate - B (TGV Closed)
- Throttle - Target Throttle - Main tables

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Throttle Table Selector/Mode
- Error Codes/Fault Status

## Tuning Notes

Alternate tables are often left conservative to ensure safe operation in degraded modes:
- Values are typically lower than Main tables to provide reduced but predictable throttle response
- Can be calibrated identically to Main tables if failsafe behavior is not desired
- Some tuners copy Main table values to Alternate tables for consistency
- Useful for testing - switching to Alternate can help diagnose table-related issues
- Monitor when this table becomes active to understand ECU switching logic
If you modify these tables, ensure they provide safe, predictable behavior even in error conditions.

## Warnings

These tables are safety-critical for failsafe operation:
- Too aggressive values can compromise safety in degraded operating modes
- Too conservative values can make the vehicle undriveable if alternate tables activate unexpectedly
- Misunderstanding when these activate can lead to confusion during troubleshooting
- Some error conditions may force the ECU to use alternate tables permanently until cleared
- Deleting or zeroing these tables can cause limp mode if the ECU tries to use them
Always maintain functional alternate tables even if they're identical to Main tables. Test behavior when the ECU switches to alternate mode to ensure vehicle remains controllable.

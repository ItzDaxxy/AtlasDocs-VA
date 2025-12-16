# Throttle - Target Throttle - Alternate - B (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x24 |
| **Data Unit** | NONE |
| **Source File** | `Throttle - Target Throttle - Alternate - B (TGV Open) - 2017 - RogueWRX.csv` |

## Description

This is a secondary alternate target throttle table used when TGVs are OPEN. The "Alternate B" designation indicates a backup to the Alternate A table, providing additional redundancy or supporting specific sub-modes within the alternate operating state. This multi-layered approach ensures the ECU has multiple fallback options for throttle control. When active, it defines throttle angles for high airflow conditions with open TGVs in alternate operating mode.

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
 1000.0000 |     0.0000 |     0.5463 |     1.0910 |     1.5854 |     2.3133 |     3.0930 |     3.8712 |     4.6357 |
 1200.0000 |     0.0000 |     1.0910 |     2.1836 |     3.1693 |     4.0284 |     4.8859 |     5.7435 |     6.5705 |
 1400.0000 |     0.0000 |     1.4008 |     2.8107 |     3.9200 |     4.9104 |     5.9098 |     6.8696 |     7.8004 |
 1600.0000 |     0.0000 |     1.7197 |     3.4302 |     4.6708 |     5.8000 |     6.9306 |     8.0003 |     9.1997 |
 1800.0000 |     0.0000 |     2.3102 |     4.3793 |     5.9800 |     7.4098 |     8.9494 |    10.2007 |    11.4000 |
 2000.0000 |     0.0000 |     2.9007 |     5.6001 |     7.2908 |     9.0105 |    10.6004 |    12.1996 |    13.6004 |
 2400.0000 |     0.0000 |     4.1001 |     6.6606 |     8.9708 |    10.5501 |    12.0607 |    13.9010 |    15.4009 |
```

## Functional Behavior

The ECU interpolates this table when operating in the specific mode that selects Alternate B tables with TGVs open. This provides an additional layer of table selection beyond Main/Alternate and TGV Open/Closed, though the exact switching logic varies by ECU calibration. The interpolation method is standard 2D lookup based on RPM and torque ratio.

## Related Tables

- Throttle - Target Throttle - Alternate - A (TGV Open)
- Throttle - Target Throttle - Alternate - B (TGV Closed)
- Throttle - Target Throttle - Main - B (TGV Open)
- All other Target Throttle table variants

## Related Datalog Parameters

- Throttle Opening Angle
- Requested Torque Ratio
- Engine RPM
- TGV Position/Status
- Accelerator Pedal Position
- Throttle Table Selector/Mode
- Error Codes/Fault Status

## Tuning Notes

Alternate B tables are rarely used in most driving conditions:
- Often calibrated identically to Alternate A or Main B tables
- Exact activation conditions may be difficult to determine without detailed ECU documentation
- Can be used for specialized modes or extreme failsafe conditions
- Some tuners copy values from other table sets to maintain consistency
- Monitor datalogs to determine if this table ever becomes active in your application
Unless you have specific knowledge of when this table activates, conservative calibration matching other alternate tables is recommended.

## Warnings

As a deep failsafe table, proper calibration is essential:
- Vehicle may only use this table under rare or severe fault conditions
- Incorrect values could leave vehicle inoperable when this table is needed
- May be combined with multiple simultaneous fault conditions
- Testing when this table is active may be difficult or impossible under normal conditions
- Corrupted or missing calibration can cause unpredictable behavior
Maintain conservative, functional values. If uncertain about usage, copy from Alternate A TGV Open or Main B TGV Open tables.

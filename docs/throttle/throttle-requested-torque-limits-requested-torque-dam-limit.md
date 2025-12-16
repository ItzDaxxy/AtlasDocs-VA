# Throttle - Requested Torque - Limits - Requested Torque DAM Limit

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 6x14 |
| **Data Unit** | NM |
| **Source File** | `Throttle - Requested Torque - Limits - Requested Torque DAM Limit - 2017 - RogueWRX.csv` |

## Description

Limits maximum torque request based on Dynamic Advance Multiplier (DAM) value and engine RPM. DAM is a knock feedback parameter that ranges from 0.0 (maximum knock retard applied) to 1.0 (no knock-based timing reduction). This table reduces allowable torque when DAM drops, providing engine protection during knock events.

When the engine experiences knock, DAM decreases, and this table progressively limits torque request to reduce cylinder pressure and protect the engine. At DAM 1.0, full torque is available (350 Nm across most RPM range). At lower DAM values, torque limits decrease, especially at higher RPM where knock is most dangerous.

This is a critical safety table that prevents the engine from requesting excessive torque when knock adaptation indicates combustion issues.

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 2400.0000 to 7200.0000
- **Points**: 14

### Y-Axis

- **Parameter**: Ignition - Dynamic Advance - DAM
- **Unit**: NONE
- **Range**: 0.0000 to 1.0000
- **Points**: 6

## Cell Values

- **Unit**: NM
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |  2400.0000 |  2800.0000 |  3200.0000 |  3600.0000 |  4000.0000 |  4400.0000 |  4800.0000 |  5200.0000 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   322.0000 |   335.0000 |   305.0000 |
    0.3125 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   334.5000 |   341.7000 |   324.9625 |
    0.5000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   342.0000 |   345.7125 |   336.9375 |
    0.6250 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   347.0000 |   348.3875 |   344.9250 |
    0.6875 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   349.7250 |
    1.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   350.0000 |   349.7250 |
```

## Functional Behavior

The ECU performs 2D interpolation using DAM and RPM:

1. **DAM Monitoring**: ECU tracks current DAM value (knock feedback)
2. **RPM Reading**: ECU monitors engine RPM
3. **Table Lookup**: 2D interpolation determines maximum torque
4. **Torque Limiting**: Requested torque capped at this value when DAM is low

**Protection Logic:**
- DAM = 1.0: Full torque allowed (no knock detected)
- DAM < 1.0: Torque progressively limited
- DAM = 0.0: Maximum torque reduction applied

## Related Tables

- **Ignition - Dynamic Advance Multiplier**: Source of DAM value
- **Ignition - Feedback Knock Correction**: Individual cylinder knock response
- **Throttle - Requested Torque - Limits - Maximum A/B/C**: Base maximum tables
- **Airflow - Turbo - Boost - Target**: Affected by torque limits

## Related Datalog Parameters

- **DAM**: Dynamic Advance Multiplier (0.0-1.0)
- **Feedback Knock Correction**: Per-cylinder knock retard
- **Fine Knock Learn**: Long-term knock adaptation
- **Requested Torque (Nm)**: Before DAM limiting
- **Limited Torque (Nm)**: After all limits applied

## Tuning Notes

**Understanding the Table:**
- Low DAM rows show reduced torque limits (engine protecting itself)
- High RPM columns may show more aggressive limiting
- Values at DAM 1.0 represent normal maximum torque

**Common Modifications:**
- Generally not modified - this is engine protection
- May increase limits slightly for engines with consistent DAM 1.0
- Reducing limits provides more conservative protection

**Considerations:**
- This table is a safety system - modify with extreme caution
- Frequent low DAM indicates fuel/timing/hardware issues
- Address root cause of DAM drops rather than modifying limits

## Warnings

- **CRITICAL SAFETY TABLE**: Increasing limits can cause engine damage
- Low DAM indicates knock - torque reduction protects the engine
- Never increase limits to mask underlying tuning/mechanical problems
- If DAM frequently drops below 1.0, investigate and fix the cause
- Ringland failure and rod knock are common results of ignoring knock
- Always datalog DAM, knock, and timing when modifying this table

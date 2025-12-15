# Ignition - Compensation - Coolant - TGV Closed

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Coolant - TGV Closed - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation based on engine coolant temperature for TGV closed conditions. It adjusts timing for temperature variations during idle and light load operation.

**Purpose:**
- Adjusts timing based on engine temperature when TGVs are closed
- Provides cold-start timing advance for better idle
- TGV closed = idle and light load with tumble active
- Optimizes timing during warm-up phase

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive values = timing advance (typical for cold)
- Negative values = timing retard (typical for hot)
- Zero = no compensation (at normal operating temp)

**TGV Closed Context:**
When TGVs are closed, airflow tumble is active, primarily at idle and light loads. This table provides temperature compensation for these critical operating conditions.

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (Coolant Temp)**: Current engine coolant temperature

**Cold Compensation Importance:**
At idle (TGV closed), cold compensation is critical:
- Cold idle is prone to rough running
- Timing advance helps combustion efficiency
- Proper cold timing aids fast warm-up

**Application with Activation:**
Like the TGV Open version, this may be scaled by an activation table for RPM/load dependent effects.

**1D Table Format:**
The 0x16 dimension indicates 1D lookup with 16 temperature points.

**Update Rate:** Evaluated continuously during TGV-closed operation.

## Related Tables

- **[Ignition - Compensation - Coolant - TGV Closed Activation](./ignition-compensation-coolant-tgv-closed-activation.md)**: Scales this compensation
- **[Ignition - Compensation - Coolant - TGV Open](./ignition-compensation-coolant-tgv-open.md)**: Temperature compensation for TGV open
- **[Ignition - Primary - Idle/Decel - Timing A](./ignition-primary-idledecel-ignition-timing-a.md)**: Idle timing base

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **Ignition Timing**: Shows final timing with compensations
- **TGV Position**: Should be closed (0%) for this table
- **Idle Speed**: Affected by idle timing

## Tuning Notes

**Stock Behavior:** Stock provides cold-advance compensation to improve idle quality and emissions during warm-up.

**Idle Stability Focus:**
Cold idle compensation is especially important because:
- Poor fuel atomization at cold temps
- Higher friction from cold oil
- More timing advance compensates for these losses

**Common Modifications:**
- Usually left at stock for stable cold idle
- May adjust if cold idle is rough despite proper warm-up enrichment
- Hot operation rarely needs modification

**TGV Delete Consideration:**
If TGV is deleted, this table may be irrelevant. Verify which tables the ECU uses after TGV delete.

## Warnings

⚠️ **Cold Idle Critical**: Changes directly affect cold idle quality.

⚠️ **Warm-Up Emissions**: Cold timing affects catalyst light-off time.

⚠️ **TGV State**: Only applies when TGVs are closed.

**Safe Practices:**
- Test cold start and idle quality after changes
- Monitor idle stability across temperature range
- Verify smooth transition as engine warms

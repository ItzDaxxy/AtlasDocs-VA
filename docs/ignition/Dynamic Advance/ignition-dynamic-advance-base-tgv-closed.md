# Ignition - Dynamic Advance - Base (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 21x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Dynamic Advance - Base (TGV Closed) - 2017 - RogueWRX.csv` |

## Description

This table defines the base dynamic ignition timing advance for TGV (Tumble Generator Valve) closed conditions, indexed by calculated load and RPM. Dynamic advance is additional timing that scales with the knock-learning DAM value.

**Purpose:**
- Provides additional timing advance when knock-free operation confirmed
- Scaled by DAM (Dynamic Advance Multiplier) for knock protection
- TGV closed = idle and light load with tumble active
- Allows efficiency gains without knock risk

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- Range: 0° to ~4° additional advance available
- Generally lower values than TGV Open table
- Higher values at moderate loads with TGV closed

**TGV Closed Context:**
When TGVs are closed, airflow tumble improves combustion efficiency and knock resistance. This table provides appropriate dynamic advance for these improved-mixing conditions.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.8360
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 0.0000 to 7600.0000
- **Points**: 21

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
--------------------------------------------------------------------------------------------------------------------
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.5150 |     3.5150 |     3.8665 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.1635 |     3.1635 |     3.8665 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.1635 |     2.1090 |     3.8665 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.1635 |     2.1090 |     3.8665 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     2.1090 |     3.1635 |     2.1090 |     2.1090 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     3.1635 |     2.1090 |     2.1090 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Pattern Analysis:**
- **Very Low Load (0-0.5 g/rev)**: Zero advance - idle covered by primary maps
- **Moderate Load (0.6-1.0 g/rev)**: Values of 2-4° advance
- **Higher Load (>1.0 g/rev)**: Values vary, generally moderate
- **Consistent across RPM**: Similar values at each load point

**Compared to TGV Open:**
TGV Closed table generally has similar or slightly lower values than TGV Open. The improved combustion from tumble allows efficient operation with modest additional advance.

**Update Rate:** Calculated every ignition event.

## Related Tables

- **[Ignition - Dynamic Advance - Base (TGV Open)](./ignition-dynamic-advance-base-tgv-open.md)**: Dynamic advance for TGV open
- **[Ignition - Dynamic Advance - DAM Initial Value](./ignition-dynamic-advance-dam-initial-value.md)**: DAM starting value
- **[Ignition - Dynamic Advance - Base Multiplier](./ignition-dynamic-advance-base-multiplier.md)**: DAM to multiplier conversion
- **[Ignition - Dynamic Advance - Adder (TGV Closed)](./ignition-dynamic-advance-adder-adder-tgv-closed.md)**: Additional advance values

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Scales this table's output
- **Ignition Timing**: Final actual timing
- **Feedback Knock Correction**: Real-time knock retard
- **Fine Knock Learn**: Per-cylinder learned corrections
- **TGV Position**: Should be 0% (closed) for this table

## Tuning Notes

**Stock Behavior:** Stock provides conservative dynamic advance appropriate for TGV-closed conditions. The improved combustion from tumble allows these values without knock issues.

**TGV Delete Consideration:**
If TGV is deleted (fixed open), this table may be irrelevant - only TGV Open tables would be used. Verify TGV position signal when tuning.

**Common Modifications:**
- Generally left at stock for idle stability
- May be zeroed if all timing tuned into primary maps
- Can fine-tune idle and light-load timing behavior

**Idle Timing:**
At idle (very low load), values are zero. Dynamic advance doesn't affect idle timing directly - idle timing is controlled by primary maps and idle-specific compensations.

## Warnings

⚠️ **Idle Quality**: While this table doesn't directly affect idle (zero values at idle loads), transitions in/out of idle may be affected.

⚠️ **TGV State Dependency**: Only applies when TGVs are closed - verify TGV operation.

⚠️ **DAM Scaling**: Actual advance depends on current DAM value.

**Safe Practices:**
- Monitor knock during TGV-closed operation (idle, light cruise)
- Test modifications at various coolant temperatures
- If TGV deleted, verify ECU behavior and table selection

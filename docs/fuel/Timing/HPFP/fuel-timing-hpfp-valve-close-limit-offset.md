# Fuel - Timing - HPFP - Valve Close Limit Offset

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Valve Close Limit Offset - 2017 - RogueWRX.csv` |

## Description

This table defines an offset applied to the HPFP valve close limit, indexed by RPM. It modifies the close timing limit for specific RPM ranges, allowing fine-tuning of pump output across the operating range.

**Purpose:**
- Adjusts close limit based on RPM
- Allows RPM-specific pump output tuning
- Modifies effective close timing limit

**Value Interpretation:**
- Values in degrees (offset to close limit)
- Positive values increase (later) close limit
- Negative values decrease (earlier) close limit
- Applied to IPW-based close limit calculation

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 200.0000 to 7000.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   200.0000 |   400.0000 |   800.0000 |  1000.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using RPM:
1. Calculate base close limit from IPW table
2. Look up offset from this table based on RPM
3. Apply offset to modify effective close limit
4. Resulting limit constrains valve close timing

**Limit Calculation:**
```
Effective Close Limit = IPW Close Limit + Offset(RPM)
```

**Update Rate:** Calculated every HPFP event.

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Limit (IPW)](./fuel-timing-hpfp-valve-close-limit-ipw.md)**: Base close limit
- **[Fuel - Timing - HPFP - Valve Close Limit Minimum](./fuel-timing-hpfp-valve-close-limit-minimum.md)**: Absolute minimum
- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Base close timing

## Related Datalog Parameters

- **RPM**: X-axis input for table lookup
- **Fuel Pressure (High) (kPa)**: Resulting pressure
- **HPFP Duty Cycle (%)**: Pump control effort
- **Injector Pulse Width (ms)**: Relates to fuel demand

## Tuning Notes

**Stock Behavior:** Stock offset provides RPM-specific fine-tuning of close limits.

**Common Modifications:**
- Adjust to modify pump output at specific RPMs
- Negative offset = earlier close limit = more pump output
- Positive offset = later close limit = less pump output

**Use Cases:**
- Address pressure droop at specific RPMs
- Balance pump output across RPM range
- Fine-tune after HPFP modifications

## Warnings

⚠️ **Limit Integrity**: Offset must not allow close timing below absolute minimum (225°).

⚠️ **RPM-Specific Effects**: Changes only affect specific RPM ranges.

**Safe Practices:**
- Make small adjustments (±5°)
- Verify pressure control after modifications
- Ensure minimum limit still enforced

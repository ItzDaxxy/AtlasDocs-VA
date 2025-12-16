# Fuel - Timing - HPFP - Fuel Over/Under Pressure Offset

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | KPA |
| **Source File** | `Under Pressure Offset - 2017 - RogueWRX.csv` |

## Description

This table defines pressure offset values used when fuel rail pressure deviates from the target (over or under pressure conditions). It adjusts HPFP operation to correct pressure errors.

**Purpose:**
- Compensates for fuel pressure deviations from target
- Adjusts HPFP timing when over-pressure or under-pressure detected
- Helps maintain stable fuel rail pressure

**Value Interpretation:**
- Values in kPa representing pressure offset
- Applied to HPFP control calculations when pressure error exists
- Allows RPM-specific compensation for pressure regulation

## Axes

### X-Axis

- **Parameter**: Fuel - Injectors - RPM
- **Unit**: NONE
- **Range**: 0.0000 to 6400.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: KPA
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |   400.0000 |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using RPM to determine the pressure offset. This offset is applied to HPFP control calculations when measured pressure doesn't match target.

**Pressure Correction Loop:**
1. ECU compares actual fuel pressure to target
2. If deviation exists, lookup offset from this table
3. Offset modifies HPFP timing to correct pressure
4. Continuous feedback loop maintains target pressure

**Update Rate:** Calculated as part of HPFP pressure control loop.

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Base HPFP timing
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Target pressure
- **[Fuel - Pressure - Maximum Pressure DTC Threshold](./fuel-pressure-maximum-pressure-dtc-threshold.md)**: Over-pressure fault threshold

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Actual measured pressure
- **RPM**: X-axis input for table lookup
- **HPFP Duty Cycle (%)**: Pump control effort
- **Fuel Pressure Target (kPa)**: Commanded pressure

## Tuning Notes

**Stock Behavior:** Stock calibration provides pressure regulation offsets that maintain stable fuel pressure across RPM range.

**Common Modifications:**
- Generally left at stock for proper pressure regulation
- May need adjustment if experiencing pressure instability
- HPFP upgrades may require recalibration

## Warnings

⚠️ **Pressure Regulation Critical**: This table affects fuel pressure control. Incorrect values cause unstable pressure.

**Safe Practices:**
- Monitor fuel pressure during operation
- Verify pressure tracks target across operating conditions

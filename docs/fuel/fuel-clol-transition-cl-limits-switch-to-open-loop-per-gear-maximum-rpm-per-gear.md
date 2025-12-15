# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Per Gear - Maximum RPM Per Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x6 |
| **Data Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Per Gear - Maximum RPM Per Gear - 2018 - LF9C102P.csv` |

## Description

This table defines maximum RPM thresholds per gear above which the ECU switches from closed-loop to open-loop fuel control. Different gears may have different RPM limits for CL operation, accounting for varying load characteristics at different gear ratios.

## Axes

### X-Axis

- **Parameter**: None
- **Unit**: NONE
- **Range**: 1.0000 to 6.0000
- **Points**: 6

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     1.0000 |     2.0000 |     3.0000 |     4.0000 |     5.0000 |     6.0000 |
------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU reads this 1D table using gear position as the index:
- **Index 1**: First gear RPM limit
- **Index 2**: Second gear RPM limit
- **Index 3**: Third gear RPM limit
- **Index 4**: Fourth gear RPM limit
- **Index 5**: Fifth gear RPM limit
- **Index 6**: Sixth gear RPM limit

When current RPM exceeds the limit for the current gear, the ECU switches from closed-loop to open-loop fuel control. This allows gear-specific RPM thresholds, recognizing that different gears see different load characteristics at the same RPM.

**Operating Logic:**
- Lower gears typically have lower RPM limits (higher load per RPM in lower gears)
- Higher gears may allow higher RPM before triggering OL
- Values of 0 or very high numbers may indicate gear is ignored

**Update Rate:** Evaluated continuously during closed-loop operation to determine if RPM limit is exceeded.

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Primary load-based CL limit
- **[Fuel - CL/OL Transition - Vehicle Speed Maximum](./fuel-clol-transition-cl-limits-switch-to-open-loop-vehicle-speed-vehicle-speed-maximum.md)**: Speed-based CL limit
- **[Fuel - Power Enrichment - Hysteresis (Enriching)](./fuel-power-enrichment-hysteresis-enriching.md)**: Load-based enrichment entry

## Related Datalog Parameters

- **RPM**: Compare to per-gear threshold
- **Gear Position**: Determines which table column is active
- **Fuel Mode**: Verify OL activation when RPM exceeds gear-specific limit
- **Calculated Load (g/rev)**: Correlates with RPM and gear

## Tuning Notes

**Stock Behavior:** Stock values provide gear-appropriate RPM limits for CL/OL switching, accounting for different load characteristics across gear ratios.

**Common Modifications:**
- **Lower Limits**: Earlier OL entry for more conservative operation
- **Higher Limits**: Extended CL operation for better fuel economy
- **Gear-Specific Tuning**: May adjust individual gears based on usage pattern

**First/Second Gear Considerations:** Lower gears see higher load per RPM due to mechanical advantage. May warrant lower RPM limits to trigger enrichment sooner.

**Track Use:** May need lower limits in all gears to ensure enrichment during aggressive driving, or rely on load-based switching instead.

## Warnings

⚠️ **Load vs RPM**: RPM alone doesn't indicate engine load. High RPM at light throttle (coasting in gear) doesn't need enrichment. The ECU uses multiple criteria (RPM, load, fuel target) for complete CL/OL logic.

⚠️ **Rev Limiter Interaction**: Ensure RPM limits here don't conflict with rev limiter behavior. The ECU should switch to OL well before rev limiter activates during WOT.

**Safe Practices:**
- Verify load-based switching is working properly before relying on RPM limits
- Test in each gear to confirm expected OL activation
- Log RPM, Fuel Mode, and Load during varied driving conditions

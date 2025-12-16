# Fuel - Timing - HPFP - Valve Close Limit (IPW)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x20 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Valve Close Limit (IPW) - 2017 - RogueWRX.csv` |

## Description

This table defines the latest allowable HPFP valve close timing as a function of RPM and Injector Pulse Width. It prevents the valve from closing too late, which would result in insufficient pressurization for the fuel demand.

**Purpose:**
- Limits how late the HPFP valve can close
- Ensures adequate pumping stroke for current fuel demand (IPW)
- Prevents fuel starvation during high fuel demand conditions

**Value Interpretation:**
- Values in crankshaft degrees (limit values)
- Higher IPW (more fuel demand) = earlier close limit required
- Lower values = valve must close earlier = more pressurization
- Ensures pump output matches injector demand

## Axes

### X-Axis

- **Parameter**: Fuel - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 400.0000 to 8000.0000
- **Points**: 20

### Y-Axis

- **Parameter**: None
- **Unit**: NONE
- **Range**: 156.0000 to 9375.0000
- **Points**: 16

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   400.0000 |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |  3200.0000 |
--------------------------------------------------------------------------------------------------------------------
  156.0000 |   334.4000 |   327.2000 |   320.0000 |   319.2000 |   318.6000 |   317.3000 |   316.5000 |   316.2000 |
  313.0000 |   332.0000 |   324.8000 |   317.6000 |   316.8000 |   316.2000 |   314.9000 |   314.1000 |   313.8000 |
  625.0000 |   327.2000 |   320.0000 |   312.8000 |   312.0000 |   311.4000 |   310.1000 |   309.3000 |   309.0000 |
  938.0000 |   322.4000 |   315.2000 |   308.0000 |   307.2000 |   306.6000 |   305.3000 |   304.5000 |   304.2000 |
 1250.0000 |   317.6000 |   310.4000 |   303.2000 |   302.4000 |   301.8000 |   300.5000 |   299.7000 |   299.4000 |
 1563.0000 |   314.3000 |   307.1000 |   299.9000 |   299.1000 |   298.5000 |   297.2000 |   296.4000 |   296.1000 |
 2344.0000 |   308.8000 |   301.6000 |   294.4000 |   293.6000 |   293.0000 |   291.7000 |   290.9000 |   290.6000 |
 3125.0000 |   303.3000 |   296.1000 |   288.9000 |   288.1000 |   287.5000 |   286.2000 |   285.4000 |   285.1000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Current engine speed
- **Y-Axis (IPW)**: Injector Pulse Width representing fuel demand

**Limit Application:**
```
Effective Close Timing = min(Base Close Timing, Close Limit from this table)
```

If the base close timing would result in insufficient pumping for current fuel demand, this limit forces earlier closing.

**Table Pattern:**
- Higher IPW (more fuel): Earlier limit (lower degrees)
- Higher RPM: Slightly later limits (less time per cycle already)
- This ensures the HPFP can supply required fuel volume

**Update Rate:** Calculated every HPFP event.

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Base close timing (limited by this table)
- **[Fuel - Timing - HPFP - Valve Close Limit Minimum](./fuel-timing-hpfp-valve-close-limit-minimum.md)**: Absolute minimum close timing
- **[Fuel - Timing - HPFP - Valve Close Limit Offset](./fuel-timing-hpfp-valve-close-limit-offset.md)**: Offset for close limit

## Related Datalog Parameters

- **Injector Pulse Width (ms)**: Y-axis input
- **RPM**: X-axis input
- **Fuel Pressure (High) (kPa)**: Should remain at target with proper limits
- **HPFP Duty Cycle (%)**: High duty may indicate limit is being applied

## Tuning Notes

**Stock Behavior:** Stock limits ensure HPFP can supply fuel for all normal operating conditions.

**Common Modifications:**
- **Higher Power Builds**: May need earlier limits (lower values) to supply more fuel
- **Larger Injectors**: Higher IPW values may need corresponding limit adjustments
- Ensures HPFP doesn't become limiting factor at high power

**Fuel System Capacity:**
If experiencing fuel pressure drop during WOT:
1. Check if HPFP duty cycle is maxed
2. Verify close limits aren't too late for fuel demand
3. Earlier limits (lower values) increase pump output

## Warnings

⚠️ **Fuel Starvation Risk**: If limits are too late, HPFP may not produce enough flow, causing lean condition.

⚠️ **High Power Applications**: Aggressive power builds may exceed stock HPFP flow capability regardless of timing.

**Safe Practices:**
- Monitor fuel pressure during WOT at all RPMs
- Verify no pressure drop under max fuel demand
- Consider HPFP upgrade for significant power increases

# Fuel - Injectors - Start of Injection - Cranking

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 8x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Injectors - Start of Injection - Cranking - 2017 - RogueWRX.csv` |

## Description

This table defines the Start of Injection (SOI) timing during engine cranking, indexed by coolant temperature and cranking RPM. Cranking SOI is critical for reliable starting across temperature ranges.

**Purpose:**
- Optimizes fuel injection timing during cranking
- Adjusts timing based on temperature for cold start optimization
- Accounts for varying cranking speeds

**Value Interpretation:**
- Values in crankshaft degrees
- Very cold temps (-40 to -30°C): 140° timing
- Normal temps (-20°C and warmer): Progresses from -20° to 53°
- The dramatic difference between cold and normal operation reflects cold-start requirements

**Cold Start Challenge:**
Cold starts require special injection timing:
- Cold fuel atomizes poorly
- Cold cylinder walls cause fuel condensation
- Early injection may help fuel vaporize from hot surfaces
- The 140° timing at extreme cold represents a very different strategy

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Fueling - Injectors - RPM
- **Unit**: NONE
- **Range**: 200.0000 to 900.0000
- **Points**: 8

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
  200.0000 |   140.0000 |   140.0000 |   -20.0000 |   -20.0000 |   -20.0000 |   -20.0000 |   -20.0000 |   -20.0000 |
  300.0000 |   140.0000 |   140.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  400.0000 |   140.0000 |   140.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |    10.0000 |
  500.0000 |   140.0000 |   140.0000 |    20.0000 |    20.0000 |    20.0000 |    20.0000 |    20.0000 |    20.0000 |
  600.0000 |   140.0000 |   140.0000 |    30.0000 |    30.0000 |    30.0000 |    30.0000 |    30.0000 |    30.0000 |
  700.0000 |   140.0000 |   140.0000 |    40.0000 |    40.0000 |    40.0000 |    40.0000 |    40.0000 |    40.0000 |
  800.0000 |   140.0000 |   140.0000 |    50.0000 |    50.0000 |    50.0000 |    50.0000 |    50.0000 |    50.0000 |
  900.0000 |   140.0000 |   140.0000 |    53.0000 |    53.0000 |    53.0000 |    53.0000 |    53.0000 |    53.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Coolant Temp)**: Engine temperature at startup
- **Y-Axis (RPM)**: Cranking speed (200-900 RPM range)

**Cranking SOI Progression:**
At -20°C and warmer, SOI progresses from:
- -20° at 200 RPM (very early crank)
- 53° at 900 RPM (engine catching)

This progression accounts for the changing cylinder fill and dynamics as cranking speed increases.

**Extreme Cold Operation:**
At -40 to -30°C, timing is 140° regardless of RPM. This represents:
- Likely targeting different part of engine cycle
- May inject during open valve for cold enrichment
- Optimized for extremely low temperature fuel behavior

**Update Rate:** Evaluated continuously during cranking until engine starts.

## Related Tables

- **[Fuel - Injectors - Start of Injection - Homogeneous](./fuel-injectors-start-of-injection-homogeneous.md)**: Normal operation SOI (transitions to after start)
- **[Fuel - Pressure - Fuel Pressure Target Cranking](./fuel-pressure-fuel-pressure-target-cranking.md)**: Cranking fuel pressure
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Injector flow rate

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **RPM**: Y-axis input (cranking speed)
- **Injector Timing (deg)**: Commanded SOI during cranking
- **Engine Runtime**: Time since cranking started

## Tuning Notes

**Stock Behavior:** Stock calibration provides optimized cranking SOI across the full temperature range for reliable starting.

**Common Modifications:**
- Generally left at stock unless experiencing specific start issues
- May need adjustment with different injectors (spray pattern differences)
- Cold climate tuning may require attention to extreme cold temps

**Starting Issues Diagnosis:**
If experiencing hard starts:
1. Verify fuel pressure builds correctly during cranking
2. Check injector pulse width is adequate
3. SOI timing may need adjustment if injectors have different spray characteristics

**Temperature Threshold:**
Notice the dramatic change between -30°C and -20°C (140° to -20°). This represents:
- Different starting strategy for extreme cold
- May need adjustment if operating in very cold climates
- Transition point could be smoothed if issues occur

## Warnings

⚠️ **Cold Start Critical**: Cranking SOI significantly affects cold start reliability. Incorrect timing causes hard starts, extended cranking, and potential flooding.

⚠️ **Temperature Calibration**: The extreme cold timing (140°) is specifically calibrated. Don't modify unless experiencing specific issues in that temp range.

⚠️ **Injector-Specific**: Different injector spray patterns may require different cranking SOI for reliable starting.

**Safe Practices:**
- Test any changes across temperature range
- Verify start reliability in both cold and hot conditions
- Keep original values available for reference

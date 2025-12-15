# Fuel - Pressure - Fuel Pressure Target Idle

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PASCAL |
| **Source File** | `Fuel - Pressure - Fuel Pressure Target Idle - 2017 - RogueWRX.csv` |

## Description

This table defines the target high-pressure fuel system pressure during idle conditions, indexed by coolant temperature. Lower pressure at idle reduces HPFP parasitic load and noise while maintaining adequate pressure for idle fuel delivery.

**Purpose:**
- Sets HPFP pressure targets specifically for idle operation
- Reduces fuel pressure (and pump load) when high pressure isn't needed
- Adjusts based on coolant temperature for warm-up behavior

**Value Interpretation:**
- Values in Pascals (divide by 1000 for kPa)
- Idle typically uses lower pressure than cruise or WOT
- Stock idle pressure typically 3,000-6,000 kPa range
- Cold temps may use different pressure than warmed-up idle

**Idle vs Normal Operation:**
- Idle: Low fuel demand, lower pressure acceptable
- Cruise/Load: Higher pressure for better atomization
- Lower idle pressure reduces HPFP noise and parasitic load

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PASCAL
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using coolant temperature as the sole axis input during idle operation.

**Interpolation Process:**
1. ECU detects idle condition (closed throttle, low load, target RPM)
2. Reads coolant temperature
3. Interpolates idle pressure target from this table
4. Commands HPFP to achieve target
5. HPFP modulates to maintain commanded pressure

**Idle Detection:**
This table is used when the ECU determines the engine is at idle, typically based on:
- Throttle position at or near closed
- Load below idle threshold
- RPM at or near idle target

**Transition Behavior:**
When transitioning from idle to load (throttle tip-in), ECU switches from this table to the main pressure table, ramping pressure up for higher fuel demands.

**Update Rate:** Continuously evaluated during idle operation.

## Related Tables

- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Pressure targets during normal operation
- **[Fuel - Pressure - Fuel Pressure Target Cranking](./fuel-pressure-fuel-pressure-target-cranking.md)**: Cranking pressure targets
- **[Fuel - Pressure - Maximum Pressure DTC Threshold](./fuel-pressure-maximum-pressure-dtc-threshold.md)**: Over-pressure protection

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Compare to target at idle
- **Coolant Temperature (°C)**: Input axis for table lookup
- **HPFP Duty Cycle (%)**: Pump effort to maintain idle pressure
- **Throttle Position (%)**: Confirms idle condition
- **RPM**: Should be at idle target when this table is active

## Tuning Notes

**Stock Behavior:** Stock calibration uses lower pressure at idle to reduce HPFP noise and parasitic loss while maintaining adequate fueling.

**Common Modifications:**
- **Higher Idle Pressure**: May be needed with larger injectors for proper atomization at idle
- **Lower Idle Pressure**: Reduce if HPFP noise is objectionable (verify fueling remains adequate)
- Generally adjusted in conjunction with injector changes

**Larger Injectors:** Direct injection injectors have specific pressure requirements. Larger injector orifices may need higher pressure to atomize properly at idle fuel demands.

**NVH Considerations:** HPFP operation is audible. Higher pressure = more pump noise. Stock calibration balances fueling needs with acceptable noise levels.

## Warnings

⚠️ **Minimum Pressure**: Too low pressure at idle can cause poor atomization, rough idle, and potential misfires.

⚠️ **Injector Compatibility**: When changing injectors, verify idle pressure provides adequate atomization. Poor atomization causes carbon buildup and rough running.

**Safe Practices:**
- Test idle quality across temperature range after modifications
- Monitor for misfires or rough idle if lowering pressure
- Verify AFR remains stable at idle

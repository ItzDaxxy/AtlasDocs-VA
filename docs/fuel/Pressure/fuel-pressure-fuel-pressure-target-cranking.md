# Fuel - Pressure - Fuel Pressure Target Cranking

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 8x4 |
| **Data Unit** | PASCAL |
| **Source File** | `Fuel - Pressure - Fuel Pressure Target Cranking - 2017 - RogueWRX.csv` |

## Description

This table defines the target high-pressure fuel system pressure during engine cranking, indexed by RPM and coolant temperature. The HPFP (High Pressure Fuel Pump) must quickly build pressure to enable direct injection during cold starts.

**Purpose:**
- Sets HPFP pressure targets during cranking (engine starting)
- Adjusts pressure based on coolant temperature (cold starts need different pressure)
- Ensures adequate pressure for reliable direct injection during startup

**Value Interpretation:**
- Values in Pascals (divide by 1000 for kPa)
- ~15,009 kPa = ~15 MPa = 15,000 kPa (maximum cranking pressure)
- ~9,976 kPa = ~10 MPa (lower pressure at very cold temps, low RPM)
- Higher pressure aids fuel atomization for combustion

**Temperature and RPM Relationship:**
- Cold temps (-30 to 0°C): May use lower initial pressure, ramping up with RPM
- Warm temps (20-80°C): Higher pressure sooner for reliable combustion
- Higher cranking RPM: Generally higher pressure targets

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 400.0000 to 1600.0000
- **Points**: 4

### Y-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -30.0000 to 80.0000
- **Points**: 8

## Cell Values

- **Unit**: PASCAL
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   400.0000 |   600.0000 |   800.0000 |  1600.0000 |
----------------------------------------------------------------
  -30.0000 | 15009280.0000 | 15009280.0000 | 15009280.0000 | 15009280.0000 |
  -20.0000 | 11989120.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
  -10.0000 | 11989120.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
    0.0000 | 9975680.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
   10.0000 | 9975680.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
   20.0000 | 9975680.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
   40.0000 | 9975680.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
   80.0000 | 9975680.0000 | 12538240.0000 | 15009280.0000 | 15009280.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Cranking speed (400-1600 RPM range during startup)
- **Y-Axis (Coolant Temp)**: Engine temperature at startup

**Interpolation Process:**
1. Read current cranking RPM and coolant temperature
2. Interpolate between nearest axis breakpoints
3. Command HPFP to achieve interpolated pressure target
4. HPFP feedback loop adjusts to match target

**Cranking Sequence:**
1. Key-on: HPFP begins pressurizing fuel rail
2. Cranking starts: ECU looks up pressure target from this table
3. As RPM climbs during crank, pressure target may increase
4. Once engine starts and stabilizes, transitions to normal pressure tables

**Update Rate:** Evaluated continuously during cranking until engine starts.

## Related Tables

- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Normal operation pressure targets
- **[Fuel - Pressure - Fuel Pressure Target Idle](./fuel-pressure-fuel-pressure-target-idle.md)**: Idle pressure targets
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Injector flow rate

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Compare to target during cranking
- **RPM**: X-axis input during cranking
- **Coolant Temperature (°C)**: Y-axis input
- **HPFP Duty Cycle (%)**: Pump effort to achieve target

## Tuning Notes

**Stock Behavior:** Stock calibration provides optimized pressure targets for reliable cold and hot starts across all temperature ranges.

**Common Modifications:**
- **Higher Pressure**: May improve cold start atomization with larger injectors
- **Lower Pressure**: Generally not recommended (risk of poor starts)
- **Temperature Compensation**: May adjust for specific cold-climate challenges

**Larger Injectors:** When upgrading injectors, may need higher rail pressure during cranking to achieve proper atomization with larger injector holes.

**Cold Start Issues:** If experiencing hard starts in cold weather, verify pressure targets are being achieved. Low battery voltage can prevent HPFP from building adequate pressure.

## Warnings

⚠️ **Pressure Limits**: The HPFP system has physical limits (~20 MPa max). Don't set targets beyond system capability.

⚠️ **Cold Start Sensitivity**: Cranking pressure is critical for starting. Inadequate pressure causes poor atomization and hard starts.

⚠️ **HPFP Wear**: Consistently commanding maximum pressure during all cranking conditions increases pump wear. Stock calibration balances performance with longevity.

**Safe Practices:**
- Test changes across temperature range (cold and hot starts)
- Monitor HPFP duty cycle (high duty during cranking is normal)
- Verify actual pressure matches target

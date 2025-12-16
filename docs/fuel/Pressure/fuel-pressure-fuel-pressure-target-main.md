# Fuel - Pressure - Fuel Pressure Target Main

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | PASCAL |
| **Source File** | `Fuel - Pressure - Fuel Pressure Target Main - 2017 - RogueWRX.csv` |

## Description

This table defines the target fuel rail pressure for the High Pressure Fuel Pump (HPFP) during normal engine operation. The FA20 DIT engine uses direct injection with fuel pressures ranging from approximately 3,000 kPa at idle to over 20,000 kPa at high load.

**Purpose:**
- Higher fuel pressure enables finer fuel atomization for better combustion
- Allows sufficient fuel flow at high load/RPM when injector on-time is limited
- Improves fuel mixture homogeneity especially during cold start and transient conditions

**Value Interpretation:**
- Values are in Pascals (displayed values like 10982400 Pa = ~10,982 kPa or ~1,593 psi)
- Low load cells: ~3,000-5,000 kPa (435-725 psi)
- High load cells: ~15,000-20,000 kPa (2,175-2,900 psi)

**Activation Conditions:**
- Used during normal engine operation after startup
- Separate tables exist for cranking and idle conditions
- ECU controls HPFP solenoid duty cycle to achieve target pressure

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 200.0000 to 6000.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1294 to 3.1056
- **Points**: 16

## Cell Values

- **Unit**: PASCAL
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   200.0000 |   400.0000 |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |
--------------------------------------------------------------------------------------------------------------------
    0.1294 | 4026880.0000 | 4026880.0000 | 4026880.0000 | 4026880.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 |
    0.2588 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 | 3020160.0000 |
    0.3882 | 5033600.0000 | 5033600.0000 | 5033600.0000 | 5033600.0000 | 5033600.0000 | 5033600.0000 | 5033600.0000 | 5033600.0000 |
    0.5176 | 7047040.0000 | 7047040.0000 | 7047040.0000 | 7047040.0000 | 7047040.0000 | 7047040.0000 | 7047040.0000 | 7047040.0000 |
    0.6470 | 8968960.0000 | 8968960.0000 | 8968960.0000 | 8968960.0000 | 8968960.0000 | 8968960.0000 | 8968960.0000 | 8968960.0000 |
    0.7764 | 9975680.0000 | 9975680.0000 | 9975680.0000 | 9975680.0000 | 9975680.0000 | 9975680.0000 | 9975680.0000 | 10982400.0000 |
    0.9058 | 10982400.0000 | 10982400.0000 | 10982400.0000 | 10982400.0000 | 10982400.0000 | 10982400.0000 | 10982400.0000 | 11989120.0000 |
    1.0352 | 11531520.0000 | 11531520.0000 | 11531520.0000 | 11531520.0000 | 11531520.0000 | 11531520.0000 | 11989120.0000 | 12995840.0000 |
```

## Functional Behavior

The ECU performs bilinear interpolation on this table using:
- **X-Axis (RPM)**: Current engine speed
- **Y-Axis (Calculated Load)**: Engine load in g/rev

**Control Loop:**
1. ECU looks up target pressure from this table based on current RPM and load
2. Actual fuel rail pressure is measured by the fuel pressure sensor
3. HPFP solenoid duty cycle is adjusted to minimize error between target and actual
4. Closed-loop PI control maintains pressure at target

**Response Characteristics:**
- HPFP can increase pressure quickly (cam-driven mechanical pump)
- Pressure decrease is slower (requires fuel consumption to reduce rail pressure)
- Rapid throttle changes may cause temporary pressure deviation

**Update Rate:** Pressure target is updated every engine cycle, with HPFP control loop running at high frequency.

## Related Tables

- **[Fuel - Pressure - Fuel Pressure Target Cranking](./fuel-pressure-fuel-pressure-target-cranking.md)**: Lower pressure targets during engine cranking
- **[Fuel - Pressure - Fuel Pressure Target Idle](./fuel-pressure-fuel-pressure-target-idle.md)**: Idle-specific pressure targets
- **[Fuel - Pressure - Maximum Pressure DTC Threshold](./fuel-pressure-maximum-pressure-dtc-threshold.md)**: Overpressure fault threshold
- **[Fuel - Timing - HPFP Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: HPFP timing control tables
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Injector flow rate at reference pressure

## Related Datalog Parameters

- **Fuel Pressure (kPa)**: Actual measured fuel rail pressure - should closely track target
- **Fuel Pressure Target (kPa)**: Commanded pressure from this table
- **HPFP Duty (%)**: Pump solenoid duty cycle - higher = more pumping
- **Calculated Load (g/rev)**: Y-axis input
- **RPM**: X-axis input
- **Injector Pulse Width (ms)**: Affected by fuel pressure (higher pressure = shorter pulse)

## Tuning Notes

**Stock Behavior:** Stock calibration targets ~5,000 kPa at idle/cruise, scaling up to ~15,000-20,000 kPa at high load. This provides adequate fuel delivery with stock injectors while minimizing pump wear and noise.

**Common Modifications:**
- **Larger Injectors**: May allow lower pressure targets since flow capacity increases
- **Higher Power Levels**: May require higher pressure targets if approaching injector duty cycle limits
- **E85 Operation**: Higher fuel flow requirements may need increased pressure targets

**Recommended Approach:**
1. Log actual vs target fuel pressure across operating conditions
2. Monitor injector duty cycle - if approaching 85%+, consider increasing pressure
3. Increase targets in small increments (~500-1000 kPa)
4. Verify HPFP can maintain target (actual should track target)

**Validation:** Actual pressure should track within ~500 kPa of target. Persistent deviation indicates pump capacity or mechanical issue.

## Warnings

⚠️ **Overpressure Risk**: Excessively high pressure targets can:
- Damage fuel system components (pump, lines, injectors, sensor)
- Cause fuel leaks which present fire hazard
- Trigger Maximum Pressure DTC and potential limp mode

⚠️ **Underpressure Risk**: If actual pressure cannot reach target:
- Injectors cannot deliver commanded fuel quantity
- Results in lean condition and potential engine damage
- Common with worn HPFP or failing low-pressure fuel pump

**Safe Operating Limits:**
- Maximum recommended: ~20,000 kPa (stock HPFP limit)
- Never exceed sensor range or DTC threshold
- Upgraded HPFP required for sustained operation above ~18,000 kPa

**Signs of Problems:**
- Actual pressure consistently below target: HPFP capacity issue
- Pressure spikes or oscillation: Air in fuel system or failing pressure regulator
- DTC P0087 (Fuel Rail Pressure Too Low): Indicates delivery issue
- Audible fuel pump whine: Normal at high pressure, excessive noise may indicate wear

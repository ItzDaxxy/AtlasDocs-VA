# Fuel - Timing - HPFP - Valve Close Base

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Valve Close Base - 2017 - RogueWRX.csv` |

## Description

This table defines the base timing for the HPFP (High Pressure Fuel Pump) valve closing event, indexed by RPM and battery voltage. The HPFP uses a cam-driven plunger with an electronically controlled spill valve - controlling when this valve closes determines how much fuel is pressurized.

**Purpose:**
- Controls HPFP valve closing timing relative to cam position
- Determines the effective pumping stroke and pressure output
- Compensates for battery voltage effects on solenoid response time

**Value Interpretation:**
- Values in crankshaft degrees
- Values around 345° represent late closing (less pumping)
- Lower values (317-331°) represent earlier closing (more pumping)
- Earlier closing = longer effective stroke = higher pressure capability

**Battery Voltage Effect:**
The HPFP solenoid response time varies with voltage:
- Low voltage: Slower solenoid, timing compensation needed
- Normal voltage (10V+): Nominal response time
- The table compensates to maintain consistent effective timing

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 200.0000 to 7000.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Battery Voltage
- **Unit**: VOLTS
- **Range**: 6.0156 to 16.0156
- **Points**: 16

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   200.0000 |   400.0000 |   800.0000 |  1000.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |
--------------------------------------------------------------------------------------------------------------------
    6.0156 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |
    6.9531 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |
    7.9688 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |
    8.9844 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   339.0000 |   335.0000 |   333.0000 |   331.0000 |
   10.0000 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   333.0000 |   325.0000 |   321.0000 |   317.0000 |
   10.4688 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   333.0000 |   325.0000 |   321.0000 |   317.0000 |
   10.9375 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   333.0000 |   325.0000 |   321.0000 |   317.0000 |
   11.4063 |   345.0000 |   345.0000 |   345.0000 |   345.0000 |   333.0000 |   325.0000 |   321.0000 |   317.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Current engine speed
- **Y-Axis (Battery Voltage)**: Current system voltage

**HPFP Operation:**
1. Cam-driven plunger draws fuel in on down-stroke
2. On up-stroke, spill valve initially open (fuel returns to low-pressure side)
3. When ECU closes spill valve, fuel is trapped and pressurized
4. Earlier valve closing = more of stroke used for pressurization

**Table Pattern Analysis:**
- At low voltage (<9V): Constant 345° (late closing, limited pumping)
- At normal voltage (10V+): Earlier closing at higher RPM (317-333°)
- Lower values at high RPM compensate for reduced per-stroke time

**Update Rate:** Calculated every HPFP event (engine-synchronous).

## Related Tables

- **[Fuel - Timing - HPFP - Valve Open Base](./fuel-timing-hpfp-valve-open-base.md)**: Valve opening timing
- **[Fuel - Timing - HPFP - Base Offset](./fuel-timing-hpfp-base-offset.md)**: Global timing offset
- **[Fuel - Timing - HPFP - Valve Close Limit (IPW)](./fuel-timing-hpfp-valve-close-limit-ipw.md)**: IPW-based close limits
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Target pressure

## Related Datalog Parameters

- **Battery Voltage (V)**: Y-axis input
- **RPM**: X-axis input
- **Fuel Pressure (High) (kPa)**: Result of HPFP operation
- **HPFP Duty Cycle (%)**: Pump control effort

## Tuning Notes

**Stock Behavior:** Stock timing calibrated for OEM HPFP performance across voltage and RPM ranges.

**Common Modifications:**
- Generally left at stock unless experiencing HPFP issues
- May need adjustment with aftermarket HPFP (different response characteristics)
- Low voltage compensation important for reliable cranking pressure

**HPFP Upgrades:** Aftermarket HPFP may have different solenoid characteristics requiring timing recalibration.

## Warnings

⚠️ **Critical Timing**: Incorrect HPFP timing causes pressure control issues, potential fuel starvation or over-pressure.

⚠️ **Low Voltage Operation**: Ensure timing compensation adequate for low battery scenarios (cranking, high electrical load).

**Safe Practices:**
- Test across voltage range (engine-off key-on, cranking, running)
- Monitor fuel pressure during all conditions
- Maintain adequate margin for voltage variation

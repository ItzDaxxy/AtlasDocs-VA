# Fuel - Timing - HPFP - Valve Open Base

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Valve Open Base - 2017 - RogueWRX.csv` |

## Description

This table defines the base timing for the HPFP (High Pressure Fuel Pump) valve opening event, indexed by RPM and battery voltage. Opening the spill valve ends the pressurization stroke and allows fuel to return to the low-pressure side.

**Purpose:**
- Controls HPFP valve opening timing relative to cam position
- Ends the pressurization stroke at appropriate timing
- Compensates for battery voltage effects on solenoid response

**Value Interpretation:**
- Values in crankshaft degrees
- Values around 155-165° represent opening during the intake/fill portion of cycle
- Lower values at higher RPM (132-149°) account for less time per stroke
- Opening timing relative to closing timing determines effective pressurization duration

**Battery Voltage Effect:**
Solenoid opening response varies with voltage:
- Low voltage (6V): Slower response, values adjusted (155°)
- Normal voltage: Nominal response (165° at low RPM)
- Higher RPM requires earlier opening for pump dynamics

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
    6.0156 |   155.0000 |   155.0000 |   155.0000 |   155.0000 |   145.4000 |   139.0000 |   135.8000 |   132.6000 |
    6.9531 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
    7.9688 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
    8.9844 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
   10.0000 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
   10.4688 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
   10.9375 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
   11.4063 |   165.0000 |   165.0000 |   165.0000 |   165.0000 |   149.4000 |   139.0000 |   135.8000 |   132.6000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Current engine speed
- **Y-Axis (Battery Voltage)**: Current system voltage

**HPFP Timing Sequence:**
1. Valve opens at timing from this table → fuel returns to low side
2. Plunger draws fuel in during downstroke
3. Valve closes (per Valve Close Base table) → pressurization begins
4. Plunger compresses fuel on upstroke → fuel flows to rail

**Open-Close Relationship:**
The difference between close timing and open timing determines the effective pumping window. Coordinated adjustment of both tables controls HPFP output.

**Update Rate:** Calculated every HPFP event.

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Valve closing timing
- **[Fuel - Timing - HPFP - Base Offset](./fuel-timing-hpfp-base-offset.md)**: Global timing offset
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Target pressure

## Related Datalog Parameters

- **Battery Voltage (V)**: Y-axis input
- **RPM**: X-axis input
- **Fuel Pressure (High) (kPa)**: Result of HPFP operation
- **HPFP Duty Cycle (%)**: Pump control effort

## Tuning Notes

**Stock Behavior:** Stock timing works with Valve Close Base for calibrated HPFP performance.

**Common Modifications:**
- Must be modified in coordination with Valve Close Base
- Aftermarket HPFP may require recalibration
- Generally left at stock unless experiencing specific HPFP issues

**Table Analysis:**
Values decrease at higher RPM (165° → 132°), reflecting the need to open earlier as cycle time decreases. This maintains consistent pump fill time.

## Warnings

⚠️ **Coordinated Timing**: Open and close timing must be calibrated together. Changing one without the other may cause pump malfunction.

⚠️ **Pump Damage Risk**: Incorrect timing can cause cavitation or excessive stress on HPFP components.

**Safe Practices:**
- Modify both open and close tables together
- Verify pressure control across RPM range after changes
- Monitor for unusual pump noise indicating timing issues

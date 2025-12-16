# Sensors - Manifold Absolute Pressure - MAP Multiplier

## Overview

| Property | Value |
|----------|-------|
| **Category** | Sensors |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Sensors - Manifold Absolute Pressure - MAP Multiplier - 2017 - RogueWRX.csv` |

## Value

**315.0000 NONE**

## Description

The MAP Multiplier is the scaling factor used to convert the raw voltage signal from the Manifold Absolute Pressure sensor into a pressure reading. This parameter works with the MAP Offset to linearize the sensor's output:

**Pressure (kPa) = (Voltage × Multiplier) + Offset**

The factory value of 315.0000 is calibrated for the OEM 3-bar MAP sensor's voltage-to-pressure characteristics. This multiplier defines the slope of the conversion curve and must match the installed MAP sensor's specifications.

## Functional Behavior

The ECU continuously reads MAP sensor voltage (0-5V range) and applies this multiplier to calculate pressure:

1. **Voltage Reading**: ECU samples MAP sensor voltage via ADC
2. **Scaling**: Applies multiplier to convert voltage to pressure units
3. **Offset Application**: Adds MAP Offset for final pressure value
4. **Usage**: Pressure used for load calculation, fuel delivery, boost control

This calculation runs every ECU cycle, making accurate calibration critical.

## Related Tables

- **Sensors - MAP Offset**: Works with multiplier for complete conversion
- **Sensors - MAP Maximum DTC Threshold**: Fault detection for MAP sensor
- **Airflow - Boost Target**: Uses MAP for boost control
- **Engine Load Calculation**: Depends on accurate MAP readings

## Related Datalog Parameters

- **Manifold Absolute Pressure (kPa)**: Calculated pressure after conversion
- **MAP Sensor Voltage (V)**: Raw voltage input
- **Engine Load (%)**: Calculated using MAP
- **Boost Pressure (psi/kPa)**: Derived from MAP

## Tuning Notes

**When to Modify:**
- Installing aftermarket MAP sensor with different characteristics
- Upgrading to 4-bar or 5-bar MAP for higher boost
- Correcting systematic pressure reading errors

**Calculation:**
Multiplier = (P2 - P1) / (V2 - V1) from sensor datasheet

**Common Values:**
- OEM 3-bar: ~315
- AEM 3.5-bar: ~350-400
- AEM 5-bar: ~500-550
- GM 3-bar: ~300-320

## Warnings

- **CRITICAL**: Incorrect multiplier causes wrong load calculations and fuel delivery
- Always verify with mechanical boost gauge before driving under boost
- Must recalibrate MAP Offset when changing multiplier
- Can cause lean conditions leading to detonation if set too low
- May trigger P0106/P0107/P0108 DTCs if significantly wrong

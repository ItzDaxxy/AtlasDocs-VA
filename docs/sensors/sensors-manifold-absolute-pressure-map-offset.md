# Sensors - Manifold Absolute Pressure - MAP Offset

## Overview

| Property | Value |
|----------|-------|
| **Category** | Sensors |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Sensors - Manifold Absolute Pressure - MAP Offset - 2017 - RogueWRX.csv` |

## Value

**19952.0000 NONE**

## Description

The MAP Offset is the zero-point calibration value used in voltage-to-pressure conversion for the Manifold Absolute Pressure sensor. This parameter works with the MAP Multiplier to linearize the sensor's output:

**Pressure (kPa) = (Voltage × Multiplier) + Offset**

The factory value of 19952.0000 compensates for the sensor's baseline voltage characteristics. This offset represents the y-intercept of the conversion equation and corrects for the sensor's non-zero voltage at zero pressure.

## Functional Behavior

The ECU applies this offset after multiplying raw MAP voltage by the multiplier:

1. **Voltage Reading**: ECU samples MAP sensor voltage
2. **Multiplier Application**: Voltage scaled by MAP Multiplier
3. **Offset Addition**: This offset value added to scaled voltage
4. **Final Pressure**: Result is pressure in kPa used for engine calculations

The offset compensates for:
- Sensor's non-zero voltage at atmospheric pressure
- Electrical bias in sensor circuit
- Manufacturing tolerances

## Related Tables

- **Sensors - MAP Multiplier**: Must be calibrated together with offset
- **Sensors - MAP Maximum DTC Threshold**: Uses converted pressure for faults
- **Engine Load Calculation**: Depends on accurate MAP readings

## Related Datalog Parameters

- **Manifold Absolute Pressure (kPa)**: Final calculated pressure
- **MAP Sensor Voltage (V)**: Raw voltage input
- **Atmospheric Pressure (kPa)**: Reference for offset validation
- **Boost Pressure (psi/kPa)**: Derived from MAP

## Tuning Notes

**When to Modify:**
- After changing MAP Multiplier (must recalibrate offset)
- Installing aftermarket MAP sensor with different baseline
- Correcting systematic pressure reading errors

**Calibration Procedure:**
1. Set MAP Multiplier correctly first
2. At key-on engine-off, MAP should read ~atmospheric pressure (~101 kPa at sea level)
3. Calculate offset adjustment: New Offset = Old Offset + (Actual - Displayed) × Multiplier
4. Verify at multiple pressure points (vacuum, atmospheric, boost)

**Reference Points:**
- Sea level atmospheric: ~101 kPa (14.7 psi)
- Engine idle vacuum: ~30-40 kPa
- Zero boost (wastegate spring): ~100-105 kPa

## Warnings

- **CRITICAL**: Incorrect offset causes wrong pressure readings at ALL operating conditions
- Must calibrate with MAP Multiplier - cannot be set independently
- Verify with mechanical gauge before driving under boost
- Affects idle quality, fuel economy, boost control, and WOT fueling
- May trigger P0106 DTCs if atmospheric reading is implausible

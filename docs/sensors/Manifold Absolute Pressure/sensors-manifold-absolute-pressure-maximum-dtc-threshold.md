# Sensors - Manifold Absolute Pressure - Maximum DTC Threshold

## Overview

| Property | Value |
|----------|-------|
| **Category** | Sensors |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | VOLTS |
| **Source File** | `Sensors - Manifold Absolute Pressure - Maximum DTC Threshold - 2017 - RogueWRX.csv` |

## Value

**4.8447 VOLTS**

## Description

Defines the maximum voltage threshold for MAP sensor diagnostic trouble code (DTC) detection. At 4.8447V (near the 5V sensor maximum), this threshold determines when the ECU will flag a MAP sensor error for reading too high - typically indicating a shorted sensor, wiring issue, or sensor reading above its calibrated range.

This threshold is set just below the sensor's maximum output to detect fault conditions while allowing legitimate high-boost readings on upgraded MAP sensors.

## Related Tables

- **Sensors - Manifold Absolute Pressure - MAP Multiplier**: Scaling for pressure calculation
- **Sensors - Manifold Absolute Pressure - MAP Offset**: Zero-point calibration
- **Sensors - Manifold Absolute Pressure - Minimum DTC Threshold**: Low-side fault detection

## Related Datalog Parameters

- **MAP Sensor Voltage (V)**: Raw sensor input compared to this threshold
- **Manifold Pressure (kPa/psi)**: Calculated from voltage
- **Check Engine Light / DTC Status**: P0108 (MAP Circuit High) if exceeded

## Tuning Notes

**When to Modify:**
- Installing higher-range MAP sensor (3.5-bar, 4-bar, 5-bar)
- Higher range sensors may output higher voltage at equivalent pressure
- Prevent false DTCs with upgraded sensors

**Common Modifications:**
- Stock 3-bar sensor: 4.8447V appropriate
- 4-bar or 5-bar sensor: May need adjustment based on sensor specification
- Verify sensor datasheet for maximum output voltage

**Considerations:**
- Value should be slightly below sensor's actual maximum output
- Too low causes false high-pressure DTCs
- Too high disables useful fault detection

## Warnings

- Raising threshold may mask legitimate sensor faults
- Ensure upgraded MAP sensor is properly calibrated first
- False readings can cause dangerous lean conditions or overboosting
- Always verify MAP readings match actual boost during testing

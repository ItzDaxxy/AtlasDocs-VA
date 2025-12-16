# Transmission - Vehicle Speed Scalar B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Transmission - Vehicle Speed Scalar B - 2017 - RogueWRX.csv` |

## Value

**32768.0000 NONE**

## Description

Secondary scalar constant used in vehicle speed calculations. At 32768 (2^15), this binary-friendly value enables efficient bit-shift operations in the ECU's speed calculation algorithm. Like Scalar A, this power-of-two value optimizes processor performance for real-time speed computation.

This scalar works alongside Scalar A and the gear ratio tables to convert wheel speed sensor pulses or transmission output shaft speed into accurate vehicle speed readings.

**Binary Value:** 32768 = 2^15 (binary: 1000000000000000)

## Related Tables

- **Transmission - Vehicle Speed Scalar A**: Primary speed scalar (also 32768)
- **Transmission - Gear Ratios - 1st-6th**: Gear-specific ratio values
- **Speedometer Calibration**: Final speed display calculation

## Related Datalog Parameters

- **Vehicle Speed (mph/kph)**: Calculated using this scalar
- **Wheel Speed Sensors**: Raw input pulses
- **Transmission Output Shaft Speed**: Alternative speed input

## Tuning Notes

**When to Modify:**
- Significant tire size change affecting speedometer accuracy
- Differential/final drive ratio swap
- Speed sensor change (different pulse count)

**Calculation Relationship:**
This scalar is part of the speed calculation that converts sensor pulses to displayed speed. Changes affect speedometer accuracy and any speed-dependent ECU functions.

**Considerations:**
- Both Scalar A and B typically remain at 32768 for stock configurations
- Modification requires understanding of full speed calculation chain
- Prefer modifying gear ratios for tire/diff changes when possible

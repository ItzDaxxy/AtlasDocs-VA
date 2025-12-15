# Transmission - Vehicle Speed Scalar A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Transmission - Vehicle Speed Scalar A - 2017 - RogueWRX.csv` |

## Value

**32768.0000 NONE**

## Description

Binary scaling factor (32768 = 2^15) used in the ECU's vehicle speed calculation algorithm. This value works with gear ratios to convert wheel speed sensor pulses and engine RPM into accurate vehicle speed readings.

The value 32768 represents a binary shift operation in ECU firmware, allowing efficient integer math processing while maintaining precision. Using powers of 2 enables fast bit-shift operations instead of slower floating-point division.

## Functional Behavior

The ECU calculates vehicle speed using:
1. **Input**: Wheel speed sensor pulses OR engine RPM + gear position
2. **Gear Ratio Application**: Applies appropriate gear ratio
3. **Scalar Division**: Divides by this scalar (or bit-shifts by 15)
4. **Tire Circumference**: Accounts for rolling circumference
5. **Output**: Vehicle speed in km/h or mph

## Related Tables

- **Transmission - Vehicle Speed Scalar B**: Secondary/redundant scalar
- **Transmission - Gear Ratios (all gears)**: Work with scalars for speed calculation
- **Speedometer Calibration**: Final speed output

## Related Datalog Parameters

- **Vehicle Speed (km/h or mph)**: Calculated output
- **Engine RPM**: Input for calculation
- **Wheel Speed Sensor Signal**: Direct speed input
- **Gear Position**: Determines which ratio to use

## Tuning Notes

**When to Modify:**
- Non-stock tire diameter affecting speedometer accuracy
- Speedometer consistently reads high or low vs GPS
- Changed final drive ratio
- Wheel speed sensor pulse count changed

**Modification Procedure:**
1. Verify actual speedometer error with GPS
2. Calculate correction factor: Actual Speed / Displayed Speed
3. Apply correction: New Scalar = 32768 / Correction Factor
4. Test accuracy across speed range (20, 40, 60, 80+ mph)

**Example:**
- Speedometer reads 65 mph, GPS shows 60 mph
- Correction = 60/65 = 0.923
- New Scalar = 32768 / 0.923 ≈ 35506

**Tire Size Impact:**
- Larger tires: Speedometer reads LOW, increase scalar
- Smaller tires: Speedometer reads HIGH, decrease scalar

## Warnings

- Incorrect scalar causes speedometer and odometer errors
- Legal implications: Odometer accuracy required by law
- Affects speed-limited features (cruise control, speed governor)
- May cause rev-matching to target incorrect RPMs
- GPS verification critical before finalizing changes
- Modify both Scalar A and B consistently

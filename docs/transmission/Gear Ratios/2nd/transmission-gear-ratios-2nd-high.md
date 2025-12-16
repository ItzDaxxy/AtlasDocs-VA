# Transmission - Gear Ratios - 2nd - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 2nd - High - 2017 - RogueWRX.csv` |

## Value

**9319.1729 REV_PER_MI**

## Description

Defines the high-end gear ratio calculation constant for 2nd gear, expressed in engine revolutions per mile. This value combines the transmission's 2nd gear ratio with the final drive ratio and tire circumference to calculate vehicle speed from engine RPM.

At 9319.17 rev/mi, this represents the upper bound of the calculation range used for gear detection and speed calculation accuracy in 2nd gear. The ECU uses both High and Low values to properly identify when the vehicle is operating in 2nd gear based on the relationship between engine RPM and vehicle speed.

**2nd Gear Stock Ratios:**
- Transmission ratio: 2.059:1
- Final drive: 4.11:1
- Combined effective ratio: ~8.46:1

## Related Tables

- **Transmission - Gear Ratios - 2nd - Low**: Lower bound for 2nd gear calculation
- **Transmission - Gear Ratios - 1st/3rd/4th/5th/6th**: Other gear ratios
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation constants

## Related Datalog Parameters

- **Current Gear**: Calculated from ratio comparison
- **Engine RPM**: Input for gear calculation
- **Vehicle Speed (mph)**: Calculated from RPM and gear ratio
- **Calculated Gear Ratio**: RPM/Speed comparison result

## Tuning Notes

**When to Modify:**
- After transmission gear swap (STI 6-speed, close-ratio gears)
- After final drive ratio change
- After significant tire size change affecting rolling circumference

**Calculation:**
`Rev/Mile = (Trans Ratio × Final Drive × 63360) / (Tire Diameter × π)`

**Considerations:**
- Both High and Low values define the detection window for each gear
- Incorrect values cause wrong gear display and potentially incorrect gear-dependent logic
- Verify calculations match actual gear behavior via datalogging

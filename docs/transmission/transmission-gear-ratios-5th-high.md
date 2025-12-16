# Transmission - Gear Ratios - 5th - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 5th - High - 2017 - RogueWRX.csv` |

## Value

**3022.9324 REV_PER_MI**

## Description

Defines the high-end gear ratio calculation constant for 5th gear at 3022.93 rev/mi. This value sets the upper bound for 5th gear detection.

**5th Gear Stock Ratios:**
- Transmission ratio: 0.825:1
- Final drive: 4.11:1
- Combined effective ratio: ~3.39:1

5th gear is an overdrive ratio primarily used for highway cruising at moderate speeds, reducing engine RPM for improved fuel economy and reduced NVH.

## Related Tables

- **Transmission - Gear Ratios - 5th - Low**: Lower bound for 5th gear
- **Transmission - Gear Ratios - 1st-6th**: Complete gear ratio set
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation

## Related Datalog Parameters

- **Current Gear**: Gear detection output
- **Engine RPM**: Calculation input
- **Vehicle Speed (mph)**: Calculated speed

## Tuning Notes

**When to Modify:**
- Transmission or final drive changes
- Tire size modifications

**Considerations:**
- High/Low must bracket actual 5th gear ratio
- Affects gear-specific ECU strategies

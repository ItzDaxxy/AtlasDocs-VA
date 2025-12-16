# Transmission - Gear Ratios - 6th - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 6th - High - 2017 - RogueWRX.csv` |

## Value

**2495.1128 REV_PER_MI**

## Description

Defines the high-end gear ratio calculation constant for 6th gear at 2495.11 rev/mi. This value sets the upper bound for 6th gear (highest gear) detection.

**6th Gear Stock Ratios:**
- Transmission ratio: 0.648:1
- Final drive: 4.11:1
- Combined effective ratio: ~2.66:1

6th gear is the tallest overdrive ratio, used for high-speed highway cruising to minimize engine RPM and maximize fuel economy.

## Related Tables

- **Transmission - Gear Ratios - 6th - Low**: Lower bound for 6th gear
- **Transmission - Gear Ratios - 1st-5th**: Other gear ratios
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
- 6th is the highest gear - no upper overlap concern
- Affects gear-specific ECU strategies
- May see reduced use on modified vehicles preferring lower gears

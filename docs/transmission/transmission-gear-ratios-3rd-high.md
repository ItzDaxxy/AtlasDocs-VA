# Transmission - Gear Ratios - 3rd - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 3rd - High - 2017 - RogueWRX.csv` |

## Value

**5595.8647 REV_PER_MI**

## Description

Defines the high-end gear ratio calculation constant for 3rd gear, expressed in engine revolutions per mile. At 5595.86 rev/mi, this represents the upper bound for 3rd gear detection in the ECU's gear calculation logic.

**3rd Gear Stock Ratios:**
- Transmission ratio: 1.438:1
- Final drive: 4.11:1
- Combined effective ratio: ~5.91:1

3rd gear is often used for spirited driving and provides good balance between acceleration and speed range, commonly used in the 40-80 mph range.

## Related Tables

- **Transmission - Gear Ratios - 3rd - Low**: Lower bound for 3rd gear
- **Transmission - Gear Ratios - 1st/2nd/4th/5th/6th**: Other gear ratios
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation constants

## Related Datalog Parameters

- **Current Gear**: Calculated gear indicator
- **Engine RPM**: Speed calculation input
- **Vehicle Speed (mph)**: Calculated speed value
- **Gear Ratio**: Live ratio calculation

## Tuning Notes

**When to Modify:**
- Transmission swap or gear ratio change
- Final drive ratio modification
- Tire size changes

**Considerations:**
- High/Low values must bracket the actual gear ratio
- Affects gear-dependent ECU strategies (boost limits, etc.)

# Transmission - Gear Ratios - 4th - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 4th - High - 2017 - RogueWRX.csv` |

## Value

**3913.5337 REV_PER_MI**

## Description

Defines the high-end gear ratio calculation constant for 4th gear at 3913.53 rev/mi. This value sets the upper bound for 4th gear detection in the ECU's gear identification logic.

**4th Gear Stock Ratios:**
- Transmission ratio: 1.088:1
- Final drive: 4.11:1
- Combined effective ratio: ~4.47:1

4th gear is close to 1:1 ratio, providing efficient cruising with good acceleration available when needed. Commonly used in 50-90 mph range.

## Related Tables

- **Transmission - Gear Ratios - 4th - Low**: Lower bound for 4th gear
- **Transmission - Gear Ratios - 1st-6th**: Complete gear ratio set
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation constants

## Related Datalog Parameters

- **Current Gear**: Calculated gear indicator
- **Engine RPM**: Calculation input
- **Vehicle Speed (mph)**: Calculated speed

## Tuning Notes

**When to Modify:**
- Transmission swap or gear change
- Final drive modification
- Tire size change

**Considerations:**
- High/Low bracket must contain actual 4th gear ratio
- Affects gear-dependent tuning strategies

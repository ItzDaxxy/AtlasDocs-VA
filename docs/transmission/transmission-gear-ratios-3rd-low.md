# Transmission - Gear Ratios - 3rd - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 3rd - Low - 2017 - RogueWRX.csv` |

## Value

**3913.5337 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 3rd gear at 3913.53 rev/mi. This value represents the lower bound of the 3rd gear detection window.

The ECU uses the High/Low pair to identify when 3rd gear is engaged by comparing the calculated RPM/speed ratio against these bounds. Correct gear detection is essential for gear-specific boost, fuel, and timing strategies.

**3rd Gear Characteristics:**
- Versatile mid-range gear
- Common for acceleration pulls and highway merging
- Good balance of torque and speed

## Related Tables

- **Transmission - Gear Ratios - 3rd - High**: Upper bound for 3rd gear
- **Transmission - Gear Ratios - 1st-6th**: Complete gear ratio set
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation

## Related Datalog Parameters

- **Current Gear**: Gear detection output
- **Engine RPM**: Calculation input
- **Vehicle Speed (mph)**: Speed measurement

## Tuning Notes

**When to Modify:**
- Transmission or final drive changes
- Tire size modifications

**Considerations:**
- Must be lower than 3rd-High value
- Ensure no overlap with 4th-High value

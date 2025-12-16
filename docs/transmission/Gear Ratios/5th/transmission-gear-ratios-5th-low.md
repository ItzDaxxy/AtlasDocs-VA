# Transmission - Gear Ratios - 5th - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 5th - Low - 2017 - RogueWRX.csv` |

## Value

**2495.1128 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 5th gear at 2495.11 rev/mi. This value sets the lower bound of the 5th gear detection window.

The ECU uses this value with 5th-High to identify when 5th gear is engaged. Correct detection ensures proper application of gear-specific calibration strategies.

**5th Gear Characteristics:**
- First overdrive ratio
- Highway cruising gear (60-80 mph typical)
- Reduced engine RPM for efficiency

## Related Tables

- **Transmission - Gear Ratios - 5th - High**: Upper bound for 5th gear
- **Transmission - Gear Ratios - 1st-6th**: Complete ratio set
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
- Must be lower than 5th-High
- Avoid overlap with 6th-High value

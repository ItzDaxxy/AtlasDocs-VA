# Transmission - Gear Ratios - 4th - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 4th - Low - 2017 - RogueWRX.csv` |

## Value

**3022.9324 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 4th gear at 3022.93 rev/mi. This value sets the lower bound of the 4th gear detection window.

The ECU compares calculated RPM/speed ratios against this value and the 4th-High value to determine if 4th gear is engaged. Accurate gear detection enables proper gear-specific calibration strategies.

**4th Gear Characteristics:**
- Near 1:1 ratio for efficiency
- Primary highway passing gear
- Good balance for varied driving

## Related Tables

- **Transmission - Gear Ratios - 4th - High**: Upper bound for 4th gear
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
- Must be lower than 4th-High
- Avoid overlap with 5th-High value

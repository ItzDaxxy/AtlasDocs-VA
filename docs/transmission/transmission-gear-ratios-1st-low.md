# Transmission - Gear Ratios - 1st - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 1st - Low - 2017 - RogueWRX.csv` |

## Value

**9319.1729 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 1st gear at 9319.17 rev/mi. This value sets the lower bound of the 1st gear detection window.

The ECU uses this value with 1st-High to identify 1st gear operation. As the lowest gear with the highest ratio, 1st gear detection helps the ECU apply appropriate launch and low-speed strategies.

**1st Gear Stock Ratios:**
- Transmission ratio: 3.454:1
- Final drive: 4.11:1
- Combined effective ratio: ~14.2:1

**1st Gear Characteristics:**
- Highest torque multiplication
- Used for launch and very low speeds
- Critical for traction control strategies

## Related Tables

- **Transmission - Gear Ratios - 1st - High**: Upper bound for 1st gear (24637.22)
- **Transmission - Gear Ratios - 2nd-6th**: Other gear ratios
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation

## Related Datalog Parameters

- **Current Gear**: Gear detection output
- **Engine RPM**: Calculation input
- **Vehicle Speed (mph)**: Speed measurement
- **Clutch Switch**: May affect gear detection during launch

## Tuning Notes

**When to Modify:**
- Transmission or final drive changes
- Tire size modifications

**Considerations:**
- Must be lower than 1st-High value
- Affects launch control and traction strategies
- Ensure gap between 1st-Low and 2nd-High

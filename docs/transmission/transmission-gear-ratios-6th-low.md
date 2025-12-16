# Transmission - Gear Ratios - 6th - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 6th - Low - 2017 - RogueWRX.csv` |

## Value

**0.0000 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 6th gear. At 0.0 rev/mi, this value indicates no lower bound check for 6th gear detection - any ratio below 6th-High is considered 6th gear.

As the highest gear, 6th has no gear below it to differentiate from, so the lower bound is set to zero. The ECU simply checks if the calculated ratio is below 6th-High to identify 6th gear operation.

**6th Gear Characteristics:**
- Highest overdrive ratio
- Maximum fuel economy gear
- Used for sustained highway cruising (70+ mph)

## Related Tables

- **Transmission - Gear Ratios - 6th - High**: Upper bound for 6th gear (2495.11)
- **Transmission - Gear Ratios - 1st-5th**: Other gear ratios
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation

## Related Datalog Parameters

- **Current Gear**: Gear detection output
- **Engine RPM**: Calculation input
- **Vehicle Speed (mph)**: Speed measurement

## Tuning Notes

**When to Modify:**
- Generally leave at 0.0
- Only modify if adding gear detection logic changes

**Considerations:**
- Zero value is intentional for highest gear
- Provides catch-all for ratios below 6th-High threshold

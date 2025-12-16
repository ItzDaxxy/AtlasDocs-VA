# Transmission - Gear Ratios - 2nd - Low

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 2nd - Low - 2017 - RogueWRX.csv` |

## Value

**5595.8647 REV_PER_MI**

## Description

Defines the low-end gear ratio calculation constant for 2nd gear, expressed in engine revolutions per mile. At 5595.86 rev/mi, this represents the lower bound of the calculation range for 2nd gear detection.

The ECU compares the actual RPM/speed ratio against the High and Low values for each gear to determine which gear is currently engaged. This information is used for gear-dependent fuel, ignition, and boost strategies.

**2nd Gear Characteristics:**
- Primary acceleration gear after launch
- Wide speed range coverage (~15-50 mph typical use)
- High torque multiplication for strong acceleration

## Related Tables

- **Transmission - Gear Ratios - 2nd - High**: Upper bound for 2nd gear calculation
- **Transmission - Gear Ratios - 1st/3rd-6th**: Other gear ratio values
- **Transmission - Vehicle Speed Scalar A/B**: Speed calculation constants

## Related Datalog Parameters

- **Current Gear**: Calculated gear indicator
- **Engine RPM**: Speed calculation input
- **Vehicle Speed (mph)**: Calculated from gear ratio
- **Gear Ratio**: Live RPM/speed calculation

## Tuning Notes

**When to Modify:**
- Transmission swap (different gear ratios)
- Final drive change
- Significant tire size change

**Considerations:**
- Must be lower than 2nd-High value
- Gap between High and Low allows for measurement tolerance
- Incorrect values cause gear detection errors

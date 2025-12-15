# Fuel - Injectors - Start of Injection - Compensation - Compensation (Homogeneous)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Injectors - Start of Injection - Compensation - Compensation (Homogeneous) - 2017 - RogueWRX.csv` |

## Description

This table defines compensation adders for the homogeneous Start of Injection timing, indexed by calculated load and RPM. These values are added to the base SOI timing to provide fine adjustment in specific operating regions.

**Purpose:**
- Provides location-specific SOI compensation
- Fine-tunes injection timing beyond base table
- Allows targeted adjustments without changing entire base table

**Value Interpretation:**
- Values in degrees (positive or negative adders)
- Value of 0 = no compensation (use base SOI)
- Negative values (-30 to -80°) = retard SOI from base
- Positive values = advance SOI from base

**Compensation Pattern:**
The table shows zeros at low loads and specific negative values (-30° to -80°) at mid-to-high loads in certain RPM ranges. This suggests:
- Fine-tuning for specific operating regions
- Addressing combustion or emission requirements at specific load/RPM points
- May compensate for hardware characteristics not captured by base table

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.2580 to 2.0640
- **Points**: 8

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 6800.0000
- **Points**: 16

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.2580 |     0.5160 |     0.7740 |     1.0320 |     1.2900 |     1.5480 |     1.8060 |     2.0640 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -80.0000 |     0.0000 |   -60.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -60.0000 |   -80.0000 |   -30.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -80.0000 |   -60.0000 |   -60.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -80.0000 |   -40.0000 |     0.0000 |
 3200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |   -80.0000 |   -40.0000 |
 3600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**SOI Calculation with Compensation:**
```
Final SOI = Base SOI (homogeneous table) + Compensation (this table)
```

**Compensation Application:**
The interpolated compensation value is added to the base SOI. Looking at the data:
- Most cells are 0° (no compensation)
- Specific mid-load regions at mid-RPM have -60° to -80° compensation
- These targeted adjustments address specific operating regions

**Update Rate:** Calculated every engine cycle as part of SOI determination.

## Related Tables

- **[Fuel - Injectors - Start of Injection - Homogeneous](./fuel-injectors-start-of-injection-homogeneous.md)**: Base SOI (modified by this table)
- **[Fuel - Injectors - Start of Injection - Compensation Activation](./fuel-injectors-start-of-injection-compensation-compensation-activation-homogeneous.md)**: Controls when compensation is active
- **[Fuel - Injectors - Start of Injection - Homogeneous (Aggressive)](./fuel-injectors-start-of-injection-homogeneous-aggressive.md)**: Aggressive SOI table

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Injector Timing (deg)**: Final commanded SOI (includes compensation)
- **Fuel Mode**: May correlate with compensation activation

## Tuning Notes

**Stock Behavior:** Stock compensation targets specific regions with -30° to -80° SOI retard, likely for:
- Emissions optimization at specific operating points
- Combustion stability in transitional regions
- Hardware compensation for specific load/RPM combinations

**Common Modifications:**
- **Zeroing Table**: Some tuners zero this table to simplify SOI control
- Usually modified only if specific issues occur in compensation regions
- May need adjustment if base SOI table is significantly modified

**Understanding the Pattern:**
The compensation clusters around:
- Mid loads (1.29-1.81 g/rev)
- Mid RPM (1600-3200)
This may address part-throttle cruise emissions or combustion characteristics.

**Interaction with Activation:**
A companion activation table may control when this compensation is applied. Without it active, these values have no effect.

## Warnings

⚠️ **Regional Effects**: Changes only affect specific load/RPM combinations. Test those regions specifically.

⚠️ **Emission Impact**: Compensation likely addresses emission requirements. Modifications may affect emissions.

⚠️ **Activation Dependency**: This table may only apply when activation conditions are met.

**Safe Practices:**
- Understand activation conditions before modifying
- Test in specific regions where compensation is applied
- Monitor combustion stability after changes

# Fuel - Injectors - Start of Injection - Compensation - Compensation Activation (Homogeneous)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 8x8 |
| **Data Unit** | PERCENT |
| **Source File** | `Fuel - Injectors - Start of Injection - Compensation - Compensation Activation (Homogeneous) - 2017 - RogueWRX.csv` |

## Description

This table controls the activation level for SOI (Start of Injection) compensation in homogeneous mode, indexed by intake air temperature and oil temperature. It determines when/how much the SOI compensation table is applied.

**Purpose:**
- Controls activation percentage of SOI compensation
- Uses temperature conditions to determine compensation level
- Activates compensation during specific thermal conditions

**Value Interpretation:**
- Values in percent (0-100%)
- 0% = no compensation applied
- 50.2% / 100% = partial/full compensation active
- Compensation activates at high oil temp (85-100°C) combined with warm IAT (35-40°C)

## Axes

### X-Axis

- **Parameter**: Fueling - Injectors - Intake Air Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 40.0000
- **Points**: 8

### Y-Axis

- **Parameter**: Fueling - Injectors - Oil Temp
- **Unit**: CELSIUS
- **Range**: -50.0000 to 100.0000
- **Points**: 8

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |    35.0000 |    40.0000 |
--------------------------------------------------------------------------------------------------------------------
  -50.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   10.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   30.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   80.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   85.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.5020 |     0.5020 |
   90.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.5020 |     1.0000 |
  100.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.5020 |     1.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (IAT)**: Intake air temperature
- **Y-Axis (Oil Temp)**: Engine oil temperature

**Activation Logic:**
The interpolated value acts as a multiplier for the compensation:
```
Applied Compensation = Base Compensation × Activation %
```

**Table Pattern Analysis:**
- Most cells are 0% (no compensation)
- Compensation activates only at high oil temp (85°C+) AND warm IAT (35°C+)
- Suggests compensation addresses hot-soak or high-temp conditions

**Update Rate:** Calculated continuously as temperatures change.

## Related Tables

- **[Fuel - Injectors - Start of Injection - Compensation (Homogeneous)](./fuel-injectors-start-of-injection-compensation-compensation-homogeneous.md)**: The compensation values controlled by this activation
- **[Fuel - Injectors - Start of Injection - Homogeneous](./fuel-injectors-start-of-injection-homogeneous.md)**: Base SOI timing

## Related Datalog Parameters

- **Intake Air Temperature (°C)**: X-axis input
- **Oil Temperature (°C)**: Y-axis input (if available)
- **Injector Timing (deg)**: Final SOI with compensation
- **Coolant Temperature (°C)**: Related thermal condition

## Tuning Notes

**Stock Behavior:** Stock activation only enables compensation during hot operating conditions - high oil temp plus warm intake.

**Purpose of Hot-Condition Compensation:**
At high temperatures:
- Fuel atomization changes
- Combustion characteristics differ
- SOI adjustment may optimize for these conditions

**Common Modifications:**
- Generally left at stock unless addressing specific hot-operation issues
- Understanding when compensation activates helps interpret fueling behavior

## Warnings

⚠️ **Temperature-Dependent**: This only activates under specific thermal conditions. Changes won't affect normal-temp operation.

**Safe Practices:**
- Monitor temperatures to understand when activation occurs
- Test any changes under hot operating conditions

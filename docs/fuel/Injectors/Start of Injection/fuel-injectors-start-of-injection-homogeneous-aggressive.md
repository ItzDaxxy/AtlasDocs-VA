# Fuel - Injectors - Start of Injection - Homogeneous (Aggressive)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Injectors - Start of Injection - Homogeneous (Aggressive) - 2017 - RogueWRX.csv` |

## Description

This table defines the Start of Injection (SOI) timing for homogeneous combustion mode under "aggressive" conditions, indexed by calculated load and RPM. This alternate timing table is used during specific operating conditions that warrant different injection timing strategy.

**Purpose:**
- Provides alternate SOI timing for aggressive operating conditions
- May be used during high-performance or transient conditions
- Allows ECU to switch timing strategies based on operating state

**Value Interpretation:**
- Values in crankshaft degrees
- Generally similar range to base homogeneous table (260-330°)
- "Aggressive" may indicate earlier timing for faster mixture preparation
- Or later timing for specific conditions

**When Used:**
The ECU may select this table during:
- Aggressive throttle inputs
- High-load operation
- Sport mode (if applicable)
- Specific temperature or fuel conditions

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.2588 to 2.0704
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
       RPM |     0.2588 |     0.5176 |     0.7764 |     1.0352 |     1.2940 |     1.5528 |     1.8116 |     2.0704 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   260.0000 |
 1200.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   260.0000 |
 1600.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |
 2000.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   270.0000 |   290.0000 |
 2400.0000 |   270.0000 |   280.0000 |   290.0000 |   290.0000 |   290.0000 |   290.0000 |   290.0000 |   290.0000 |
 2800.0000 |   290.0000 |   290.0000 |   290.0000 |   300.0000 |   310.0000 |   310.0000 |   310.0000 |   300.0000 |
 3200.0000 |   290.0000 |   290.0000 |   290.0000 |   300.0000 |   310.0000 |   310.0000 |   310.0000 |   310.0000 |
 3600.0000 |   290.0000 |   290.0000 |   290.0000 |   300.0000 |   310.0000 |   320.0000 |   330.0000 |   310.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Selection:**
ECU selects between base and aggressive SOI tables based on operating conditions. The exact selection logic is determined by other calibration parameters.

**Comparison to Base Table:**
This table shows generally consistent values (270°) across low loads, with progression to higher values (up to 330°) at high loads. The "aggressive" nature may refer to:
- More consistent timing for performance
- Higher values at high load for more mixing time
- Optimized for transient response

**Update Rate:** Calculated every engine cycle when aggressive mode is active.

## Related Tables

- **[Fuel - Injectors - Start of Injection - Homogeneous](./fuel-injectors-start-of-injection-homogeneous.md)**: Base SOI timing
- **[Fuel - Injectors - Start of Injection - Cranking](./fuel-injectors-start-of-injection-cranking.md)**: Cranking SOI timing
- **[Fuel - Injectors - Start of Injection - Compensation](./fuel-injectors-start-of-injection-compensation-compensation-homogeneous.md)**: SOI compensation

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Injector Timing (deg)**: Actual commanded timing
- **Throttle Position (%)**: May correlate with aggressive mode selection

## Tuning Notes

**Stock Behavior:** Stock aggressive timing provides performance-oriented SOI calibration while maintaining safe combustion characteristics.

**Common Modifications:**
- Usually modified in conjunction with base homogeneous table
- May need adjustment with injector upgrades
- Ensure consistency between base and aggressive tables

**Understanding Aggressive vs Base:**
The term "aggressive" in ECU calibration typically means:
- More performance-oriented targets
- May accept slightly higher emissions for performance
- Optimized for throttle response

**Table Pattern Analysis:**
Notice the 270° constant at low loads, progressing to 330° at high load/high RPM. This suggests the aggressive map prioritizes thorough mixing at high loads.

## Warnings

⚠️ **Table Selection Unknown**: Without understanding exactly when this table is active, modifications may have unexpected effects.

⚠️ **Consistency Important**: If modifying SOI, ensure both base and aggressive tables are coordinated.

**Safe Practices:**
- Modify both base and aggressive tables together when changing injectors
- Test across varied driving conditions to experience both table sets
- Monitor for any misfires or combustion irregularities

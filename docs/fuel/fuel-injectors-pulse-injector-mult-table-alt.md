# Fuel - Injectors - Pulse - Injector Mult Table Alt

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Injectors - Pulse - Injector Mult Table Alt - 2018 - LF9C102P.csv` |

## Description

This is an alternate injector pulse width multiplier table, used under different operating conditions than the primary multiplier table. The ECU may switch between tables based on operating mode, temperature, or other conditions.

**Purpose:**
- Provides alternate pressure-based flow compensation
- May be used for different operating modes (cold start, flex fuel, etc.)
- Allows condition-specific injector characterization

**Value Interpretation:**
- Values are multipliers similar to primary table
- Relationship with pressure follows similar pattern
- May have different calibration for specific conditions

**When Used:**
The alternate table may be selected based on:
- Engine temperature (cold operation)
- Fuel type (if flex fuel equipped)
- Specific operating modes defined by ECU logic

## Axes

### X-Axis

- **Parameter**: Fuel - Pressure - Fuel Pressure OBD
- **Unit**: KPA
- **Range**: 300.1194 to 23999.7891
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   300.1194 |   500.1989 |   999.7879 |  2000.1858 |  2999.9736 |  3999.7615 |  5999.9473 |  8000.1328 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using current fuel rail pressure, similar to the primary multiplier table. Table selection logic determines when this alternate table is active.

**Table Selection:**
The ECU chooses between primary and alternate tables based on internal logic. Without detailed calibration documentation, the exact switching conditions may need to be determined through testing.

**Update Rate:** Evaluated every injection event when this table is selected.

## Related Tables

- **[Fuel - Injectors - Pulse - Injector Mult Table](./fuel-injectors-pulse-injector-mult-table.md)**: Primary multiplier table
- **[Fuel - Injectors - Pulse - Injector Offset Table Alt](./fuel-injectors-pulse-injector-offset-table-alt.md)**: Companion offset table
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Final calculated pulse width
- **Coolant Temperature (°C)**: May influence table selection
- **Fuel Mode**: May indicate which table set is active

## Tuning Notes

**Stock Behavior:** Stock calibration uses this table for specific conditions. If modifying injectors, both primary and alternate tables may need adjustment.

**Common Modifications:**
- Usually modified in conjunction with primary table
- May need same or different values depending on purpose
- If unclear when used, can set equal to primary table as starting point

**Determining When Active:**
Log fuel pressure and actual AFR across various conditions (cold start, hot, different loads) to understand when alternate table is selected by comparing expected vs actual fueling.

## Warnings

⚠️ **Understand Selection Logic**: Before modifying, try to determine when this table is active to avoid unexpected AFR changes.

⚠️ **Keep Consistent**: If injector characteristics don't change with conditions, keep both tables aligned.

**Safe Practices:**
- Modify both tables together when changing injectors
- Test across various operating conditions
- Verify AFR accuracy in all scenarios

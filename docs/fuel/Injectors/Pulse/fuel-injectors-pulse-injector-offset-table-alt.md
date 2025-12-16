# Fuel - Injectors - Pulse - Injector Offset Table Alt

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Injectors - Pulse - Injector Offset Table Alt - 2018 - LF9C102P.csv` |

## Description

This is an alternate injector pulse width offset (dead time) table, used under different operating conditions than the primary offset table. Works in conjunction with the alternate multiplier table for complete injector characterization in alternate operating mode.

**Purpose:**
- Provides alternate dead time compensation
- Used during specific operating conditions
- Pairs with Injector Mult Table Alt for complete alternate characterization

**Value Interpretation:**
- Values represent time offset similar to primary table
- May have different calibration for specific conditions
- Typically follows similar pressure relationship as primary table

**When Used:**
Selected by ECU when alternate injector characterization is active, potentially for:
- Cold engine operation
- Specific fuel modes
- Condition-dependent compensation

## Axes

### X-Axis

- **Parameter**: Fuel - Fuel Pressure
- **Unit**: KPA
- **Range**: 300.1200 to 23999.8398
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
       RPM |   300.1200 |   500.2000 |   999.7900 |  2000.1901 |  2999.9800 |  3999.7700 |  5999.9600 |  8000.1504 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using fuel rail pressure, applying this offset when the alternate characterization mode is active. Works with Injector Mult Table Alt for complete fuel calculation.

**Table Selection:**
ECU selects between primary and alternate table sets based on operating conditions. Both multiplier and offset tables switch together.

**Update Rate:** Evaluated every injection event when alternate mode is active.

## Related Tables

- **[Fuel - Injectors - Pulse - Injector Offset Table](./fuel-injectors-pulse-injector-offset-table.md)**: Primary offset table
- **[Fuel - Injectors - Pulse - Injector Mult Table Alt](./fuel-injectors-pulse-injector-mult-table-alt.md)**: Companion alternate multiplier
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Final calculated pulse width
- **Coolant Temperature (°C)**: May influence table selection
- **Engine Runtime**: Cold start duration may trigger alternate tables

## Tuning Notes

**Stock Behavior:** Stock calibration provides alternate dead time compensation for specific conditions.

**Common Modifications:**
- Usually modified together with primary offset table
- If injector dead time doesn't vary with conditions, keep both tables identical
- May need different values if dead time changes with temperature

**Temperature Effects:** Cold engine operation may have different injector characteristics:
- Cold fuel affects atomization
- Injector behavior may vary slightly with temperature
- Alternate tables may compensate for these variations

## Warnings

⚠️ **Paired Tables**: Always modify offset and multiplier alt tables together for consistent characterization.

⚠️ **Testing Required**: Verify fueling accuracy in both primary and alternate modes after modifications.

**Safe Practices:**
- Keep both table sets consistent with injector characteristics
- Test across temperature range
- Monitor AFR during cold start and warm operation

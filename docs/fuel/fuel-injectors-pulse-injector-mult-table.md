# Fuel - Injectors - Pulse - Injector Mult Table

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Injectors - Pulse - Injector Mult Table - 2018 - LF9C102P.csv` |

## Description

This table defines the injector pulse width multiplier as a function of fuel rail pressure. Since fuel flow through an injector varies with the square root of differential pressure, this table compensates for pressure-dependent flow variations to maintain accurate fuel delivery.

**Purpose:**
- Compensates for fuel flow variations at different rail pressures
- Multiplies base pulse width to achieve desired fuel mass
- Enables accurate fueling across the wide HPFP pressure range (3-20+ MPa)

**Value Interpretation:**
- Values are multipliers (typically near 1.0 at reference pressure)
- Higher pressure = lower multiplier (fuel flows faster per unit time)
- Lower pressure = higher multiplier (fuel flows slower)
- Follows approximate square root relationship with pressure

**Pressure-Flow Relationship:**
Injector flow rate ∝ √(differential pressure). As rail pressure increases, fuel flows faster for a given pulse width. This table compensates so the ECU can command fuel mass directly regardless of current pressure.

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

The ECU performs 1D interpolation using current fuel rail pressure:
1. Read current fuel pressure from HPFP sensor
2. Look up multiplier from this table
3. Multiply base injector pulse width by this factor
4. Adjusted pulse width delivers correct fuel mass

**Fuel Calculation Simplified:**
```
Final Pulse Width = Base Pulse Width × Multiplier(pressure) + Offset(pressure)
```

The multiplier table works with the offset table to fully characterize injector behavior across the pressure range.

**Update Rate:** Evaluated every injection event to account for changing rail pressure.

## Related Tables

- **[Fuel - Injectors - Pulse - Injector Offset Table](./fuel-injectors-pulse-injector-offset-table.md)**: Dead time offset compensation
- **[Fuel - Injectors - Pulse - Injector Mult Table Alt](./fuel-injectors-pulse-injector-mult-table-alt.md)**: Alternate multiplier table
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Commanded pressure

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Final calculated pulse width
- **Injector Duty Cycle (%)**: IPW relative to available time
- **Command Fuel Final (λ)**: Target lambda being achieved

## Tuning Notes

**Stock Behavior:** Stock table is calibrated for OEM injectors. Values follow the theoretical square root relationship with empirical corrections for actual injector behavior.

**Common Modifications:**
- **Different Injectors**: Must recalibrate if injector characteristics differ from stock
- Injector flow curves vary by design - use manufacturer data
- Some injectors are more linear than others across pressure range

**Injector Upgrades:** When installing different injectors:
1. Obtain injector characterization data from manufacturer
2. Create new multiplier table based on flow vs pressure data
3. Verify fueling accuracy across pressure range with wideband

**Reference Pressure:** The multiplier is typically 1.0 at some reference pressure. Values above 1.0 at lower pressures, below 1.0 at higher pressures.

## Warnings

⚠️ **Critical for Fuel Accuracy**: Incorrect multipliers cause AFR errors that scale with pressure deviation from reference.

⚠️ **Injector-Specific**: This table is specific to injector model. Different injector designs require different characterization.

⚠️ **Combined with Offset**: Both multiplier and offset tables must be correct for accurate fueling. Errors compound.

**Safe Practices:**
- Use injector manufacturer data when available
- Verify with wideband AFR measurement at various operating pressures
- Log actual vs commanded AFR across load/RPM range

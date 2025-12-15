# Fuel - Injectors - Pulse - Injector Offset Table

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Injectors - Pulse - Injector Offset Table - 2018 - LF9C102P.csv` |

## Description

This table defines the injector pulse width offset (dead time compensation) as a function of fuel rail pressure. Injector dead time is the minimum pulse width required before fuel actually begins flowing, and it varies with differential pressure across the injector.

**Purpose:**
- Compensates for injector dead time (opening delay)
- Adds offset to base pulse width to account for valve opening time
- Varies with pressure (higher pressure = faster valve opening)

**Value Interpretation:**
- Values represent time offset (likely in microseconds or milliseconds)
- Higher pressure = smaller offset (valve opens faster against higher pressure differential)
- Lower pressure = larger offset (valve opens slower)
- Critical for accurate low-pulse-width fueling (idle, light load)

**Injector Dead Time:**
Dead time (also called latency or offset) is the time between energizing the injector coil and actual fuel flow beginning. During this time, the magnetic field builds and the valve opens against fuel pressure. This time varies with:
- Supply voltage (battery voltage)
- Differential pressure across injector
- Injector design characteristics

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

The ECU performs 1D interpolation using current fuel rail pressure:
1. Read current fuel pressure from HPFP sensor
2. Look up offset value from this table
3. Add offset to calculated base pulse width
4. Final pulse width = (Base PW × Multiplier) + Offset

**Complete Fuel Calculation:**
```
Final IPW = (Requested Fuel Mass / Flow Rate) × Multiplier(pressure) + Offset(pressure)
```

The offset accounts for the non-linear opening behavior of the injector.

**Update Rate:** Evaluated every injection event.

## Related Tables

- **[Fuel - Injectors - Pulse - Injector Mult Table](./fuel-injectors-pulse-injector-mult-table.md)**: Pressure-based flow multiplier
- **[Fuel - Injectors - Pulse - Injector Offset Table Alt](./fuel-injectors-pulse-injector-offset-table-alt.md)**: Alternate offset table
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Commanded pressure

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Final calculated pulse width including offset
- **Battery Voltage (V)**: Also affects dead time (separate compensation)
- **Injector Duty Cycle (%)**: IPW relative to available time

## Tuning Notes

**Stock Behavior:** Stock table calibrated for OEM injectors. Dead time varies approximately logarithmically with pressure.

**Common Modifications:**
- **Different Injectors**: Dead time varies significantly between injector designs
- High-impedance vs low-impedance injectors have different characteristics
- Manufacturer data sheets provide dead time vs pressure specifications

**Injector Upgrades:** When installing different injectors:
1. Obtain dead time data from injector manufacturer
2. Create new offset table based on dead time vs pressure curve
3. Most critical at idle and light load where offset is large relative to total pulse width

**Dead Time Importance:**
- At idle (short pulse widths), offset may be 30-50% of total IPW
- At WOT (long pulse widths), offset is smaller percentage
- Incorrect offset causes worst AFR errors at light loads

## Warnings

⚠️ **Idle Quality**: Incorrect dead time causes idle AFR errors. Rich/lean idle is often dead time miscalibration.

⚠️ **Light Load Sensitivity**: Small dead time errors cause large percentage errors at low fuel demands.

⚠️ **Injector-Specific**: Every injector model has unique dead time characteristics. Cannot use generic values.

**Safe Practices:**
- Use injector manufacturer specifications
- Verify idle AFR with wideband
- Test across pressure range to confirm offset accuracy

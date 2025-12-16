# Airflow - Turbo - Boost - Compensation - Boost IAT Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Boost - Compensation - Boost IAT Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts boost target based on Intake Air Temperature (IAT). Hot intake air is less dense and more prone to knock, so this table typically reduces boost targets at higher IAT to protect the engine.

Values are in PERCENT - negative values reduce boost target at hot temperatures, helping prevent knock when intercooler efficiency decreases. This compensation is critical during heat-soak conditions common in traffic or after spirited driving.

## Axes

### X-Axis

- **Parameter**: Boost Control - Wastegate - IAT
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using IAT:

1. **IAT Reading**: ECU reads intake air temperature sensor
2. **Table Lookup**: Interpolates compensation percentage
3. **Target Adjustment**: Base Target × (1 + Compensation%)

**Temperature Compensation:**
- Cold IAT: May add boost (denser air)
- Normal IAT (20-40°C): No compensation (0%)
- Hot IAT (50°C+): Reduce boost for safety

## Related Tables

- **Airflow - Turbo - Boost - Boost Target Main**: Base boost target
- **Airflow - Turbo - Boost - Barometric Compensation**: Altitude adjustment
- **Airflow - Turbo - Wastegate - IAT Compensation**: Wastegate duty adjustment
- **Ignition - IAT Compensation**: Timing adjustment for IAT

## Related Datalog Parameters

- **IAT (°C)**: X-axis input
- **Target Boost**: Result after compensation
- **Actual Boost**: Measured manifold pressure

## Tuning Notes

**Common Modifications:**
- Reduce hot IAT derating with upgraded intercooler
- May increase cold IAT boost addition for denser air
- Coordinate with ignition IAT compensation

**Considerations:**
- Hot air = less dense = higher effective AFR
- Hot air = more knock prone
- Upgraded intercooler allows less conservative values

## Warnings

- Hot IAT dramatically increases knock risk
- Don't reduce hot IAT compensation without intercooler upgrades
- Heat-soak can spike IAT rapidly during traffic/hard driving
- Monitor knock and AFR when adjusting these values
- Consider water-methanol injection for consistent IAT

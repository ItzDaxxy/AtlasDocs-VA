# Airflow - Turbo - Wastegate - Wastegate Barometric Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x10 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate Barometric Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts wastegate duty based on barometric pressure (altitude) and RPM. At higher altitudes, the turbo must work harder to achieve target boost due to lower air density, requiring different wastegate duty cycles.

Values are in PERCENT - negative values reduce wastegate duty at altitude, allowing the wastegate to open more easily. The data shows significant reductions (-20% to -45%) at low barometric pressures (high altitudes) across the RPM range.

This compensation helps maintain consistent boost control behavior regardless of elevation, preventing over-boost at altitude where reduced back-pressure changes wastegate behavior.

## Axes

### X-Axis

- **Parameter**: Boost Control - Barometric Pressure
- **Unit**: PASCAL
- **Range**: 63129.6953 to 99953.7500
- **Points**: 10

### Y-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 3000.0000 to 6100.0000
- **Points**: 9

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM | 63129.6953 | 69705.1484 | 76280.5938 | 82856.0391 | 89431.4922 | 92060.1250 | 94692.6172 | 96006.9375 |
--------------------------------------------------------------------------------------------------------------------
 3000.0000 |   -20.3125 |   -14.8438 |   -10.1563 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4000.0000 |   -29.6875 |   -25.0000 |   -20.3125 |   -14.8438 |    -7.8125 |     0.0000 |     0.0000 |     0.0000 |
 4800.0000 |   -35.1563 |   -29.6875 |   -25.0000 |   -18.7500 |   -11.7188 |     0.0000 |     0.0000 |     0.0000 |
 5200.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |    -7.0313 |     0.0000 |     0.0000 |
 5600.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 5800.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 5900.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
 6000.0000 |   -45.3125 |   -39.8438 |   -35.1563 |   -29.6875 |   -20.3125 |   -11.7188 |    -4.6875 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using barometric pressure and RPM:

1. **Baro/RPM Reading**: ECU monitors both values
2. **Table Lookup**: 2D interpolation for duty compensation
3. **Duty Adjustment**: Applied as multiplier to wastegate duty

**Compensation Logic:**
- Sea level (~100 kPa): 0% adjustment
- High altitude (~63 kPa): -20% to -45% adjustment
- Reduces duty to prevent over-boost at altitude

## Related Tables

- **Airflow - Turbo - Wastegate - Duty Initial**: Base duty modified by this
- **Airflow - Turbo - Wastegate - IAT Compensation**: Temperature adjustment
- **Airflow - Turbo - Boost - Barometric Compensation**: Target adjustment

## Related Datalog Parameters

- **Barometric Pressure (Pa/kPa)**: X-axis input
- **Engine RPM**: Y-axis input
- **Wastegate Duty (%)**: Final commanded duty
- **Altitude (calculated)**: Derived from barometric

## Tuning Notes

**Common Modifications:**
- May need adjustment for different turbo characteristics
- Altitude-frequent drivers may need fine-tuning
- Coordinate with boost barometric compensation

**Considerations:**
- Wastegate behavior changes significantly with altitude
- Less back-pressure at altitude = wastegate opens easier
- Compensation prevents over-boost in mountains

## Warnings

- Removing compensation can cause over-boost at altitude
- Test at various altitudes before modifying
- Mountain passes can quickly change conditions
- Over-boost at altitude especially dangerous

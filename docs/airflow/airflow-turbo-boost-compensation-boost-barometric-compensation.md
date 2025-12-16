# Airflow - Turbo - Boost - Compensation - Boost Barometric Compensation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x8 |
| **Data Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - Boost - Compensation - Boost Barometric Compensation - 2018 - LF9C102P.csv` |

## Description

Adjusts boost target based on barometric pressure (altitude) and engine RPM. At higher altitudes, reduced atmospheric pressure affects turbo efficiency and knock threshold, requiring boost target adjustments.

Values are in PERCENT - negative values reduce boost target, positive values increase it. The data shows significant reductions at lower barometric pressures (higher altitudes), especially at mid-to-high RPM where the turbo generates the most boost.

**Altitude Effects:**
- Lower air density reduces turbo efficiency
- Less oxygen per boost unit requires target reduction
- Knock threshold changes with altitude
- Stock table reduces boost up to ~40% at high altitude

## Axes

### X-Axis

- **Parameter**: Boost Control - Barometric Pressure
- **Unit**: PASCAL
- **Range**: 63129.6953 to 96006.9375
- **Points**: 8

### Y-Axis

- **Parameter**: Boost Control - Wastegate - RPM
- **Unit**: RPM
- **Range**: 1600.0000 to 8000.0000
- **Points**: 9

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM | 63129.6953 | 69705.1484 | 76280.5938 | 82856.0391 | 89431.4922 | 92060.1250 | 94692.6172 | 96006.9375 |
--------------------------------------------------------------------------------------------------------------------
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 4000.0000 |   -11.7188 |    -9.3750 |    -7.0313 |    -4.6875 |    -2.3438 |     0.0000 |     0.0000 |     0.0000 |
 4800.0000 |   -28.9063 |   -24.2188 |   -18.7500 |   -13.2813 |    -6.2500 |    -3.1250 |     0.0000 |     0.0000 |
 5600.0000 |   -39.8438 |   -34.3750 |   -27.3438 |   -18.7500 |   -10.9375 |    -7.8125 |    -3.1250 |     0.0000 |
 6400.0000 |   -24.2188 |   -17.1875 |   -10.9375 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 7200.0000 |   -24.2188 |   -17.1875 |   -10.9375 |    -4.6875 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using barometric pressure and RPM:

1. **Baro Reading**: ECU reads atmospheric pressure
2. **RPM Reading**: ECU monitors engine RPM
3. **Table Lookup**: 2D interpolation for compensation percentage
4. **Target Adjustment**: Base Target × (1 + Compensation%)

**Compensation Application:**
- 96000 Pa (~sea level): 0% compensation
- 63000 Pa (~12,000 ft): -25% to -40% compensation
- Applied to boost target before wastegate control

## Related Tables

- **Airflow - Turbo - Boost - Boost Target Main**: Base boost target
- **Airflow - Turbo - Boost - Boost IAT Compensation**: Temperature adjustment
- **Airflow - Turbo - Wastegate - Barometric Compensation**: Wastegate duty adjustment

## Related Datalog Parameters

- **Barometric Pressure (Pa/kPa)**: X-axis input
- **Engine RPM**: Y-axis input
- **Target Boost**: Result after compensation
- **Altitude (calculated)**: Derived from barometric

## Tuning Notes

**Common Modifications:**
- Reduce compensation for less aggressive altitude derating
- May need adjustment for different turbo characteristics
- Consider E85's knock resistance at altitude

**Considerations:**
- Compensation protects engine at altitude
- Higher altitude = less dense air = less cooling = more knock prone
- Turbo must work harder for same boost at altitude

## Warnings

- Removing altitude compensation risks knock at elevation
- Test at various altitudes before reducing compensation
- Mountain driving can quickly change conditions
- Monitor knock and AFR when adjusting these values

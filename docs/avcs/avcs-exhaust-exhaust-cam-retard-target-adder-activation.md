# AVCS - Exhaust - Exhaust Cam Retard Target Adder Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `AVCS - Exhaust - Exhaust Cam Retard Target Adder Activation - 2018 - LF9C102P.csv` |

## Description

Controls the activation scaling of exhaust cam retard target compensation based on coolant temperature. This 1D table determines how much of the exhaust cam compensation tables should be applied at various engine temperatures.

Values are in PERCENT - at 100%, full compensation is applied; at lower values, compensation is scaled down. This allows the ECU to gradually enable or disable cam timing compensation as the engine warms up or cools down.

This table is critical for cold start behavior where different cam timing may be needed until the engine reaches operating temperature.

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
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

The ECU performs 1D interpolation using coolant temperature:

1. **Temperature Reading**: ECU reads coolant temperature
2. **Table Lookup**: Interpolate activation percentage
3. **Scaling**: Compensation × Activation% = Applied Compensation
4. **Result**: Temperature-modulated cam timing compensation

**Activation Logic:**
```
Applied_Compensation = Base_Compensation × (Activation% / 100)
```

**Temperature-Based Control:**
- Cold engine: May reduce compensation for warm-up
- Operating temp: Full compensation applied (100%)
- Allows smooth transition as engine warms

## Related Tables

- **AVCS - Exhaust - Compensation Tables**: Scaled by this table
- **AVCS - Exhaust - Exhaust Cam Target**: Base target
- **Engine - Coolant Temperature**: Input source

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **AVCS Exhaust Target (°)**: Final commanded position
- **AVCS Exhaust Compensation Active**: Activation status

## Tuning Notes

**Temperature Activation:**
- Determines warm-up cam timing behavior
- May ramp from reduced to full compensation
- Stock values optimize emissions and driveability

**Cold Start Considerations:**
- Cold engine may need different overlap strategy
- Gradual activation prevents harsh transitions
- Affects warm-up emissions and idle stability

## Warnings

- Changes affect cold start behavior
- Emissions during warm-up depend on this table
- Idle quality during warm-up affected
- Test across temperature range
- Don't disable without understanding effects

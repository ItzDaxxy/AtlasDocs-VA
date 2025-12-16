# Sensors - Oil Temperature

## Overview

| Property | Value |
|----------|-------|
| **Category** | Sensors |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x32 |
| **Data Unit** | CELSIUS |
| **Source File** | `Sensors - Oil Temperature - 2017 - RogueWRX.csv` |

## Description

Converts oil temperature sensor voltage to temperature in Celsius. The oil temperature sensor uses a negative temperature coefficient (NTC) thermistor that changes resistance based on temperature - as oil temperature increases, resistance decreases, lowering the voltage signal.

This conversion table allows the ECU to translate the analog voltage signal into an accurate temperature reading. Oil temperature is critical for engine protection, lubrication effectiveness, and may influence fuel/ignition strategies during warm-up.

The FA20DIT uses oil temperature for:
- Oil cooler fan/thermostat control
- Engine protection (high temp warning/limp mode)
- Cold start enrichment refinement
- Optimal operating temperature verification

## Axes

### X-Axis

- **Parameter**: Developer - Sensors - Voltage
- **Unit**: VOLTS
- **Range**: 4.9808 to 0.0000
- **Points**: 32

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: CELSIUS
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     4.9808 |     4.4925 |     3.7503 |     3.3596 |     3.0862 |     2.8908 |     2.7346 |     2.5978 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using sensor voltage:

1. **Voltage Reading**: ECU reads oil temperature sensor voltage (0-5V range)
2. **Table Lookup**: Interpolates between voltage breakpoints
3. **Temperature Output**: Returns oil temperature in Celsius
4. **Usage**: Temperature used for protection logic and operating decisions

**Typical Voltage-Temperature Relationship (NTC):**
- High voltage (~5V) = Cold oil (high resistance)
- Low voltage (~0V) = Hot oil (low resistance)
- Normal operating range: ~90-110°C

## Related Tables

- **Sensors - Coolant Temperature**: Similar conversion for coolant
- **Engine Protection - Oil Temperature Limits**: High temp cutoff values

## Related Datalog Parameters

- **Oil Temperature (°C)**: Converted temperature output
- **Oil Temperature Sensor Voltage (V)**: Raw sensor input
- **Coolant Temperature (°C)**: Often compared for diagnostic purposes

## Tuning Notes

**When to Modify:**
- Aftermarket oil temperature sensor with different resistance curve
- Sensor relocation requiring calibration adjustment
- Diagnostic purposes when sensor readings seem incorrect

**Considerations:**
- Stock calibration matches OEM sensor specification
- Aftermarket sensors may have different NTC characteristics
- Verify calibration with known reference thermometer

## Warnings

- Incorrect calibration causes false temperature readings
- False low readings may allow operation with overheating oil
- False high readings may trigger unnecessary protection modes
- Oil temperature is critical for engine longevity - verify accuracy
- Never ignore high oil temperature warnings regardless of calibration

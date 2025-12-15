# Sensors - Coolant Temperature

## Overview

| Property | Value |
|----------|-------|
| **Category** | Sensors |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x32 |
| **Data Unit** | CELSIUS |
| **Source File** | `Sensors - Coolant Temperature - 2017 - RogueWRX.csv` |

## Description

Voltage-to-temperature conversion table for the engine coolant temperature (ECT) sensor. This table translates the analog voltage signal (0-5V) from the thermistor-based sensor into temperature readings in Celsius.

The coolant temperature sensor is the most critical temperature input for engine management, affecting:
- Cold-start and warm-up fuel enrichment
- Ignition timing compensation
- Idle speed control (fast idle when cold)
- Cooling fan activation
- Closed-loop fuel trim enablement
- Engine protection limits

The table uses voltage as the X-axis (high voltage = cold, low voltage = hot) because thermistor resistance decreases as temperature increases, creating an inverse relationship between voltage and temperature.

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

The ECU performs 1D interpolation using sensor voltage to determine temperature:

1. **Voltage Reading**: ECU reads coolant temp sensor voltage via ADC
2. **Table Lookup**: Finds voltage in X-axis, interpolates for temperature
3. **Temperature Output**: Result used throughout engine management

Voltage-Temperature relationship (NTC thermistor):
- ~5V = Very cold (-40°C range) - high resistance
- ~2.5V = Moderate (~25°C)
- ~0.5V = Very hot (100°C+) - low resistance

The ECU reads this sensor continuously and uses the temperature for dozens of calculations.

## Related Tables

- **Sensors - Oil Temperature**: Complementary temperature monitoring
- **Fuel - Cranking Base Pulse Width**: Uses ECT for cold-start fueling
- **Fuel - Warm-up Enrichment**: Primary input for cold enrichment
- **Ignition - Timing Compensation**: Adjusts timing based on temperature
- **Engine - Idle Speed Target A-J**: Target RPM varies with temperature
- **Engine - Radiator Fan Thresholds**: Fan activation based on temp

## Related Datalog Parameters

- **Coolant Temperature (°C/°F)**: The output of this table
- **ECT Sensor Voltage (V)**: Raw input to this table
- **Oil Temperature**: Complementary temperature reading
- **Cooling Fan Status**: Activated based on temp
- **Fuel Trim (Short/Long Term)**: Affected by temperature

## Tuning Notes

**Factory Setting**: Calibrated for OEM coolant temperature sensor thermistor

**When to Modify:**
- Installing aftermarket ECT sensor with different resistance curve
- Non-OEM replacement sensor with different characteristics
- Correcting systematic temperature reading errors

**Modification Procedure:**
1. Identify new sensor's resistance-to-temperature curve from specs
2. Calculate voltage at each temperature using ECU pull-up resistor (~2.5kΩ typical)
3. Update table values to match new sensor
4. Verify with infrared thermometer or mechanical gauge
5. Test across full temperature range (cold start to full operating)

## Warnings

- **CRITICAL**: Most important sensor for engine protection and operation
- Incorrect calibration causes severe drivability and potential engine damage
- Reading too hot prevents cold-start enrichment (rough/no start when cold)
- Reading too cold causes constant over-fueling, fouled plugs, catalyst damage
- False low temps prevent cooling fan operation (overheating risk)
- False high temps cause unnecessary fan operation and false warnings
- Affects ignition timing - incorrect readings can cause knock
- Always verify with mechanical thermometer after modification
- May trigger P0115/P0116/P0117/P0118 DTCs if readings are implausible

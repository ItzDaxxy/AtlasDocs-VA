# Sensors - Mass Airflow

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x64 |
| **Data Unit** | G_PER_SEC |
| **Source File** | `Sensors - Mass Airflow - 2017 - RogueWRX.csv` |

## Description

The Mass Airflow (MAF) sensor calibration table that converts the MAF sensor's output voltage (0-5V) to actual airflow in grams per second (g/s). This is the fundamental table that tells the ECU how much air is entering the engine.

The MAF sensor uses a heated wire or film element - as air flows past, it cools the element, requiring more current to maintain temperature. The sensor outputs a voltage proportional to airflow. This table defines the voltage-to-airflow relationship.

This calibration is specific to the MAF sensor used. Different MAF sensors (stock, larger aftermarket) have different voltage curves and require different calibration tables.

## Axes

### X-Axis

- **Parameter**: Air Flow Voltage
- **Unit**: VOLTS
- **Range**: 0.0000 to 5.0000
- **Points**: 64

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: G_PER_SEC
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.0800 |     0.1600 |     0.2400 |     0.3200 |     0.4000 |     0.4800 |     0.5600 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation to convert MAF voltage to airflow:

1. **Voltage Reading**: ECU reads MAF sensor voltage (0-5V)
2. **Table Lookup**: Interpolate voltage to airflow (g/s)
3. **Output**: Mass airflow used for all engine calculations

**MAF Sensor Characteristics:**
- 0V: No/minimal airflow
- ~5V: Maximum sensor range (varies by sensor)
- Non-linear relationship: voltage increases with airflow
- Hot-wire or hot-film element technology

**Typical Flow Ranges:**
- Idle: ~3-8 g/s
- Cruise: ~15-30 g/s
- Full boost: ~200-300+ g/s (stock turbo)

## Related Tables

- **Airflow - MAF - VE Correction**: Applies VE factor to MAF reading
- **Airflow - Idle - Mass Airflow Minimum**: Minimum enforced airflow
- **Fuel - Injector Scaling**: Fuel calculation from airflow
- **Ignition - Primary Tables**: Timing from calculated load

## Related Datalog Parameters

- **MAF Voltage (V)**: X-axis input (raw sensor)
- **MAF (g/s)**: Output from this table
- **Calculated Load (%)**: Derived from airflow
- **AFR**: Verification of airflow accuracy

## Tuning Notes

**Common Modifications:**
- Required for MAF sensor upgrades
- Larger MAF sensor = different calibration curve
- Manufacturer typically provides calibration data

**MAF Upgrade Considerations:**
- Larger MAF housing reduces velocity at same flow
- Different sensor element = different characteristics
- Must recalibrate to maintain accurate fueling

**Calibration Process:**
1. Obtain new MAF sensor calibration data
2. Update table with new voltage-to-g/s values
3. Verify with fuel trims across operating range
4. Fine-tune VE tables if needed

## Warnings

- Incorrect MAF calibration causes global fueling errors
- Lean conditions at high flow extremely dangerous
- Always verify AFR after MAF calibration changes
- MAF sensor contamination can skew readings
- Aftermarket intakes may require MAF recalibration

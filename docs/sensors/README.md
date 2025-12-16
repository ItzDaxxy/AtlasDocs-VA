# Sensors

Sensor scaling and calibration tables.

## Overview

Sensor tables define:
- Voltage-to-value conversion curves
- Sensor linearization
- Compensation factors
- Validation ranges

## Common Sensors

- **MAF** (Mass Airflow)
- **MAP** (Manifold Absolute Pressure)
- **IAT** (Intake Air Temperature)
- **ECT** (Engine Coolant Temperature)
- **TPS** (Throttle Position Sensor)
- **APP** (Accelerator Pedal Position)
- **O2/AFR** (Oxygen/Air-Fuel Ratio)
- **Knock** sensors

## Subcategories

### Mass Airflow (MAF)
Converts MAF sensor voltage to airflow (g/s):
- **MAF Scaling**: Primary voltage-to-airflow conversion curve
- **MAF Temperature Compensation**: IAT-based corrections
- **MAF VE Corrections**: Volumetric efficiency adjustments

### Temperature Sensors
Converts resistance/voltage to temperature:
- **IAT Scaling**: Intake air temperature conversion
- **ECT Scaling**: Engine coolant temperature conversion
- **Oil Temperature**: Oil temp sensor calibration

### Pressure Sensors
MAP and barometric pressure calibration:
- **MAP Scaling**: Manifold pressure conversion
- **Barometric Scaling**: Atmospheric pressure calibration
- **Fuel Pressure**: Fuel rail pressure sensor

### Position Sensors
Throttle and pedal position calibration:
- **TPS Scaling**: Throttle position sensor conversion
- **APP Scaling**: Accelerator pedal position conversion

### Oxygen/AFR Sensors
Exhaust gas sensor calibration:
- **Front O2 Scaling**: Primary oxygen sensor
- **Rear O2 Scaling**: Downstream catalyst monitor
- **Wideband AFR**: Air-fuel ratio sensor scaling

### Knock Sensors
Knock detection sensor calibration:
- **Knock Sensor Scaling**: Voltage-to-knock-intensity conversion
- **Knock Frequency Filters**: Frequency band selection

## Key Tables

| Table Name | Type | Description |
|------------|------|-------------|
| MAF Scaling | 2D Curve | Voltage to airflow (g/s) |
| IAT Conversion | 2D Curve | Voltage to temperature (°C) |
| ECT Conversion | 2D Curve | Voltage to temperature (°C) |
| MAP Scaling | 2D Curve | Voltage to pressure (kPa) |
| TPS Scaling | Linear | Voltage to position (%) |
| Knock Sensor Gain | Scalar | Sensitivity adjustment |

## Related Systems

- **All**: Sensors feed data to every ECU function
- **Fuel**: MAF and O2 sensors critical for fueling
- **Ignition**: Knock sensors influence timing
- **Airflow**: MAF and MAP for load calculation

## Technical Details

### MAF Sensor Operation
The hot-wire MAF sensor measures intake airflow:
1. **Heated Element**: Maintains constant temperature above IAT
2. **Cooling Effect**: Airflow cools the element
3. **Current Measurement**: More current needed to maintain temp = more airflow
4. **Voltage Output**: 0-5V signal proportional to airflow

### Sensor Validation
ECU continuously monitors sensors for faults:
- Out-of-range voltage triggers DTC
- Implausible readings (MAF vs MAP disagreement)
- Sensor response time validation
- Circuit short/open detection

## Notes

- Sensor scaling must match physical hardware
- Aftermarket sensors may require recalibration
- Critical for accurate load calculation
- MAF scaling is the most commonly modified sensor table
- Incorrect scaling causes fueling and load calculation errors
- Always verify sensor calibration after hardware changes

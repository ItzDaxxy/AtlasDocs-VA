# Engine - Displacement

## Overview

| Property | Value |
|----------|-------|
| **Category** | Engine |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | L |
| **Source File** | `Engine - Displacement - 2018 - LF9C102P.csv` |

## Value

**2.0000 L**

## Description

Defines the engine displacement used by the ECU for various fuel and ignition calculations. This is a fundamental parameter that affects volumetric efficiency calculations, air-fuel ratio computations, and injector pulse width scaling.

For the FA20DIT (2015-2021 VA WRX), the displacement is 1998cc, derived from:
- Bore: 86.0mm
- Stroke: 86.0mm
- Cylinders: 4
- Configuration: Horizontally opposed (boxer)

The ECU uses this value to:
- Calculate theoretical airflow based on engine speed and manifold pressure
- Determine base injector pulse width requirements
- Scale volumetric efficiency tables
- Calculate fuel delivery for target air-fuel ratios

## Related Tables

- **Fuel - Injector Flow Rate**: Works with displacement to calculate injection timing
- **Fuel - Base Fuel Map**: Scaled based on displacement calculations
- **Airflow - MAF Calibration**: Cross-referenced for airflow validation

## Related Datalog Parameters

- **Engine Speed (RPM)**: Used with displacement for airflow calculations
- **Calculated Load (g/rev)**: Derived from displacement-based volumetric efficiency
- **Manifold Absolute Pressure**: Combined with displacement for theoretical airflow

## Tuning Notes

**WARNING: DO NOT MODIFY** unless the engine has been physically modified (stroker kit, etc.).

This is a hardware constant. Incorrect displacement values will cause:
- Severely incorrect fuel delivery calculations
- Improper ignition timing advance
- MAF sensor scaling errors
- Potential engine damage

Only modify if:
1. A stroker kit has been installed (changing stroke dimension)
2. Bore has been increased through machining
3. Engine has been swapped to different displacement

For stock engines or standard bolt-on modifications, this value must remain at 2.0000 L.

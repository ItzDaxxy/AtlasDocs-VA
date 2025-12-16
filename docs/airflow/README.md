# Airflow

Mass airflow and volumetric efficiency calculations.

## Overview

Airflow tables define how the ECU calculates air mass entering the engine, which is fundamental to:
- Fuel injection calculations
- Load determination
- Boost control targets

## Subcategories

### Turbo - Boost
Boost target and limit tables defining desired manifold pressure across operating conditions.
- **Boost Target Main**: Primary boost target by RPM and load
- **Boost Limit**: Maximum allowed boost (safety ceiling)
- **Boost Compensation**: Barometric and IAT adjustments to target

### Turbo - Wastegate
Wastegate solenoid control for boost regulation.
- **Duty Initial**: Feedforward wastegate duty
- **Duty Maximum**: Upper limit on wastegate duty
- **Compensation Tables**: Barometric and IAT adjustments
- **PWM Frequency**: Solenoid control frequency (10 Hz stock)

### Turbo - PI Control
Closed-loop boost control using Proportional-Integral controller.
- **Proportional**: Instantaneous error correction
- **Integral Positive/Negative**: Accumulated error correction
- **IAT Compensation**: Temperature adjustments to PI gains
- **Integral Limits**: Anti-windup bounds (+10%/-90%)

### MAF - Volumetric Efficiency
Airflow correction based on engine breathing efficiency.
- **VE Correction B**: General VE table
- **VE Correction TGV Open/Closed**: TGV-specific VE tables

### Idle - Mass Airflow
Minimum airflow constraints for idle stability.

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Boost Target Main | 3D Map | Primary boost target by RPM/load |
| Boost Limit Base | 3D Map | Maximum allowed boost pressure |
| Wastegate Duty Initial | 3D Map | Feedforward wastegate duty |
| Wastegate Duty Maximum | 3D Map | Maximum wastegate duty limit |
| PI Control Proportional | 1D | P-term gain by boost error |
| PI Control Integral Positive | 1D | I-term for under-boost |
| PI Control Integral Negative | 1D | I-term for over-boost |
| MAF VE Correction | 3D Map | Volumetric efficiency by MAP/RPM |
| Sensors - Mass Airflow | 1D | MAF voltage to g/s calibration |

## Related Systems

- **Fuel**: Directly determines injector pulse width
- **Sensors**: MAF sensor scaling
- **Engine**: Load calculations

## Notes

- FA20DIT uses both MAF and MAP for load calculation
- Speed density fallback available in some configurations

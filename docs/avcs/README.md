# AVCS (Active Valve Control System)

Variable valve timing control tables for intake and exhaust camshaft timing.

## Overview

AVCS (Subaru's Active Valve Control System) is an oil pressure-actuated variable valve timing system that controls camshaft phasing to optimize:
- Low-end torque through intake cam advance
- High-RPM power via optimized overlap
- Fuel efficiency at cruise loads
- Emissions through precise valve overlap control

The VA WRX uses dual AVCS controlling both intake and exhaust camshafts independently based on engine operating conditions.

## Subcategories

### Intake Cam Control
Tables controlling intake camshaft advance timing (0-50° range):
- **Base Target Tables**: Primary intake cam targets by RPM and load
- **Barometric Compensation**: Altitude adjustment multipliers for intake cam
- **TGV State Variants**: Separate targets for TGV open/closed conditions
- **Aggressive Mode Tables**: Performance-oriented intake timing

### Exhaust Cam Control
Tables controlling exhaust camshaft retard timing (0-30° range):
- **Base Target Tables**: Primary exhaust cam targets by RPM and load
- **Retard Target Adders**: Additional retard under specific conditions
- **Barometric Compensation**: Altitude adjustment multipliers for exhaust cam
- **TGV State Variants**: Separate targets for TGV open/closed conditions
- **Aggressive Mode Tables**: Performance-oriented exhaust timing

### Ignition - AVCS Variants
Ignition timing tables with AVCS-specific calibration:
- **AVCS Enabled Tables**: Timing optimized for variable cam operation
- **AVCS Disabled Tables**: Timing for fixed cam (cold start/fault) conditions
- **TGV State Variants**: Separate maps for TGV open/closed

### Fuel - AVCS Variants
Fuel target tables with AVCS-specific calibration:
- **AVCS Enabled Tables**: Fueling optimized for variable cam operation
- **AVCS Disabled Tables**: Fueling for fixed cam conditions
- **Low DAM Protection**: Richer targets when knock is detected
- **TGV State Variants**: Separate maps for TGV open/closed

## Key Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Intake Cam Target (TGV Open) | 3D Map | Base intake cam advance targets |
| Intake Cam Target (TGV Closed) | 3D Map | Intake targets with TGVs restricted |
| Exhaust Cam Target (TGV Open) | 3D Map | Base exhaust cam retard targets |
| Exhaust Cam Retard Target Adder | 3D Map | Additional exhaust retard conditions |
| Barometric Multiplier - High | 2D Map | Sea-level adjustment multiplier |
| Barometric Multiplier - Low | 2D Map | High-altitude adjustment multiplier |
| Ignition - Primary - AVCS Enabled | 3D Map | Timing with AVCS active |
| Ignition - Primary - AVCS Disabled | 3D Map | Timing with fixed cams |
| Fuel - Open Loop - AVCS Enabled | 3D Map | AFR targets with AVCS active |
| Low DAM Threshold | Scalar | DAM level triggering protective fueling |

## Related Systems

- **Ignition**: All primary timing maps have AVCS-enabled/disabled variants
- **Fuel**: Open-loop fuel tables vary based on AVCS state
- **Airflow**: TGV position determines which AVCS tables are used
- **Engine**: Oil pressure and temperature affect AVCS activation

## Technical Details

### Intake Cam Operation
- **Range**: 0° (retarded) to 50° (advanced)
- **Default Position**: 0° advance (spring-loaded)
- **Actuation**: Oil pressure via duty-cycled solenoid
- **Benefits**: Advance improves low-end torque, reduces pumping losses

### Exhaust Cam Operation
- **Range**: 0° (no retard) to 30° (retarded)
- **Default Position**: 0° retard (spring-loaded)
- **Actuation**: Oil pressure via duty-cycled solenoid
- **Benefits**: Retard increases overlap for scavenging, improves VE

### AVCS Activation Requirements
- Sufficient oil pressure (~30+ PSI)
- Coolant temperature above threshold
- Engine running (not cranking)
- No AVCS fault codes present

## Notes

- VA WRX uses dual AVCS (intake and exhaust independently controlled)
- Intake cam advance range: 0-50°
- Exhaust cam retard range: 0-30°
- AVCS disabled during cold start until oil pressure established
- TGV state affects which AVCS tables are active
- Barometric compensation adjusts for altitude (high vs low pressure)
- Aggressive tables may be enabled by specific ECU modes

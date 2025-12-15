# Fuel

Fuel injection and delivery tables.

## Overview

Fuel tables control:
- Injector pulse width calculations
- Air/fuel ratio targets
- Open/closed loop operation
- Fuel enrichment strategies
- Direct injection timing (FA20DIT)

## Subcategories

- **[Closed Loop Target](closed-loop-target/)**: AFR targets during closed-loop operation
- **[Open Loop Target](open-loop-target/)**: AFR targets during open-loop (WOT) operation
- **[CL/OL Transition](cl-ol-transition/)**: Thresholds for switching between modes
- **[HPFP](hpfp/)**: High-pressure fuel pump timing and control
- **[Injector](injector/)**: Injector characterization and dead times
- **[Lean Limit](lean-limit/)**: Maximum lean AFR boundaries

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Closed Loop Target | 2D | Lambda target during closed-loop (feedback) |
| Open Loop Target Base | 2D | Lambda target during WOT/open-loop |
| CL→OL Transition Load | 2D | Load threshold to enter open-loop |
| CL→OL Transition Throttle | 2D | Throttle threshold to enter open-loop |
| HPFP SOI Timing | 2D | Start of injection timing (degrees) |
| Injector Dead Time | 2D | Injector latency vs battery voltage |
| Primary Injector Scaling | Constant | Flow rate calibration for primary injectors |

## Key Concepts

### Lambda vs AFR
- **Lambda (λ)**: Normalized air-fuel ratio (1.0 = stoichiometric)
- **Stoichiometric**: 14.7:1 for gasoline, 9.76:1 for E85
- Lambda 0.80 = rich (11.76:1 gasoline), Lambda 1.10 = lean (16.17:1)

### Closed-Loop vs Open-Loop
- **Closed-Loop**: ECU uses O2 sensor feedback to trim fuel
- **Open-Loop**: ECU runs from base tables only (WOT, cold start)
- Transition occurs at specific load/throttle thresholds

### FA20DIT Direct Injection
- High-pressure fuel system (up to 200+ bar)
- HPFP driven by intake camshaft lobe
- Injection timing affects combustion and emissions
- Multiple injection events per cycle possible

## Related Systems

- **Airflow**: Determines base fuel requirement
- **Sensors**: O2 sensor feedback
- **Engine**: Load and RPM inputs
- **Ignition**: AFR affects timing safety

## Notes

- FA20DIT uses both port and direct injection
- Closed loop uses wideband O2 feedback
- Stoich for pump gas: 14.7:1 AFR (lambda 1.0)

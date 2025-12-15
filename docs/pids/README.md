# PIDs (Parameter IDs)

OBD-II and proprietary parameter definitions.

## Overview

PIDs define:
- Datalog parameter addresses
- Scaling and conversion formulas
- Units and display formats
- Custom parameter definitions

## Subcategories

- **Standard OBD-II**: Universal diagnostic parameters
- **Subaru Extended**: Manufacturer-specific parameters
- **Custom PIDs**: User-defined parameter calculations

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| PID Address | Constant | Memory address for parameter read |
| PID Scaling | Constant | Conversion formula (raw to engineering units) |
| PID Units | Constant | Display units (°C, psi, %, etc.) |
| PID Sample Rate | Constant | Polling frequency in Hz |

## Key Concepts

### PID Structure
Each Parameter ID includes:
- **Address**: ECU memory location (RAM address)
- **Length**: Data size (1, 2, or 4 bytes)
- **Scaling**: Formula to convert raw bytes to real values
- **Units**: Engineering units for display

### Common VA WRX PIDs

| Parameter | Address | Description |
|-----------|---------|-------------|
| Coolant Temp | Standard | Engine coolant temperature |
| IAT | Standard | Intake air temperature |
| MAF | Standard | Mass airflow (g/s) |
| Boost | Extended | Manifold pressure (psi gauge) |
| AF Learning | Extended | Fuel trim correction (%) |
| DAM | Extended | Dynamic Advance Multiplier (0-1) |
| Fine Knock Learn | Extended | Per-cylinder knock correction |
| Feedback Knock | Extended | Real-time knock correction |
| AF Correction | Extended | Short-term fuel trim |
| IPW | Extended | Injector pulse width (ms) |

### Datalog Setup
- Select PIDs based on what you're tuning/monitoring
- Balance sample rate vs number of parameters
- Essential PIDs for WRX tuning: Boost, AFR, DAM, Knock, Timing

## Related Systems

- **All**: PIDs are used to monitor all ECU parameters
- **Analytical**: Diagnostic codes

## Notes

- Standard OBD-II PIDs plus Subaru-specific extended PIDs
- Essential for datalog setup
- Custom PIDs can be defined for specific monitoring needs

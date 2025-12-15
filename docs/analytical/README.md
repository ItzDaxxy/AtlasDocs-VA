# Analytical

Diagnostic and analysis tables for ECU monitoring and troubleshooting.

## Overview

Analytical tables provide diagnostic capabilities:
- Knock detection thresholds
- Sensor validation ranges
- Error detection parameters
- Self-test criteria

## Subcategories

- **Knock Detection**: Knock sensor thresholds and sensitivity
- **Sensor Validation**: Input range checking and fault detection
- **Self-Diagnostics**: ECU self-test parameters and thresholds

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Knock Threshold High | 2D | Knock detection threshold when timing is advanced |
| Knock Threshold Low | 2D | Knock detection threshold when timing is retarded |
| Sensor Range Min | 1D | Minimum valid sensor voltage/value |
| Sensor Range Max | 1D | Maximum valid sensor voltage/value |
| DTC Enable Conditions | 2D | Conditions required to set diagnostic codes |

## Key Concepts

### Knock Detection System
The FA20DIT uses two knock sensors (one per bank):
- **Left Sensor**: Monitors cylinders 1 and 3 (front-left, rear-left)
- **Right Sensor**: Monitors cylinders 2 and 4 (front-right, rear-right)

Knock detection uses:
- Raw knock sensor voltage converted to counts
- Threshold comparison per-cylinder
- Frequency filtering to isolate knock signature (~6-7 kHz for FA20)

### Sensor Validation
ECU continuously validates sensor inputs:
- **Open Circuit**: Voltage too high (pulled to 5V)
- **Short Circuit**: Voltage too low (grounded)
- **Range Fault**: Value outside physical possibility

### Diagnostic Trouble Codes (DTCs)
- **P-codes**: Powertrain-related (most tuning-relevant)
- **Enable Conditions**: Speed, temp, time requirements to set code
- **Freeze Frame**: Snapshot of conditions when code set

## Related Systems

- **Sensors**: Validation ranges for sensor inputs
- **Engine**: Operating parameter bounds
- **PIDs**: Diagnostic trouble codes

## Notes

- Critical for understanding ECU self-diagnostics
- Useful for setting up datalog triggers

# VDC (Vehicle Dynamics Control)

Stability and traction control tables.

## Overview

VDC tables control:
- Traction control intervention thresholds
- Stability control parameters
- ABS integration
- Wheel slip limits
- Yaw rate targets

## Subcategories

- **Traction Control**: Wheel slip detection and throttle/ignition intervention
- **Stability Control**: Yaw rate and lateral acceleration management
- **ABS Integration**: Anti-lock braking coordination with engine management

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Traction Control Threshold | 2D | Wheel slip % threshold for TC intervention |
| Stability Yaw Target | 2D | Target yaw rate based on steering angle and speed |
| TC Throttle Reduction | 2D | Throttle cut magnitude during TC intervention |
| TC Ignition Cut | 2D | Ignition timing retard during TC intervention |
| VDC Enable Speed | 1D | Minimum vehicle speed for VDC activation |

## Key Concepts

### Traction Control (TC)
- Monitors wheel speed differential between driven wheels
- Intervenes via throttle reduction and ignition timing retard
- Can be reduced or disabled for track use (at driver's risk)

### Stability Control (VDC)
- Monitors yaw rate, lateral acceleration, and steering angle
- Compares actual vs expected vehicle behavior
- Can apply individual wheel braking to correct oversteer/understeer

### AWD Integration
- VA WRX uses Active Torque Vectoring AWD
- VDC coordinates with center differential control
- Torque split adjustments complement stability interventions

## Related Systems

- **Throttle**: VDC can reduce throttle
- **Engine**: VDC can cut ignition/fuel
- **Transmission**: AWD torque split

## Notes

- VDC = Vehicle Dynamics Control (Subaru's stability system)
- Can be partially or fully disabled via tables
- Traction control separate from stability control
- Affects AWD center differential behavior

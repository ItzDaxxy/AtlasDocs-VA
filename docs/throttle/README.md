# Throttle

Electronic throttle control (ETC) tables.

## Overview

Throttle tables control:
- Pedal-to-throttle mapping
- Throttle response curves
- Drive-by-wire behavior
- Throttle limiters
- Cruise control integration

## Subcategories

### Pedal-to-Throttle Mapping
Defines the relationship between accelerator pedal position and throttle blade opening:
- **Main Throttle Map**: Primary pedal-to-throttle conversion
- **Sport Mode Map**: More aggressive throttle response
- **Eco Mode Map**: Smoother, more gradual response

### Requested Torque
Torque-based throttle control for drivetrain protection:
- **Requested Torque Target**: Base torque request tables
- **Torque Limits - Main**: Maximum torque limits by condition
- **Torque Limits - Temperature**: Thermal protection limits

### Throttle Response
Controls throttle blade movement characteristics:
- **Opening Rate**: Maximum throttle opening speed
- **Closing Rate**: Throttle closing characteristics
- **Tip-In Compensation**: Response to sudden pedal input

### Cruise Control
Automatic speed maintenance tables:
- **Cruise Speed Targets**: Speed control parameters
- **Cruise Throttle Authority**: Throttle range for cruise

## Key Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Pedal to Throttle | 2D Map | Main pedal-to-throttle conversion |
| Requested Torque Target | 3D Map | Torque request by pedal/RPM |
| Torque Limits - Main | 3D Map | Maximum allowed torque |
| Torque Limits - Oil Temp | Scalar | Oil temperature protection threshold |
| Throttle Opening Rate | 2D Map | Maximum opening speed |
| Tip-In Smoothing | 2D Map | Response filtering |

## Related Systems

- **Engine**: Throttle position determines engine load
- **Airflow**: Throttle position directly affects airflow
- **VDC**: Traction control can limit throttle
- **Transmission**: Throttle blips for rev matching
- **Fuel**: Throttle transients affect fueling strategy

## Technical Details

### Drive-by-Wire Operation
The FA20DIT uses electronic throttle control (no mechanical cable):
1. **Pedal Position Sensor**: Measures driver input (0-100%)
2. **ECU Processing**: Applies mapping and limits
3. **Throttle Motor**: Moves throttle blade to commanded position
4. **TPS Feedback**: Confirms actual position matches command

### Response Characteristics
- Stock mapping provides smooth, non-linear response
- Light pedal input = small throttle opening (smoothness)
- Heavy pedal input = aggressive throttle response (performance)
- Electronic filtering prevents jerky response

## Notes

- FA20DIT uses electronic throttle (no cable)
- Pedal position ≠ throttle position (non-linear mapping)
- "Sport" modes typically steepen the response curve
- Torque-based control limits drivetrain stress
- Temperature protection reduces torque when engine/oil hot
- Cruise control has limited throttle authority for safety

# Transmission

Gearbox and transmission control tables.

## Overview

Transmission tables control:
- Shift points (CVT/automatic)
- Rev matching (manual)
- Gear ratios (for calculations)
- Launch control
- Flat foot shifting

## Subcategories

### Gear Ratios
Defines the gear ratio constants used for speed/load calculations:
- **Gear Ratio 1st-6th**: Individual gear ratios for ECU calculations
- **Final Drive Ratio**: Differential ratio
- **Tire Circumference**: Wheel size for speed calculation

### Rev Matching
Controls automatic throttle blips during downshifts:
- **Rev Match Enable**: Activation conditions
- **Rev Match Target RPM**: Target RPM calculation
- **Blip Duration/Intensity**: Throttle blip characteristics

### Launch Control (if equipped)
Manages launch RPM and traction for optimal acceleration:
- **Launch RPM Limit**: Rev limit during launch
- **Launch Timing Retard**: Ignition timing during launch
- **Launch Boost Target**: Boost building during launch

## Key Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Gear Ratio 1 | Scalar | 1st gear ratio (3.454) |
| Gear Ratio 2 | Scalar | 2nd gear ratio (1.947) |
| Gear Ratio 3 | Scalar | 3rd gear ratio (1.296) |
| Gear Ratio 4 | Scalar | 4th gear ratio (0.972) |
| Gear Ratio 5 | Scalar | 5th gear ratio (0.738) |
| Gear Ratio 6 | Scalar | 6th gear ratio (0.666) |
| Final Drive | Scalar | Differential ratio (4.111) |
| Rev Match Blip | 2D Map | Throttle blip intensity by gear/RPM |

## Related Systems

- **Engine**: Rev limiter during shifts, launch control integration
- **Throttle**: Throttle cut/blip during shifts
- **VDC**: Traction control integration
- **Airflow**: Boost control during launch

## Notes

- VA WRX MT uses 6-speed manual transmission
- Rev matching controlled by ECU (can be disabled)
- Launch control available in some configurations/calibrations
- Gear ratios are constants used for ECU calculations (vehicle speed, load)
- Changing gear ratios in ECU requires matching physical gearbox changes

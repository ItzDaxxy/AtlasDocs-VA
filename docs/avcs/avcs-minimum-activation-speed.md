# AVCS - Minimum Activation Speed

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | KMH |
| **Source File** | `AVCS - Minimum Activation Speed - 2018 - LF9C102P.csv` |

## Value

**1.1719 KMH**

## Description

Defines the minimum vehicle speed required before the ECU will activate AVCS control. Below this speed threshold, both intake and exhaust cam timing is held at the mechanical default position (full retard, minimum valve overlap).

This speed-based enable condition ensures adequate engine oil pressure is established before commanding the AVCS oil control valves (OCVs). The AVCS system relies on engine oil pressure to hydraulically actuate the cam phasers, making oil pressure critical for proper operation.

The stock value of 1.1719 km/h (~0.73 mph) is deliberately very low, allowing AVCS to activate almost immediately after the vehicle begins moving. This provides optimal performance and emissions control during normal driving conditions.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md)
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-closed.md)
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-open.md)
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Closed)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-closed.md)

## Related Datalog Parameters

- **Vehicle Speed** - Current vehicle speed must exceed this threshold
- **AVCS Intake Cam Advance (Actual)** - Will remain at 0 degrees (default position) when speed is below threshold
- **AVCS Exhaust Cam Retard (Actual)** - Will remain at 0 degrees (default position) when speed is below threshold
- **AVCS Intake Cam Advance (Target)** - ECU commanded target position
- **AVCS Exhaust Cam Retard (Target)** - ECU commanded target position
- **Engine Oil Pressure** - Should be adequate (>150 kPa) before AVCS activation
- **Engine Coolant Temperature** - Additional enable condition (typically >60°C required)

## Tuning Notes

**Stock Value Recommendations:**
The factory setting of 1.1719 km/h works well for most applications and should be left unchanged unless addressing specific issues.

**Increase Threshold (5-10 km/h) When:**
- Experiencing AVCS hunting or oscillation during idle or low-speed driving
- Using aftermarket oil system with reduced pressure at idle
- Launch control system conflicts with AVCS operation
- Wanting simplified behavior during parking lot maneuvers
- Testing conservative calibrations without variable cam timing at idle

**Decrease Threshold (0-1 km/h) When:**
- Performing stationary dyno tuning where AVCS activation is desired
- Need AVCS control during standing idle (rarely beneficial)
- Testing AVCS calibration changes without road driving
- Optimizing emissions at idle with cam timing adjustments

**Important Considerations:**
- AVCS requires multiple enable conditions beyond just vehicle speed (oil pressure, coolant temp, RPM range, no DTCs)
- Setting too high will delay optimal cam timing during acceleration from stops
- Setting to 0 km/h allows AVCS at complete standstill but may cause idle instability
- Always monitor AVCS actual vs target error after changes to confirm stable operation
- Significant AVCS error (>5 degrees) indicates inadequate oil pressure or mechanical issues

**Diagnostic Use:**
Temporarily increasing this value to 20-30 km/h can help diagnose whether AVCS-related idle issues are caused by cam timing changes or other factors.

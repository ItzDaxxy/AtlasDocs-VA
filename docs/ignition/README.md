# Ignition

Spark timing tables for all operating conditions.

## Overview

Ignition tables control spark advance/retard based on:
- Engine load (typically calculated load or manifold pressure)
- Engine RPM
- Coolant temperature
- Intake air temperature
- Knock sensor feedback
- AVCS position (some tables have TGV/AVCS variants)

## Subcategories

- **[Primary](primary/)**: Base ignition timing maps (4 variants for TGV/AVCS states)
- **[Dynamic Advance](dynamic-advance/)**: DAM-controlled timing adders
- **[Compensation](compensation/)**: Temperature and condition-based timing adjustments
- **[Knock Thresholds](knock-thresholds/)**: Per-cylinder knock detection sensitivity
- **[Idle/Decel](idle-decel/)**: Timing during idle and deceleration

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Primary - TGVs Closed (AVCS Disabled) | 3D | Base timing, TGVs closed, no AVCS |
| Primary - TGVs Open (AVCS Disabled) | 3D | Base timing, TGVs open, no AVCS |
| Primary - TGVs Closed (AVCS Enabled) | 3D | Base timing, TGVs closed, AVCS active |
| Primary - TGVs Open (AVCS Enabled) | 3D | Base timing, TGVs open, AVCS active |
| Dynamic Advance Base | 3D | Additional timing scaled by DAM |
| DAM Initial Value | Constant | Starting DAM after ECU reset (0.125) |
| Knock Threshold Cyl 1-4 | 2D | Per-cylinder knock sensitivity |
| Coolant Compensation | 2D | Timing adjustment for coolant temp |
| IAT Compensation | 2D | Timing adjustment for intake air temp |

## Key Concepts

### Timing Calculation
Final timing = Primary + (Dynamic Advance × DAM) + Compensations - Knock Retard

### Dynamic Advance Multiplier (DAM)
- Range: 0.0 to 1.0 (some ROMs 0-16 scaled)
- Starts at 0.125 (1/8) after ECU reset
- Increases if no knock detected
- Decreases with sustained knock events
- DAM of 1.0 = full timing, 0.5 = 50% of dynamic advance

### TGV and AVCS Variants
The ECU selects between 4 primary timing maps based on:
- **TGV State**: Open (high flow) or Closed (tumble generation)
- **AVCS State**: Whether variable cam timing is active
Each combination has different optimal ignition timing

## Related Systems

- **Fuel**: AFR affects knock threshold
- **AVCS**: Valve timing affects optimal spark timing
- **Sensors**: Knock sensor input
- **Analytical**: Knock thresholds

## Notes

- Timing is typically measured in degrees BTDC (Before Top Dead Center)
- Negative values = retarded timing
- Knock pulls timing temporarily via feedback
- Always monitor knock counts when adjusting timing

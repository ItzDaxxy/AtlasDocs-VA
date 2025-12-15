# AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | NONE |
| **Source File** | `AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Provides additive compensation values (in degrees) that modify the base intake cam advance target from the primary intake cam target table when operating at low barometric pressure (high altitude, typically above ~3000 ft) with TGV valves closed. This compensation table allows altitude-specific fine-tuning of cam timing across the operating range.

At high altitude, reduced air density affects engine performance and optimal cam timing strategy. This compensation table allows the ECU to adjust cam timing specifically for high-altitude operation while preserving the base calibration structure. In stock calibration, this table is typically populated with zeros, but provides a mechanism for altitude-specific tuning adjustments.

This table shares the same TGV operating conditions as the high barometric variant - active when TGV valves are closed (low/mid RPM, light load conditions) but specifically for low barometric pressure (high altitude) operation.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 3.0960
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8000.0000
- **Points**: 20

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 1600.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2000.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2800.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 3200.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
```

## Functional Behavior

The ECU applies this compensation table as follows:

1. **Barometric Monitoring:** ECU continuously monitors barometric pressure via sensor
2. **Table Selection:** Active when TGV valves are closed AND barometric pressure is low (high altitude)
3. **2D Interpolation:** ECU looks up compensation value based on current RPM and calculated load
4. **Additive Application:** The interpolated value is added to the base target from the primary intake cam target table
5. **Final Target Calculation:** Base Target + Compensation + Activation Scaling = Final Commanded Position
6. **Altitude Adaptation:** Compensation allows altitude-specific optimization without changing base calibration

The barometric pressure threshold between "high" and "low" multiplier tables is calibration-dependent, typically around 90-95 kPa (approximately 3000-5000 ft elevation).

## Related Tables

- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-closed.md) - Base target table for low barometric pressure
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-closed.md) - Sea level equivalent
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-open.md) - Companion compensation for TGV open
- [AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Retard Compensation (TGV Closed)](./avcs-exhaust-barometric-multiplier-low-exhaust-cam-retard-compensation-tgv-closed.md) - Exhaust cam compensation counterpart
- [AVCS - Intake - Intake Cam Advance Target Adder Activation](./avcs-intake-intake-cam-advance-target-adder-activation.md) - Activation scaling table

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target including compensation
- **AVCS Intake Cam Advance (Actual)** - Measured cam position
- **AVCS Intake Cam Advance Error** - Tracking error
- **TGV Position** - Must be closed for this table to be active
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **Calculated Load** - X-axis lookup parameter
- **Barometric Pressure** - Must be low (high altitude) for table selection
- **Intake Cam Advance Compensation** - Direct monitor of compensation value if available
- **Manifold Absolute Pressure** - Helps verify altitude conditions

## Tuning Notes

**High Altitude Specific Tuning:**

Altitude affects cam timing requirements in several ways:
- Reduced air density changes optimal valve overlap characteristics
- Lower oxygen content may benefit from different scavenging strategy
- Reduced power output at altitude may allow more aggressive cam timing
- Turbo boost characteristics change at altitude, affecting optimal cam timing

**Typical Modification Patterns:**

**Altitude Optimization:**
- Adjust compensation to recover performance lost to altitude
- May use more aggressive advance to improve cylinder filling
- Typical range: +3 to +10 degrees in cruise/light-load regions
- Consider local altitude if vehicle operates primarily at high elevation

**Idle Refinement:**
- Altitude can affect idle quality - use compensation to fine-tune
- Small negative compensation (retard) may improve stability at altitude
- Typical range: -2 to -5 degrees in lowest RPM/load cells
- Test cold-start behavior at altitude conditions

**Cross-Altitude Calibration:**
- If tuning for specific altitude, this table is critical
- Vehicles operating at multiple altitudes need both high and low tables optimized
- Ensure smooth transition at barometric threshold between table sets
- Consider customer's typical operating elevation

**Coordination Requirements:**
- Synchronize with exhaust cam low barometric compensation
- Verify ignition timing tables appropriate for altitude operation
- Check that fuel tables compensate for altitude VE changes
- Test boost control calibration at altitude if turbo equipped

## Warnings

**Altitude-Specific Risks:**

**Barometric Threshold Transitions:**
- Driving between sea level and high altitude crosses barometric threshold
- Ensure smooth transition between high and low barometric compensation tables
- Large differences between tables can cause driveability issues
- Test at various altitudes if possible

**Altitude Performance:**
- High altitude reduces available power - aggressive cam timing won't recover all losses
- Turbo boost may be limited at altitude regardless of cam timing
- Excessive advance at altitude can still cause knock despite reduced power
- Oil pressure and temperature characteristics may differ at altitude

**System Interactions:**
- Cam timing changes affect VE at altitude differently than sea level
- MAF calibration becomes more critical with altitude-specific cam tuning
- Fuel trims may need wider authority for cross-altitude operation
- Boost control strategy must coordinate with cam timing

**Testing Requirements:**
- Ideal testing includes validation at actual operating altitude
- Barometric simulation or altitude chamber testing may be necessary
- Monitor cam position tracking at altitude - oil characteristics may vary
- Verify idle stability across temperature range at altitude
- Check for altitude-related DTCs after modifications

**Do Not:**
- Make large changes without understanding local barometric pressure
- Assume altitude compensation works the same as sea level tuning
- Ignore the threshold between high and low barometric tables
- Forget that this table affects idle quality (TGV closed operation)
- Apply sea-level tuning strategies directly to altitude compensation

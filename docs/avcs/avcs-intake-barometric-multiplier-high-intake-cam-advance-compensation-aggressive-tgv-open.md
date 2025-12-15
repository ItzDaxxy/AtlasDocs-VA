# AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | NONE |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Provides additive compensation values (in degrees) that modify the base intake cam advance target under "aggressive" operating conditions at high barometric pressure (sea level to ~3000 ft) with TGV valves open. This is an alternate compensation table that the ECU may select based on specific operating conditions such as higher coolant temperatures, performance driving modes, or certain load/RPM combinations.

The "aggressive" variant typically represents a more performance-oriented cam timing strategy compared to the standard table. It may be activated during conditions where the ECU determines more aggressive cam timing is appropriate - potentially including high coolant temperatures, sport mode selections, or sustained high-load operation. The exact activation logic is ECU-dependent and may vary based on multiple operating parameters.

This table operates when TGV valves are open (high RPM and/or high load conditions) where maximum airflow is required, and barometric pressure is high (near sea level).

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 2.8380
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

The ECU applies this aggressive compensation table as follows:

1. **Condition Monitoring:** ECU continuously monitors parameters that trigger aggressive mode selection
2. **Table Selection:** Active when aggressive mode conditions are met AND TGV valves are open AND barometric pressure is high
3. **2D Interpolation:** ECU looks up compensation value based on current RPM and calculated load
4. **Additive Application:** The interpolated value is added to the base target from the primary intake cam target table
5. **Mode Transitions:** ECU manages smooth transitions between standard and aggressive compensation tables
6. **Final Target Calculation:** Base Target + Aggressive Compensation + Activation Scaling = Final Commanded Position

The transition between standard and aggressive compensation modes is designed to be smooth to prevent driveability issues. The ECU uses hysteresis and filtering to avoid rapid switching between modes.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target Aggressive (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-aggressive-tgv-open.md) - Base aggressive target table
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Standard (non-aggressive) base target
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation Aggressive (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-aggressive-tgv-open.md) - High altitude equivalent
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation Aggressive (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-aggressive-tgv-open.md) - Exhaust cam aggressive compensation
- [AVCS - Intake - Intake Cam Advance Target Adder Activation](./avcs-intake-intake-cam-advance-target-adder-activation.md) - Activation scaling table

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target including aggressive compensation
- **AVCS Intake Cam Advance (Actual)** - Measured cam position
- **AVCS Intake Cam Advance Error** - Tracking error
- **TGV Position** - Must be open for this table to be active
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **Calculated Load** - X-axis lookup parameter
- **Barometric Pressure** - Must be high for table selection
- **Coolant Temperature** - May influence aggressive mode activation
- **Intake Cam Advance Compensation** - Direct monitor of compensation value if available

## Tuning Notes

**Understanding Aggressive Mode:**

The aggressive compensation table provides an opportunity for dual-strategy calibration:
- Conservative timing for normal driving (standard compensation)
- More aggressive timing for performance scenarios (this table)
- ECU automatically selects appropriate strategy based on conditions

**Typical Modification Patterns:**

**Performance Enhancement:**
- More aggressive advance in power band (typically 3000-6500 RPM)
- Optimize for maximum cylinder filling and VE
- Typical range: +5 to +15 degrees in performance regions
- Must coordinate with ignition timing and fuel delivery

**Mode-Specific Strategy:**
- Differentiate aggressive mode from standard mode for distinct behavior
- Larger values create more noticeable difference when aggressive mode activates
- Consider driver expectations if in a selectable performance mode
- Test transition smoothness between modes

**High-Load Optimization:**
- Focus on cells that see use during aggressive driving
- Higher RPM and load regions benefit most from aggressive cam timing
- Ensure oil pressure and temperature are adequate for aggressive timing
- Monitor actual vs target cam position during high-load operation

**Coordination Requirements:**
- Synchronize with aggressive exhaust cam compensation
- Ensure ignition timing tables support increased cam advance
- Verify fuel delivery matches VE changes from cam timing
- Test across full temperature range - aggressive mode may activate based on temp

## Warnings

**Aggressive Mode Specific Risks:**

**Mode Activation Uncertainty:**
- Exact conditions triggering aggressive mode may not be fully documented
- Mode switches may occur unpredictably if activation logic is unclear
- Always test both standard and aggressive tables thoroughly
- Monitor datalogs to understand when aggressive mode becomes active

**Performance Risks:**
- Aggressive compensation typically adds more cam advance for performance
- Excessive advance increases valve-to-piston contact risk
- Knock sensitivity changes with aggressive cam timing
- Oil temperature and pressure critical for aggressive cam operation

**System Coordination:**
- Aggressive intake and exhaust timing must work together
- Ignition timing requirements change significantly with aggressive cam timing
- Fuel delivery must match altered VE from aggressive strategy
- MAF calibration may need adjustment for aggressive mode operation

**Testing Requirements:**
- Log all operating conditions when aggressive mode is active
- Verify smooth transitions between standard and aggressive modes
- Test at temperature extremes if temp-based activation is suspected
- Monitor knock, AFR, and cam position tracking during aggressive operation
- Validate that ECU can achieve commanded aggressive cam positions

**Do Not:**
- Make aggressive compensation more extreme than +20 degrees without extensive testing
- Ignore the base target and standard compensation when tuning aggressive compensation
- Forget to test transition behavior between modes
- Assume aggressive mode activates the same way across all ECU calibrations
- Use aggressive mode for conditions requiring conservative, reliable operation

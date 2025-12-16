# AVCS - Intake - Barometric Multiplier High - Intake Cam Target Aggressive (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Target Aggressive (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines an alternative "aggressive" intake camshaft advance calibration for high barometric pressure (sea level) conditions when TGV valves are open. This table represents a more performance-oriented cam timing strategy compared to the standard intake cam target table.

The "Aggressive" designation indicates this table uses more advanced cam timing across the operating range, typically targeting:
- Higher valve overlap for improved high-RPM breathing
- More aggressive scavenging at high load
- Performance-oriented VE optimization
- Potentially sacrificing some idle quality or low-speed drivability for power gains

The ECU likely selects between standard and aggressive tables based on specific operating conditions, driver modes, or calibration switches. This allows the ECU to use conservative timing for daily driving and aggressive timing for performance driving.

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

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
  800.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
 1200.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
 1600.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2000.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2400.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2800.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 3200.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
```

## Functional Behavior

The ECU uses this aggressive calibration table under specific performance-oriented conditions:

1. **Table Selection Logic:** ECU determines when to use Aggressive vs standard intake cam target (may be based on driving mode, pedal position history, specific operating windows, or calibration flags)
2. **2D Interpolation:** When active, ECU interpolates RPM and load to determine aggressive cam advance target
3. **Compensation:** Base aggressive target is modified by same compensation and activation tables as standard target
4. **Performance Optimization:** Aggressive table typically shows higher advance values across most cells for maximum VE and power

Comparing cell values to the standard table reveals the performance delta - typically 5-15 degrees more advance in key operating regions.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Standard (non-aggressive) calibration
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target Aggressive (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-target-aggressive-tgv-open.md) - High altitude aggressive variant
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target Aggressive (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-aggressive-tgv-open.md) - Companion aggressive exhaust cam table

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Shows if aggressive table is being used
- **AVCS Intake Cam Advance (Actual)** - Actual cam position
- **Drive Mode** - May influence aggressive vs standard table selection
- **Calculated Load** - X-axis lookup
- **Engine Speed (RPM)** - Y-axis lookup
- **Pedal Position** - May factor into table selection logic

## Tuning Notes

**Understanding Aggressive vs Standard:**
Compare this table cell-by-cell with the standard intake cam target to see the OEM performance delta. The aggressive table typically shows:
- More uniform positive advance across all cells
- Higher values at mid-to-high load for maximum power
- Less load-dependent variation (flatter calibration)
- Optimization for peak VE rather than drivability

**When to Modify Aggressive Table:**
- Performance builds benefit from aggressive table optimization
- Can push advance further than standard table for race applications
- Focus on high-load, high-RPM cells where power is made
- Less concern for idle quality since standard table handles that

**Tuning Strategy:**
- Start with standard table values and add 5-10 degrees progressively
- Monitor knock activity carefully (more advance = more knock risk)
- Coordinate with aggressive exhaust cam table for optimal overlap
- Test maximum advance limits in high-load cells
- Consider that this table may only activate in specific modes or conditions

**For Modified Engines:**
- Larger turbos benefit from more aggressive cam timing
- E85 fuel allows significantly more advance due to knock resistance
- Aftermarket cams may need complete recalibration of aggressive table
- High-boost applications may need to reduce advance despite "aggressive" label

## Warnings

**Performance-Oriented Risks:**
- Aggressive cam timing increases knock sensitivity at high load
- More overlap can cause idle instability if table is poorly selected
- May sacrifice low-end torque and drivability for top-end power
- Increases cylinder pressure and stress on engine components

**Table Selection Uncertainty:**
- Selection logic between standard and aggressive may not be fully documented
- Changes may not activate if ECU doesn't invoke aggressive table
- Verify datalog shows aggressive targets being commanded during testing
- May require specific enable conditions (driving mode, pedal behavior, etc.)

**Knock and Reliability:**
- Always monitor knock count and feedback when testing aggressive timing
- More advance requires more ignition timing retard headroom
- Consider piston-to-valve clearance with extreme advance values
- Oil pressure must be excellent for rapid AVCS response to aggressive targets

**Coordination:**
- Must work in tandem with aggressive exhaust cam table
- Ignition timing tables should account for aggressive cam positions
- Fuel tables may need adjustment for altered VE characteristics

# AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 18x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines target exhaust camshaft retard angles for high barometric pressure (sea level to ~3000 ft) conditions when the Tumble Generator Valves (TGV) are open. This table controls exhaust cam timing to optimize valve overlap, scavenging, and exhaust gas evacuation across the operating range.

Exhaust cam retard moves the exhaust camshaft timing later relative to the crankshaft, which delays the exhaust valve closing event. Positive values represent retarding the exhaust cam toward more valve overlap with the intake valves. This affects:
- Valve overlap duration and characteristics
- Exhaust scavenging efficiency
- Residual exhaust gas retention (internal EGR)
- Cylinder-to-cylinder charge homogeneity
- Turbocharged spool characteristics
- Exhaust gas temperature and emissions

Combined with intake cam advance, exhaust cam retard creates variable valve overlap that the ECU optimizes for different performance, efficiency, and emissions targets across the operating map.

## Axes

### X-Axis

- **Parameter**: AVCS - Intake - Target - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1935 to 2.8380
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7200.0000
- **Points**: 18

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1935 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     0.0000 |     0.0000 |     0.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
  800.0000 |     0.0000 |     0.0000 |     0.0000 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1100.0000 |     0.0000 |     4.9993 |     9.0015 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1200.0000 |     0.0000 |     4.9993 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |    10.0014 |
 1600.0000 |     0.0000 |    12.0011 |    15.0007 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2000.0000 |     0.0000 |    12.0011 |    18.0030 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2400.0000 |     0.0000 |    11.0012 |    12.0011 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
 2800.0000 |     0.0000 |    11.0012 |    11.0012 |    10.0014 |    10.0014 |    10.0014 |    15.0007 |    15.0007 |
```

## Functional Behavior

The ECU performs 2D interpolation to determine exhaust cam retard target:

1. **Table Selection:** Active when barometric pressure is high (>~900 hPa) and TGV valves are open
2. **Base Target Lookup:** ECU interpolates RPM (Y-axis) and calculated load (X-axis) for base exhaust retard target
3. **Compensation Application:** Base target is modified by exhaust cam compensation adders and activation scaling
4. **Overlap Coordination:** ECU coordinates exhaust cam retard with intake cam advance to achieve desired total valve overlap
5. **Command Output:** Final target sent to exhaust cam AVCS oil control valve

The exhaust cam typically operates in a smaller range than intake cam (0-30 degrees retard vs 0-50 degrees advance for intake), reflecting its more focused role in overlap control.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Companion intake cam table (must coordinate)
- [AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-low-exhaust-cam-target-tgv-open.md) - High altitude equivalent
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Closed)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-closed.md) - TGV closed variant
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target Aggressive (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-aggressive-tgv-open.md) - Aggressive variant
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-tgv-open.md) - Compensation adders
- [AVCS - Exhaust - Exhaust Cam Retard Target Adder Activation](./avcs-exhaust-exhaust-cam-retard-target-adder-activation.md) - Temperature-based activation
- [Ignition - Primary - AVCS Enabled - TGV Open](./ignition-primary-avcs-enabled-tgv-open.md) - Ignition timing for AVCS active conditions

## Related Datalog Parameters

- **AVCS Exhaust Cam Retard (Target)** - Final commanded exhaust cam target
- **AVCS Exhaust Cam Retard (Actual)** - Measured exhaust cam position
- **AVCS Exhaust Cam Retard Error** - Target vs actual difference
- **AVCS Exhaust Duty Cycle** - Exhaust OCV solenoid command
- **AVCS Intake Cam Advance (Target)** - Must coordinate with exhaust for proper overlap
- **AVCS Intake Cam Advance (Actual)** - Actual intake position
- **Engine Speed (RPM)** - Y-axis lookup
- **Calculated Load** - X-axis lookup
- **TGV Position** - Determines table selection
- **Barometric Pressure** - High vs Low table selection
- **Engine Oil Pressure** - Required for AVCS operation

## Tuning Notes

**Understanding Exhaust Cam Strategy:**

Exhaust cam retard works in conjunction with intake cam advance to control valve overlap:
- **More exhaust retard** = Later exhaust valve closing = More overlap = More scavenging/EGR
- **Less exhaust retard** = Earlier exhaust valve closing = Less overlap = Cleaner separation

Stock calibration typically shows:
- Minimal retard at idle/low load (reduce overlap for stable combustion)
- Moderate retard at mid-load (balance scavenging and efficiency)
- Higher retard at high load/RPM (maximize scavenging, help turbo spool)

**Valve Overlap Effects:**

Total valve overlap = Intake advance + Exhaust retard

**Increasing Overlap (More Retard):**
- Improves exhaust scavenging at high RPM
- Can help turbo spool by maintaining exhaust energy
- Increases internal EGR (reduces combustion temp and knock sensitivity)
- May reduce low-RPM cylinder pressure and torque
- Risk of rough idle if applied at low load

**Decreasing Overlap (Less Retard):**
- Improves cylinder pressure and low-end torque
- Cleaner cylinder charge (less residual exhaust)
- Better idle stability
- May limit high-RPM breathing and scavenging
- Potentially higher combustion temperatures

**Coordination with Intake Cam:**

Exhaust and intake cam timing must be coordinated:
- Both advancing creates more overlap
- Offsetting changes can maintain overlap while shifting valve events
- Test combinations systematically rather than changing one cam in isolation

**Typical Modifications:**

**For Improved Turbo Spool:**
- Increase retard at spool-critical RPM range (2000-4000 RPM, mid-high load)
- More overlap helps maintain exhaust energy to turbine
- Coordinate with intake advance for optimal overlap

**For Better Low-End Torque:**
- Reduce retard at low RPM/load
- Less overlap improves cylinder pressure
- Balance against emissions and idle quality

**For High-RPM Power:**
- Increase retard at peak power RPM
- Maximize scavenging efficiency
- Watch for diminishing returns (excessive overlap can hurt)

**For E85/High Octane Fuel:**
- Can run more aggressive retard due to knock resistance
- Increased overlap and internal EGR tolerated better
- Still monitor knock activity

**Common Adjustments:**
- Incremental changes of 2-5 degrees
- Test across full RPM range
- Monitor knock, EGT, and boost response
- Validate with intake cam coordination

## Warnings

**Critical Coordination:**
- Exhaust cam timing must be coordinated with intake cam timing
- Changing only exhaust without considering intake can create suboptimal overlap
- Total overlap affects knock sensitivity, torque, and emissions
- Always consider the combined effect of both cams

**Overlap-Related Risks:**

**Excessive Overlap (Too Much Retard):**
- Can cause rough idle and low-speed instability
- May reduce cylinder pressure and low-end torque
- Excessive internal EGR can affect combustion stability
- Potential for intake charge dilution with exhaust gases

**Insufficient Overlap (Too Little Retard):**
- Limits high-RPM scavenging and breathing
- May increase combustion temperatures and knock risk
- Reduced benefit of dual AVCS system
- Potential EGT concerns without adequate scavenging

**Turbocharger Interactions:**
- Exhaust cam timing significantly affects turbo spool and response
- Changes can alter boost onset and peak boost capability
- Exhaust backpressure characteristics change with cam timing
- Wastegate and boost control may need adjustment

**Mechanical Limits:**
- Typical exhaust AVCS range: 0-30 degrees retard
- Requesting targets beyond mechanical range causes tracking errors
- Oil pressure must be adequate for commanded positions
- Cold oil reduces AVCS response speed

**Testing Requirements:**
- Monitor exhaust gas temperatures (EGT) after exhaust cam changes
- Check turbo spool characteristics across RPM range
- Validate knock activity hasn't increased
- Verify AVCS tracking error remains acceptable (<3 degrees)
- Test idle stability and cold-start behavior

**Emissions Impact:**
- Exhaust cam timing is critical for emissions compliance
- Changes may affect catalyst warm-up and efficiency
- Light-load cells are heavily emissions-tested
- May trigger check engine lights or failed emissions tests

**Do Not:**
- Make large changes to idle/light-load cells
- Exceed mechanical AVCS limits
- Ignore coordination with intake cam timing
- Copy values from different TGV state tables without validation
- Assume more retard is always better (highly RPM/load dependent)

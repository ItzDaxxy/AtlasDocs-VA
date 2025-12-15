# AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines target intake camshaft advance angles for low barometric pressure (high altitude, typically >3000 ft) conditions when the Tumble Generator Valves (TGV) are open. This table provides altitude-compensated intake cam timing calibration for operation at higher elevations where air density is reduced.

The low barometric multiplier strategy adjusts cam timing to compensate for reduced air density at altitude. Comparing this table to the High barometric version reveals altitude compensation strategy - typically showing different advance values to optimize torque and emissions at reduced atmospheric pressure.

This table is actively used when:
- Barometric pressure <~900 hPa (elevation >~3000 ft / ~1000 m)
- TGV valves are open (high RPM or high load operation)
- AVCS system is enabled (vehicle speed > minimum activation threshold)
- All AVCS enable conditions are met (oil pressure, coolant temp, etc.)

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
  400.0000 |   -10.0014 |   -11.0012 |    -7.0018 |    -0.9999 |     2.9996 |     6.0019 |    10.0014 |    20.0027 |
  800.0000 |   -10.0014 |   -11.0012 |    -7.0018 |    -0.9999 |     2.9996 |     6.0019 |    10.0014 |    20.0027 |
 1200.0000 |   -10.0014 |   -11.0012 |    -2.9996 |     0.9999 |     6.0019 |     6.0019 |     8.0016 |    10.0014 |
 1600.0000 |    -9.0015 |    -9.0015 |   -10.0014 |    -7.0018 |    -3.9995 |    -0.9999 |     1.9997 |    10.0014 |
 2000.0000 |    -7.0018 |    -7.0018 |   -15.0007 |   -12.0011 |    -9.0015 |    -6.0019 |     4.9993 |    15.0007 |
 2400.0000 |    -6.0019 |    -6.0019 |   -15.0007 |   -13.0010 |   -11.0012 |     0.0000 |    10.0014 |    20.0027 |
 2800.0000 |    -6.0019 |    -6.0019 |   -15.0007 |   -14.0008 |   -13.0010 |     0.0000 |    10.0014 |    20.0027 |
 3200.0000 |    -6.0019 |    -6.0019 |   -15.0007 |   -14.0008 |   -13.0010 |   -12.0011 |     0.0000 |    10.0014 |
```

## Functional Behavior

The ECU performs 2D interpolation on this table using current RPM and calculated engine load when operating at high altitude:

1. **Barometric Pressure Monitoring:** ECU continuously monitors atmospheric pressure via barometric pressure sensor
2. **Table Selection:** When barometric pressure falls below threshold (~900 hPa), ECU switches from High to Low barometric tables
3. **Base Target Lookup:** ECU interpolates RPM (Y-axis) and load (X-axis) to determine base intake cam advance target
4. **Compensation:** Base target is modified by compensation adders and temperature-based activation scaling
5. **Command Output:** Final target sent to AVCS PID controller for OCV actuation

The transition between High and Low barometric tables includes hysteresis to prevent rapid switching near the threshold pressure.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Sea level equivalent table
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-closed.md) - Low altitude, TGV closed variant
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target Aggressive (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-target-aggressive-tgv-open.md) - Aggressive variant
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-open.md) - Additive compensation
- [AVCS - Exhaust - Barometric Multiplier Low - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-low-exhaust-cam-target-tgv-open.md) - Companion exhaust cam table

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target
- **AVCS Intake Cam Advance (Actual)** - Measured position
- **AVCS Intake Cam Advance Error** - Target vs actual difference
- **Barometric Pressure** - Determines table selection (key parameter)
- **Engine Speed (RPM)** - Y-axis lookup
- **Calculated Load** - X-axis lookup
- **TGV Position** - Must indicate TGV open state
- **Altitude** - Derived from barometric pressure
- **Engine Oil Pressure** - AVCS enable condition

## Tuning Notes

**Altitude Compensation Strategy:**
At high altitude, reduced air density affects:
- Turbo boost levels (less dense air = lower absolute pressure)
- Volumetric efficiency characteristics
- Combustion stability and knock sensitivity
- Exhaust gas temperatures and scavenging

The Low barometric table typically uses different cam timing strategies to compensate for these altitude-related changes.

**Comparison with High Barometric Table:**
When tuning, compare values cell-by-cell with the High barometric version to understand the OEM altitude compensation strategy. Common patterns:
- May use less aggressive advance at altitude due to reduced knock sensitivity
- Could optimize for different torque characteristics given reduced air density
- May account for turbo efficiency changes at altitude

**Tuning for High Altitude Operations:**
If vehicle operates primarily at high altitude:
- Focus tuning effort on this Low barometric table
- Consider that boost targets and wastegate duty will differ from sea level
- Account for reduced cooling efficiency in thinner air
- Monitor oil pressure more carefully (altitude can affect oil system performance)

**General Modification Guidelines:**
Follow same tuning principles as High barometric table:
- Incremental changes of 2-5 degrees
- Test across full operating range
- Coordinate with exhaust cam timing
- Validate with datalog analysis (target vs actual tracking)

**For Vehicles at Sea Level:**
If vehicle never operates at high altitude, this table sees minimal use. However:
- Keep it synchronized with High barometric table unless specific altitude tuning is needed
- Use it as a backup calibration
- Consider that rapid altitude changes (mountain driving) will invoke this table

## Warnings

**Altitude-Specific Considerations:**

**Barometric Pressure Switching:**
- ECU switches between High/Low tables based on barometric pressure threshold
- Abrupt differences between High and Low tables will cause harsh transitions
- Ensure smooth calibration continuity between the two tables
- Test transitions by simulating altitude changes or driving through elevation changes

**Turbocharged Engine Altitude Effects:**
- Boost pressure is absolute, so effective boost (gauge pressure) is higher at altitude for same turbo speed
- Cam timing changes may interact differently with altered boost characteristics
- Knock sensitivity changes with altitude (generally less knock risk at high altitude)
- Exhaust back pressure and turbine efficiency shift with altitude

**Oil System Considerations:**
- Oil pressure may be affected by altitude (reduced atmospheric pressure)
- AVCS response characteristics can change with altitude-related oil pressure variation
- Cold-weather high-altitude operation is particularly challenging for oil viscosity

**Calibration Dependencies:**
- Ensure ignition and fuel tables also have proper altitude compensation
- Boost control strategy must account for altitude effects
- All AVCS-related tables (intake and exhaust) should be coordinated for altitude operation

**Testing Requirements:**
- If possible, test at actual altitude conditions
- Use barometric pressure override (if available) for sea-level testing
- Monitor for AVCS tracking errors when switching between barometric tables
- Validate behavior across altitude transitions (e.g., mountain pass driving)

**Do Not:**
- Create large discontinuities between High and Low barometric tables
- Ignore this table if vehicle may see high-altitude operation
- Copy values between different TGV state tables without validation
- Exceed AVCS mechanical range limits (0-50 degrees typical)

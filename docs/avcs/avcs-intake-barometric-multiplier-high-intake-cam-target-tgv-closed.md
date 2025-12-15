# AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Defines target intake camshaft advance angles for high barometric pressure (sea level to ~3000 ft) conditions when the Tumble Generator Valves (TGV) are closed. This table provides intake cam timing calibration optimized for the low/mid RPM and low load operating regions where the TGV valves create tumble flow for improved combustion efficiency.

The TGV system creates different airflow characteristics:
- **TGV Closed:** Creates tumble/swirl in the cylinders for better low-speed combustion, fuel atomization, and emissions control. Used at low RPM and light load.
- **TGV Open:** Maximizes airflow for power production. Used at high RPM and high load.

Comparing this table to the TGV Open variant reveals how cam timing strategy changes based on intake manifold flow dynamics. The closed TGV configuration typically requires different cam timing to optimize the tumble effect and maintain good drivability.

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

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |   -10.0014 |   -11.0012 |   -13.0010 |   -11.0012 |    -6.0019 |     0.9999 |    10.0014 |    15.0007 |
  800.0000 |   -10.0014 |   -11.0012 |   -13.0010 |   -11.0012 |    -6.0019 |     0.9999 |    10.0014 |    20.0027 |
 1200.0000 |   -13.0010 |   -13.0010 |   -16.0006 |   -11.0012 |    -0.9999 |     0.9999 |     2.9996 |    10.0014 |
 1600.0000 |   -15.0007 |   -16.0006 |   -20.0027 |   -12.0011 |    -2.9996 |     2.9996 |     0.9999 |     4.9993 |
 2000.0000 |   -15.0007 |   -15.0007 |   -20.0027 |   -10.0014 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
 2400.0000 |   -15.0007 |   -25.0021 |   -25.0021 |   -12.0011 |    -3.9995 |    -3.9995 |    -4.9993 |    -4.9993 |
 2800.0000 |   -14.0008 |   -14.0008 |   -17.0032 |   -17.0032 |   -12.0011 |   -11.0012 |   -11.0012 |   -10.0014 |
 3200.0000 |   -14.0008 |   -14.0008 |   -17.0032 |   -18.0030 |   -11.0012 |   -10.0014 |   -10.0014 |   -10.0014 |
```

## Functional Behavior

The ECU selects this table when TGV valves are in the closed position and barometric pressure is high:

1. **TGV State Detection:** ECU monitors TGV valve position via position sensors
2. **Table Selection:** When TGV valves are closed AND barometric pressure is high, this table becomes active
3. **2D Interpolation:** ECU interpolates based on current RPM and calculated load
4. **Compensation Application:** Base target is modified by compensation tables and activation scaling
5. **Transition Handling:** ECU manages smooth transitions when TGV valves open/close

TGV valves typically close at low RPM (<3500-4000 RPM) and light-to-moderate load. At high load or high RPM, TGV valves open and the ECU switches to the TGV Open cam timing table.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Companion table for TGV open conditions
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-closed.md) - High altitude equivalent
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-closed.md) - Additive compensation
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Closed)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-closed.md) - Companion exhaust table
- [Ignition - Primary - AVCS Enabled - TGV Closed](./ignition-primary-avcs-enabled-tgv-closed.md) - Ignition timing for this operating mode
- [Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed)](./fuel-open-loop-avcs-enabled-target-base-tgv-closed.md) - Fuel targets for TGV closed

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target
- **AVCS Intake Cam Advance (Actual)** - Measured position
- **AVCS Intake Cam Advance Error** - Tracking error
- **TGV Position** - Must indicate closed state for this table
- **TGV Target Position** - ECU commanded TGV position
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **Calculated Load** - X-axis lookup parameter
- **Throttle Position** - Influences TGV state
- **Barometric Pressure** - Table selection criterion

## Tuning Notes

**TGV Closed Operating Region:**
This table primarily affects:
- Idle and low-speed driving behavior
- Part-throttle cruise conditions
- Low-RPM acceleration and driveability
- Cold-start and warm-up behavior
- Emissions during light-load operation

**Comparing TGV Closed vs TGV Open Tables:**
The stock calibration typically shows differences between TGV states:
- TGV Closed may use less aggressive advance for stable idle
- Transition region between tables needs smooth continuity
- Different cam strategies optimize for different airflow patterns

**Tuning Priorities for This Table:**
1. **Idle Quality:** Low RPM/low load cells are critical for smooth idle
2. **Driveability:** Mid-load cells affect part-throttle response and cruise
3. **Transition Smoothness:** Cells near TGV opening threshold should match TGV Open table strategy
4. **Emissions:** Light-load operation is heavily emissions-tested; changes may affect compliance

**Modification Strategies:**

**For Improved Idle Quality:**
- Reduce advance (more negative values) at lowest RPM/load cells
- Keep changes small (<5 degrees) in idle region
- Test cold-start behavior after any idle-region changes

**For Better Part-Throttle Response:**
- Optimize mid-load cells for torque and transient response
- Consider slight advance increase for improved cylinder filling
- Validate with road testing in common driving conditions

**For TGV Delete Modifications:**
If TGV system is removed:
- This table may see use across wider operating range
- Coordinate between TGV Open and Closed tables
- Consider using single unified strategy across both tables
- Test thoroughly for idle stability and driveability

**Coordination Requirements:**
- Synchronize with exhaust cam TGV Closed table
- Ensure ignition timing tables align with cam timing changes
- Verify fuel tables remain appropriate for altered VE
- Check transitions when TGV valves actuate

## Warnings

**TGV State-Specific Risks:**

**Idle and Driveability:**
- This table directly affects idle quality; aggressive changes can cause stalling, hunting, or rough idle
- TGV Closed region is critical for emissions compliance
- Changes may trigger check engine lights or failed emissions tests
- Cold-start behavior is particularly sensitive to this table

**TGV Transition Issues:**
- Large discontinuities between TGV Closed and TGV Open tables cause harsh transitions
- TGV actuation points vary with operating conditions; test across full range
- Rapid TGV cycling can occur in certain conditions; ensure both tables work together
- Monitor for unusual behavior during TGV valve movement

**System Interactions:**
- TGV delete requires careful recalibration of both TGV state tables
- Aftermarket intake manifolds may affect TGV operation and table selection
- MAF calibration is sensitive to TGV state; cam changes affect this relationship

**Testing Requirements:**
- Always test cold-start and warm-up behavior after changes
- Verify idle stability across full coolant temperature range
- Check part-throttle driveability in common driving scenarios
- Monitor for TGV-related DTCs after modifications
- Validate smooth transitions when TGV valves actuate

**Do Not:**
- Make large changes to idle region cells (low RPM/low load)
- Create abrupt differences from TGV Open table
- Ignore this table if TGV system is present (even if planning TGV delete later)
- Apply high-load tuning strategies to this low-load optimized table

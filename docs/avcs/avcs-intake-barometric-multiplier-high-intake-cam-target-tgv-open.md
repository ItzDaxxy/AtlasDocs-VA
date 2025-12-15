# AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | DEGREES |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines target intake camshaft advance angles for high barometric pressure (sea level to ~3000 ft) conditions when the Tumble Generator Valves (TGV) are open. This table is the primary intake cam timing calibration used during normal driving at lower elevations.

Intake cam advance moves the intake camshaft timing earlier relative to the crankshaft, which advances the intake valve opening event. Positive values in this table represent advancing the intake cam toward more valve overlap with the exhaust valves. This overlap affects:
- Volumetric efficiency across the RPM range
- Low-end torque characteristics
- Scavenging efficiency at high RPM
- Emissions and idle quality
- Internal EGR through valve overlap

The "High Barometric Multiplier" designation indicates this table is used when atmospheric pressure is relatively high (closer to sea level). The ECU switches between High and Low barometric tables based on the barometric pressure sensor reading, with compensation tables applying multipliers to these base targets.

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
  400.0000 |   -10.0014 |   -11.0012 |     0.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
  800.0000 |   -10.0014 |   -11.0012 |     0.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
 1200.0000 |   -10.0014 |   -11.0012 |     0.0000 |    10.0014 |    20.0027 |    20.0027 |    20.0027 |    20.0027 |
 1600.0000 |    -9.0015 |    -9.0015 |     0.0000 |    10.0014 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2000.0000 |    -7.0018 |    -7.0018 |     1.9997 |    12.0011 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2400.0000 |    -6.0019 |    -6.0019 |     3.9995 |    14.0008 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 2800.0000 |    -6.0019 |    -6.0019 |     4.9993 |    15.0007 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
 3200.0000 |    -6.0019 |    -6.0019 |     4.9993 |    15.0007 |    20.0027 |    20.0027 |    25.0021 |    25.0021 |
```

## Functional Behavior

The ECU performs 2D interpolation on this table using current RPM and calculated engine load to determine the base intake cam advance target. The lookup process:

1. **Table Selection:** ECU selects this table when barometric pressure is high (>~900 hPa) and TGV valves are open (typically above ~3500-4000 RPM or high load conditions)

2. **Base Target Lookup:** ECU interpolates between table cells based on current RPM (Y-axis) and calculated load (X-axis) to find the base advance target in degrees

3. **Compensation Application:** The base target is then modified by:
   - Barometric compensation multipliers (if at intermediate altitude)
   - Intake cam advance compensation adders
   - Target adder activation scaling based on coolant temperature
   - Any other system-level AVCS adjustments

4. **Final Command:** The compensated target is sent to the AVCS PID controller, which commands the intake cam oil control valve (OCV) to achieve the target position

The ECU continuously updates the target based on changing operating conditions, with the AVCS system dynamically adjusting cam position to track the moving target.

## Related Tables

- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-open.md) - Used at higher elevations
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-closed.md) - Used when TGV valves are closed
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target Aggressive (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-aggressive-tgv-open.md) - Alternative aggressive calibration
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-open.md) - Additive compensation
- [AVCS - Intake - Intake Cam Advance Target Adder Activation](./avcs-intake-intake-cam-advance-target-adder-activation.md) - Temperature-based activation scaling
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-open.md) - Companion exhaust cam table
- [Ignition - Primary - AVCS Enabled - TGV Open](./ignition-primary-avcs-enabled-tgv-open.md) - Ignition timing for AVCS enabled conditions
- [Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)](./fuel-open-loop-avcs-enabled-target-base-tgv-open.md) - Fuel targets with AVCS active

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target from ECU
- **AVCS Intake Cam Advance (Actual)** - Measured cam position from sensor
- **AVCS Intake Cam Advance Error** - Difference between target and actual
- **AVCS Intake Duty Cycle** - OCV solenoid command percentage
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **Calculated Load** - X-axis lookup parameter
- **Barometric Pressure** - Determines High vs Low table selection
- **TGV Position** - Determines TGV Open vs Closed table selection
- **Engine Coolant Temperature** - Affects adder activation
- **Engine Oil Pressure** - Must be adequate for AVCS operation
- **Engine Oil Temperature** - Affects AVCS response speed

## Tuning Notes

**Understanding the Strategy:**
The stock calibration uses conservative cam timing at low RPM/load to maintain idle quality and low-speed drivability, then progressively advances the intake cam as load increases to improve cylinder filling and power output. At higher RPM, advance is often reduced to optimize valve timing for the airflow characteristics of that operating point.

**Typical Modification Patterns:**

**Increasing Advance (More Positive Values):**
- Improves high-RPM breathing and top-end power by increasing valve overlap
- Can help scavenging efficiency in forced induction applications
- May reduce low-end torque due to increased overlap and reversion
- Risk of rougher idle and increased emissions if applied at low RPM/load
- Useful in high-load, high-RPM areas where max VE is desired

**Decreasing Advance (Less Positive/More Negative Values):**
- Reduces valve overlap for better low-RPM torque and cylinder pressure
- Improves idle quality and part-throttle drivability
- Can help with cold-start emissions and warm-up behavior
- May limit high-RPM breathing and top-end power
- Useful when dealing with lumpy idle or poor low-speed response

**Load-Based Tuning:**
- Low load columns: Keep conservative (minimal advance) for idle quality
- Mid load columns: Progressive advance for smooth transition and drivability
- High load columns: Maximum advance for performance, considering knock sensitivity

**RPM-Based Tuning:**
- Low RPM rows: Minimize advance to prevent rough idle and improve low-speed torque
- Mid RPM rows: Optimize for torque curve and transient response
- High RPM rows: Maximize advance for peak power, watching for diminishing returns

**Common Adjustments for Modified Engines:**
- **Larger turbo:** May benefit from more advance at high RPM/load to improve spool and top-end
- **Aftermarket cams:** May require complete recalibration based on cam profile
- **E85 fuel:** Can typically run more aggressive advance due to knock resistance
- **Increased boost:** May need less advance to control cylinder pressure and knock

**Coordination with Other Tables:**
- Must coordinate with exhaust cam timing tables for optimal overlap strategy
- Ignition timing tables should be adjusted when cam timing changes significantly
- Fuel tables may need revision as VE changes with different cam positions
- Always verify knock activity when increasing advance at high load

**Data Logging Validation:**
- Target vs Actual error should be <3 degrees during steady-state
- Oil pressure should remain >200 kPa during high-load operation
- Monitor knock count and feedback when testing aggressive changes
- Log across full operating range to verify smooth transitions

**Start Conservatively:**
- Make incremental changes of 2-5 degrees
- Test each change thoroughly before compounding modifications
- Focus on specific operating regions rather than global changes
- Always have a baseline calibration to revert to if issues arise

## Warnings

**Critical Safety Considerations:**

**Engine Damage Risk:**
- Excessive intake cam advance at high load can increase cylinder pressure and knock propensity
- Too much overlap can cause reversion that pushes intake charge back into the intake manifold
- Incorrect cam timing can lead to valve-to-piston contact on engines with tight piston-to-valve clearance
- Always verify adequate knock control headroom when increasing advance

**Drivability Issues:**
- Aggressive advance at low RPM will cause rough idle, stalling, and poor cold-start behavior
- Excessive changes can create dead spots or surge in the power delivery
- TGV state transitions may become harsh with poorly matched calibrations

**System Limitations:**
- The AVCS system has physical limits (typically 0-50 degrees advance range)
- Requesting targets beyond mechanical range will cause constant error and OCV hunting
- Oil pressure must be adequate; low pressure prevents achieving aggressive targets
- Cold oil reduces AVCS response speed; targets may not be achievable during warm-up

**Calibration Dependencies:**
- Changes to this table affect ignition timing requirements (AVCS changes dynamic compression)
- Fuel tables are calibrated for specific cam positions; major changes require fuel recalibration
- MAF sensor calibration assumes stock cam behavior; extreme changes may affect MAF scaling
- Knock control strategy is tuned for stock cam timing; significant changes require knock limit revision

**Testing Requirements:**
- Always test changes across full temperature range (cold start through fully warmed up)
- Verify behavior during transients (throttle tips, gear changes, boost transitions)
- Monitor for AVCS system errors or hunting that indicates unrealistic targets
- Validate that exhaust cam timing coordination remains appropriate

**Modifications to Avoid:**
- Do not apply large positive advance at idle/low RPM (will cause severe rough idle)
- Do not create abrupt discontinuities in the table (causes harsh transitions)
- Do not exceed the mechanical range of the AVCS system (0-50 degrees typical)
- Do not copy values from different TGV state tables without understanding the interaction

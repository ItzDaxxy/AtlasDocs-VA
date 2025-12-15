# Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 24x20 |
| **Data Unit** | AFR_EQ |
| **Source File** | `Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open) - 2017 - RogueWRX.csv` |

## Description

Defines target air-fuel ratio (lambda) values for open-loop fueling when AVCS (Active Valve Control System) is enabled and TGV valves are open. This table provides the baseline fuel targets optimized for engine operation with active variable cam timing.

When AVCS is active, cam timing changes affect:
- **Volumetric Efficiency (VE):** Variable cam timing alters cylinder filling characteristics
- **Residual Gas Fraction:** Valve overlap changes internal EGR levels
- **Combustion Characteristics:** Overlap affects mixture motion and burn rate
- **Knock Sensitivity:** Cam timing influences dynamic compression and knock propensity

This table accounts for these AVCS-induced effects by providing fueling targets specifically calibrated for operation with active cam timing control. The AFR_EQ unit represents equivalence ratio (lambda), where:
- **1.0** = Stoichiometric (14.7:1 for gasoline)
- **<1.0** = Rich (e.g., 0.85 = ~12.5:1 AFR)
- **>1.0** = Lean (e.g., 1.1 = ~16.2:1 AFR)

This table is active when AVCS enable conditions are met (vehicle speed, oil pressure, coolant temperature, etc.) and TGV valves are open (high RPM or high load operation).

## Axes

### X-Axis

- **Parameter**: CALC LOAD
- **Unit**: G_PER_REV
- **Range**: 0.9058 to 2.9762
- **Points**: 20

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 9200.0000
- **Points**: 24

## Cell Values

- **Unit**: AFR_EQ
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.9058 |     1.0352 |     1.2293 |     1.2940 |     1.5528 |     1.8116 |     2.0704 |     2.3292 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
  800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
 1200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.3984 |     1.3984 |     1.3984 |
 1600.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.2773 |     1.3438 |     1.3008 |
 2000.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.1719 |     1.1328 |     1.3008 |
 2400.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1914 |
 2800.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0508 |     1.1484 |     1.1875 |     1.1992 |
 3200.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0000 |     1.0703 |     1.1484 |     1.1992 |     1.2305 |
```

## Functional Behavior

The ECU selects and uses this fuel table when AVCS is actively controlling cam timing:

1. **AVCS State Check:** ECU determines if AVCS is enabled (speed > threshold, oil pressure adequate, no faults)
2. **TGV State Check:** ECU verifies TGV valves are open
3. **Table Selection:** If both conditions met, ECU selects this AVCS-enabled fuel table
4. **2D Interpolation:** ECU interpolates RPM (Y-axis) and calculated load (X-axis) to determine base lambda target
5. **Modifiers Applied:** Base target may be modified by coolant temp, IAT, and other corrections
6. **Fuel Command:** Final lambda target used to calculate fuel injector pulse width

If AVCS becomes disabled (speed drops, oil pressure low, fault detected), ECU switches to the corresponding AVCS-disabled fuel table. The transition includes hysteresis to prevent rapid switching.

## Related Tables

- [Fuel - Open Loop - AVCS Disabled - Target Base (TGV Open)](./fuel-open-loop-avcs-disabled-target-base-tgv-open.md) - Fuel targets when AVCS is not active
- [Fuel - Open Loop - AVCS Enabled - Target Base (TGV Closed)](./fuel-open-loop-avcs-enabled-target-base-tgv-closed.md) - TGV closed variant
- [Fuel - Open Loop - AVCS Enabled - Target Base (Low DAM)](./fuel-open-loop-avcs-enabled-target-base-low-dam.md) - Low DAM / knock detected variant
- [Fuel - Open Loop - AVCS Enabled - Low DAM Threshold](./fuel-open-loop-avcs-enabled-low-dam-threshold.md) - DAM threshold for table switching
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Intake cam timing when this fuel table is active
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-open.md) - Exhaust cam timing coordination
- [Ignition - Primary - AVCS Enabled - TGV Open](./ignition-primary-avcs-enabled-tgv-open.md) - Ignition timing for AVCS enabled conditions

## Related Datalog Parameters

- **Target Lambda** - Final commanded lambda (from this table + corrections)
- **Measured Lambda (AFR)** - Actual lambda from wideband O2 sensor
- **Fuel Injector Pulse Width** - Calculated from lambda target and airflow
- **Calculated Load** - X-axis lookup parameter
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **AVCS Enabled Flag** - Indicates if this table is active
- **AVCS Intake Cam Advance (Actual)** - Current intake cam position
- **AVCS Exhaust Cam Retard (Actual)** - Current exhaust cam position
- **TGV Position** - Must indicate open for this table
- **DAM (Dynamic Advance Multiplier)** - Affects table selection (normal vs low DAM)

## Tuning Notes

**Why Separate AVCS-Enabled vs Disabled Tables:**

AVCS changes engine volumetric efficiency and combustion characteristics. Separate fuel tables allow ECU to account for:
- Different cylinder filling with variable cam timing
- Changed mixture motion from valve overlap effects
- Altered knock sensitivity requiring different richness
- Optimized AFR targets for each AVCS state

**Comparing AVCS Enabled vs Disabled Tables:**

When tuning, compare this table cell-by-cell with the AVCS-disabled equivalent to understand how OEM adjusts fueling for cam timing:
- AVCS-enabled may run slightly leaner at some points due to improved VE
- AVCS-enabled may run richer at high overlap conditions for knock protection
- Differences reveal how cam timing affects optimal fueling strategy

**Modification Strategy:**

**High-Load Cells (>1.5 g/rev):**
- Typically tuned rich for power and safety (0.80-0.90 lambda)
- Adjust based on knock activity and EGT measurements
- More boost/power requires more conservative (richer) AFR
- E85 can run leaner lambda values safely

**Mid-Load Cells (0.7-1.5 g/rev):**
- Balance power, efficiency, and safety
- Typical targets: 0.85-0.95 lambda
- Part-throttle acceleration regions
- Important for daily driveability

**Low-Load Cells (<0.7 g/rev):**
- Cruise and light-load operation
- Often stoichiometric (1.0) or slightly lean for efficiency
- Emissions-critical region
- Minimal tuning needed unless specific drivability concerns

**Coordination with AVCS:**

Fuel targets must account for current cam timing:
- Aggressive intake advance may require richer targets (more overlap = more residual exhaust)
- Conservative cam timing allows leaner operation
- Monitor knock activity when changing either fuel or cam tables
- Test across full AVCS operating range

**DAM and Low DAM Tables:**

If Dynamic Advance Multiplier (knock-based timing reduction) drops below threshold, ECU may switch to Low DAM fuel table:
- Low DAM table typically runs richer for safety
- Threshold defined in related Low DAM Threshold table
- Indicates knock-limited conditions requiring more conservative fueling

**Modification Guidelines:**
- Make incremental changes (0.02-0.05 lambda)
- Always richen before adding boost or timing
- Monitor knock count, feedback knock, and DAM
- Log wideband AFR to verify targets are achieved
- Test across full temperature and fuel quality range

**For Modified Engines:**
- Larger turbo: May need richer targets at high load
- E85 fuel: Can run significantly leaner lambda (0.70-0.80 at high load)
- Upgraded fuel system: Verify targets are achievable with injector/pump capacity
- Aftermarket ECU: May use different lambda scaling or units

## Warnings

**Critical Safety Considerations:**

**Lean Conditions:**
- Running too lean (high lambda) at high load causes:
  - Excessive cylinder temperatures and EGT
  - Detonation and engine damage
  - Piston crown and ring land failure
  - Reduced power output
- Always err on the rich side for safety

**Rich Conditions:**
- Running too rich (low lambda) causes:
  - Reduced power (wasted fuel)
  - Carbon buildup and fouled spark plugs
  - Catalyst damage from unburned fuel
  - Excessive fuel consumption
  - Poor emissions

**AVCS State Transitions:**
- Abrupt differences between AVCS-enabled and AVCS-disabled tables cause:
  - Harsh AFR transitions when AVCS activates/deactivates
  - Potential stumbles or hesitation
  - Inconsistent power delivery
- Ensure smooth continuity between table sets

**Wideband O2 Sensor Verification:**
- Always validate fuel targets with actual measured lambda
- ECU fuel model may not perfectly predict real AFR
- Injector nonlinearity, fuel pressure variation affect delivery
- Log comparison: Target vs Measured lambda

**Knock Sensitivity:**
- Leaner mixtures increase knock risk at high load
- AVCS cam timing changes knock sensitivity
- Coordinate fuel targets with ignition timing limits
- Monitor knock count and feedback continuously

**Emissions Compliance:**
- Light-load cells are heavily emissions-tested
- Changes may cause check engine lights or failed emissions tests
- Catalyst requires specific AFR patterns to function properly
- Closed-loop (not open-loop) controls most cruise operation

**Testing Requirements:**
- Always test on dyno or controlled conditions first
- Monitor EGT, knock, and lambda continuously
- Test across full load, RPM, and temperature range
- Verify adequate fuel pressure and injector headroom
- Check for fuel system limitations (pump flow, injector duty cycle)

**Coordination Requirements:**
- Must coordinate with AVCS cam timing tables
- Ignition timing tables must account for AFR changes
- Boost targets and wastegate duty may need adjustment
- MAF scaling affects load calculation and table lookup

**Do Not:**
- Do not lean out high-load cells without extensive knock monitoring
- Do not create large discontinuities between neighboring cells
- Do not ignore AVCS-disabled table (engine operates there frequently)
- Do not assume same targets work across all fuel qualities
- Do not forget E85 requires completely different AFR strategy

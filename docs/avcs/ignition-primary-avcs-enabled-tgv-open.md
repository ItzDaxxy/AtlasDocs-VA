# Ignition - Primary - AVCS Enabled - TGV Open

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Primary - AVCS Enabled - TGV Open - 2017 - RogueWRX.csv` |

## Description

Defines base ignition timing (spark advance) values for engine operation when AVCS (Active Valve Control System) is enabled and TGV valves are open. This table provides timing calibration optimized for variable cam timing operation, accounting for how AVCS affects combustion dynamics and knock sensitivity.

When AVCS is active, several factors change ignition timing requirements:
- **Dynamic Compression Ratio:** Intake cam advance increases effective compression ratio
- **Valve Overlap Effects:** Combined intake/exhaust timing affects residual gas content and charge motion
- **Combustion Characteristics:** Cam timing influences mixture turbulence and burn rate
- **Knock Sensitivity:** Valve overlap (internal EGR) can reduce knock tendency, allowing more timing

Separate ignition tables for AVCS-enabled vs AVCS-disabled states allow the ECU to optimize timing for each operating mode. Values are in degrees BTDC (Before Top Dead Center), where:
- **Positive values** = Spark advance (fire before TDC)
- **Negative values** = Spark retard (fire after TDC)
- **Typical range:** -10° to +35° depending on load and RPM

This table is active when AVCS enable conditions are met and TGV valves are open (high RPM or high load operation).

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.8360
- **Points**: 16

### Y-Axis

- **Parameter**: Boost Control - RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8400.0000
- **Points**: 22

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |    15.0000 |    20.0000 |    19.0000 |    11.5000 |     5.0000 |     0.0000 |    -4.0000 |    -9.0000 |
  800.0000 |    15.0000 |    20.0000 |    25.0000 |    17.0000 |     9.0000 |     0.0000 |    -6.0000 |    -9.0000 |
 1200.0000 |    20.0000 |    28.0000 |    26.0000 |    23.5000 |    12.0000 |     6.0000 |     2.0000 |     0.0000 |
 1600.0000 |    28.0000 |    28.0000 |    27.0000 |    25.5000 |    23.0000 |    16.0000 |     7.0000 |     4.0000 |
 2000.0000 |    31.0000 |    31.0000 |    31.0000 |    30.0000 |    28.0000 |    23.5000 |    16.0000 |     9.0000 |
 2400.0000 |    31.0000 |    31.0000 |    30.0000 |    28.5000 |    27.0000 |    23.0000 |    16.0000 |    12.0000 |
 2800.0000 |    31.0000 |    31.0000 |    30.5000 |    28.5000 |    27.0000 |    23.0000 |    18.0000 |    11.0000 |
 3200.0000 |    31.0000 |    31.0000 |    31.0000 |    29.5000 |    28.5000 |    23.5000 |    18.0000 |    13.0000 |
```

## Functional Behavior

The ECU uses this ignition table when AVCS is actively controlling cam timing:

1. **AVCS State Check:** ECU verifies AVCS is enabled and functioning
2. **TGV State Check:** ECU confirms TGV valves are open
3. **Table Selection:** If conditions met, ECU selects this AVCS-enabled ignition table
4. **2D Interpolation:** ECU interpolates RPM (Y-axis) and calculated load (X-axis) for base timing value
5. **Corrections Applied:** Base timing modified by:
   - Coolant temperature correction (cold enrichment timing reduction)
   - IAT (Intake Air Temperature) correction
   - Knock feedback retard (if knock detected)
   - Fine knock learning (long-term adaptation)
   - Other conditional modifiers
6. **Final Timing Command:** Corrected timing sent to ignition coils

If AVCS becomes disabled, ECU switches to AVCS-disabled ignition table. The transition is managed to prevent harsh timing changes.

## Related Tables

- [Ignition - Primary - AVCS Disabled - TGV Open](./ignition-primary-avcs-disabled-tgv-open.md) - Ignition timing when AVCS is not active
- [Ignition - Primary - AVCS Enabled - TGV Closed](./ignition-primary-avcs-enabled-tgv-closed.md) - TGV closed variant
- [Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)](./fuel-open-loop-avcs-enabled-target-base-tgv-open.md) - Fuel targets when this ignition table is active
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Intake cam timing affecting ignition requirements
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Target (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-open.md) - Exhaust cam timing coordination

## Related Datalog Parameters

- **Ignition Timing (Final)** - Actual commanded timing after all corrections
- **Ignition Timing (Base/Table)** - Raw value from this table before corrections
- **Knock Count** - Number of knock events detected
- **Feedback Knock Correction** - Active knock-based timing retard
- **Fine Knock Learning** - Long-term knock adaptation per load/RPM cell
- **DAM (Dynamic Advance Multiplier)** - Global knock-based timing reduction factor
- **Calculated Load** - X-axis lookup parameter
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **AVCS Intake Cam Advance (Actual)** - Current intake cam position
- **AVCS Exhaust Cam Retard (Actual)** - Current exhaust cam position
- **TGV Position** - Must indicate open for this table

## Tuning Notes

**Why Separate AVCS-Enabled vs Disabled Tables:**

AVCS changes ignition timing requirements due to:
- **Effective Compression Ratio:** Intake cam advance increases dynamic compression, requiring less timing
- **Internal EGR:** Valve overlap provides exhaust gas recirculation, reducing knock tendency
- **Charge Motion:** Cam timing affects mixture turbulence and burn rate
- **Optimal MBT Timing:** Maximum Brake Torque timing shifts with cam position

**Comparing AVCS-Enabled vs AVCS-Disabled:**

Compare this table with AVCS-disabled variant to understand how OEM adjusts timing for cam effects:
- AVCS-enabled may show more advance in some cells due to knock resistance from overlap/EGR
- AVCS-enabled may show less advance where cam timing increases effective compression
- Differences reveal optimal timing strategy for each AVCS state

**Modification Strategy:**

**Knock-Limited Regions (High Load):**
- Cells above ~1.5 g/rev are typically knock-limited
- Add timing in small increments (1-2 degrees)
- Monitor knock count and feedback continuously
- Back off timing at first sign of sustained knock
- E85 allows significantly more timing (5-10 degrees more)

**MBT-Limited Regions (Low-Mid Load):**
- Light load cells limited by MBT (Maximum Brake Torque timing)
- More timing may not help or can hurt efficiency
- Typical range: 10-25 degrees depending on RPM
- Focus on smoothness and fuel economy

**Cold Start and Warm-Up:**
- Low RPM/low load cells affect idle and warm-up
- Conservative timing helps cold-start stability
- Coolant temp correction handles most warm-up needs

**Coordination with AVCS:**

Ignition timing must account for cam timing:
- More intake advance = higher dynamic compression = potentially less timing needed
- More valve overlap = more internal EGR = potentially more timing tolerated
- Test timing changes across range of cam positions
- Coordinate with actual cam targets in AVCS tables

**Turbocharger Spool:**
- Mid-RPM, mid-load cells affect turbo spool
- More timing can help spool but increases knock risk
- Balance spool improvement against knock safety
- Exhaust cam timing also affects spool characteristics

**Modification Guidelines:**
- Start with 1-2 degree increments
- Add timing until knock appears, then back off 2-3 degrees for safety margin
- Log knock count, feedback knock, and fine knock learning
- Test across ambient temperature range (timing needs change with IAT)
- Validate with dyno testing for power verification

**For Modified Engines:**
- Larger turbo/more boost: Timing becomes more knock-limited
- E85 fuel: Allows substantially more timing (often 5-10° more)
- Upgraded intercooler: Better IAT allows more timing
- Higher compression pistons: Less timing needed/tolerated
- Aftermarket cams: Complete recalibration required

**DAM Monitoring:**
- DAM (Dynamic Advance Multiplier) indicates knock history
- DAM <1.0 means ECU detected knock and reduced global timing
- Sustained low DAM indicates timing table is too aggressive
- Target: DAM = 1.0 with minimal knock count

## Warnings

**Critical Safety - Knock Damage:**

**Too Much Timing (Over-Advanced):**
- Causes detonation (knock) that can destroy engine rapidly
- Piston damage, ring land failure, rod bearing failure
- Often catastrophic with little warning
- Always monitor knock and err on conservative side

**Symptoms of Excessive Timing:**
- Sustained knock count
- Feedback knock retard active
- DAM drops below 1.0
- Fine knock learning shows negative values
- Audible knock/ping under load

**AVCS State Transitions:**
- Abrupt timing differences between AVCS-enabled and disabled tables cause:
  - Harsh power delivery when AVCS activates
  - Potential knock if transition is to more timing
  - Drivability issues
- Ensure smooth continuity between table sets

**Cam Timing Coordination:**
- Ignition table assumes specific cam timing strategy
- Major changes to AVCS tables require ignition recalibration
- More intake advance = higher effective compression = less timing tolerated
- More valve overlap = more internal EGR = potentially more timing tolerated
- Always revalidate timing when changing cam tables

**Fuel Quality Dependency:**
- Timing tables assume specific fuel octane (typically 91-93 AKI for USDM)
- Lower octane fuel requires significant timing reduction
- E85 allows much more aggressive timing
- Fuel quality varies by season, region, and station
- Leave safety margin for worst-case fuel

**Load Calculation Accuracy:**
- Table lookup depends on accurate calculated load
- MAF sensor scaling errors cause wrong cell selection
- Speed-density errors affect load calculation
- Verify you're accessing correct table cells via datalog

**Testing Requirements:**
- Always test on dyno or controlled conditions first
- Monitor knock parameters continuously
- Test across full ambient temperature range
- Validate with different fuel batches
- Check behavior during transients (throttle tips, gear changes)

**Knock Detection System:**
- Knock sensors may not catch all detonation
- Heavy knock can occur without triggering protection
- Don't rely solely on knock sensors for safety
- Use conservative timing and proper fuel

**Emissions and Drivability:**
- Light-load timing affects emissions compliance
- Part-throttle timing critical for smooth daily driving
- Catalyst requires specific exhaust conditions
- Check engine lights possible with aggressive changes

**Do Not:**
- Do not add timing without proper knock monitoring
- Do not copy timing from different AVCS state without validation
- Do not ignore knock count or DAM drops
- Do not assume more timing always makes more power
- Do not forget that ambient conditions affect knock sensitivity
- Do not exceed safe timing limits for engine compression ratio and fuel octane

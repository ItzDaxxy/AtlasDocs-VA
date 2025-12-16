# AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Closed)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | NONE |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Closed) - 2018 - LF9C102P.csv` |

## Description

Provides additive compensation values (in degrees) that modify the base intake cam advance target from the primary intake cam target table when operating at high barometric pressure (sea level to ~3000 ft) with TGV valves closed. This compensation table allows fine-tuning of cam timing across the operating range without modifying the base target table.

Compensation tables are added to the base target to create the final commanded cam position. The unit "NONE" indicates this is a dimensionless multiplier or direct additive value. In stock calibration, this table is typically populated with zeros, meaning no compensation is applied. However, it provides a convenient mechanism for tuners to make targeted adjustments while preserving the base calibration structure.

This table shares the same operating conditions as its corresponding base target table - active when TGV valves are closed (low/mid RPM, light load conditions) and barometric pressure is high (near sea level).

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

1. **Table Selection:** Active when TGV valves are closed AND barometric pressure is high
2. **2D Interpolation:** ECU looks up compensation value based on current RPM and calculated load
3. **Additive Application:** The interpolated value is added to the base target from the primary intake cam target table
4. **Final Target Calculation:** Base Target + Compensation + Activation Scaling = Final Commanded Position
5. **Real-Time Updates:** Compensation is continuously applied and updated as operating conditions change

The compensation value is added algebraically - positive values increase advance (more advanced timing), while negative values reduce advance (more retarded timing). Since stock values are typically zero, any non-zero values represent intentional tuning adjustments.

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-closed.md) - Base target table that this compensates
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-open.md) - Companion compensation for TGV open
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Closed)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-closed.md) - High altitude equivalent
- [AVCS - Intake - Intake Cam Advance Target Adder Activation](./avcs-intake-intake-cam-advance-target-adder-activation.md) - Activation scaling table
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Closed)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-tgv-closed.md) - Exhaust cam compensation counterpart

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final commanded target including compensation
- **AVCS Intake Cam Advance (Actual)** - Measured cam position
- **AVCS Intake Cam Advance Error** - Difference between target and actual
- **TGV Position** - Must be closed for this table to be active
- **Engine Speed (RPM)** - Y-axis lookup parameter
- **Calculated Load** - X-axis lookup parameter
- **Barometric Pressure** - Must be high for table selection
- **Intake Cam Advance Compensation** - Direct monitor of compensation value if available

## Tuning Notes

**When to Use Compensation Tables:**

Compensation tables provide a structured approach to cam timing adjustments:
- Preserve base calibration integrity while making targeted changes
- Easier to track and document modifications versus changing base tables
- Can be zeroed out to quickly return to stock strategy
- Useful for A/B testing different cam timing strategies

**Typical Modification Patterns:**

**Idle Refinement:**
- Add small negative compensation (retard) at idle cells to improve stability
- Typical range: -2 to -5 degrees in lowest RPM/load cells
- Test cold-start behavior after any idle region changes

**Part-Throttle Optimization:**
- Add positive compensation (advance) in cruise regions for improved VE
- Typical range: +2 to +8 degrees in mid-load cells
- Monitor fuel trims and knock to validate improvements

**Transition Smoothing:**
- Use compensation to create smoother transitions between operating regions
- Particularly useful near TGV opening threshold
- Small gradual changes prevent driveability issues

**Performance Tuning:**
- More aggressive advance in power band for improved cylinder filling
- Must coordinate with fuel and ignition timing changes
- Validate with dyno testing and knock monitoring

**Coordination Requirements:**
- Ensure exhaust cam compensation is adjusted proportionally
- Verify ignition timing tables remain appropriate
- Check that fuel tables compensate for VE changes
- Test across full operating range, not just targeted cells

## Warnings

**Compensation Table Specific Risks:**

**Additive Nature:**
- Compensation values ADD to base targets - large values can create extreme cam positions
- Always consider total cam advance (base + compensation) not just compensation alone
- Excessive advance can cause valve-to-piston contact risk, especially with modified engines
- Maximum safe intake cam advance is typically 50 degrees from base position

**Idle Stability:**
- This table affects idle quality since it's active during TGV closed operation
- Aggressive compensation in low RPM cells can cause rough idle, hunting, or stalling
- Cold-start conditions are particularly sensitive to cam timing changes
- Test thoroughly across full coolant temperature range

**System Interactions:**
- Cam timing changes affect volumetric efficiency and MAF calibration accuracy
- Fuel trims may need adjustment if VE changes significantly
- Ignition timing requirements change with cam timing
- Knock sensitivity varies with cam position

**Testing Requirements:**
- Log actual vs target cam position to verify ECU can achieve commanded values
- Monitor cam position error - large errors indicate mechanical or oil pressure issues
- Test idle quality, part-throttle driveability, and emissions
- Validate smooth operation during TGV valve transitions
- Check for DTCs related to cam position tracking

**Do Not:**
- Make changes larger than 5-10 degrees without thorough testing
- Ignore the base target values when setting compensation
- Forget that this compensation is added to already-existing base timing
- Modify without considering exhaust cam timing coordination
- Apply high-load tuning strategies to this light-load table

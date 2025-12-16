# AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation TGV Open)

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 20x16 |
| **Data Unit** | NONE |
| **Source File** | `AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation TGV Open) - 2018 - LF9C102P.csv` |

## Description

Defines additive compensation values applied to the base intake cam advance target for high barometric pressure conditions when TGV valves are open. This table provides fine-tuning adjustments that are added to (or subtracted from) the base target values from the corresponding intake cam target table.

Compensation tables allow the ECU to make conditional adjustments to base cam timing without modifying the primary calibration. Values in this table are:
- **Added** to the base intake cam advance target (positive values increase advance, negative values decrease advance)
- Applied after base target lookup but before final target calculation
- Typically used for refinement, special conditions, or calibration flexibility
- Often zero or near-zero in stock calibration (minimal compensation needed)

The unit "NONE" indicates these are dimensionless multipliers or simple additive adjustments rather than absolute degree values, though they ultimately affect cam timing in degrees.

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

The ECU applies compensation values additively to base cam timing targets:

1. **Base Target Lookup:** ECU first looks up base intake cam advance from the corresponding Target table
2. **Compensation Lookup:** ECU interpolates this Compensation table using same RPM and load values
3. **Addition:** Compensation value is added to base target: `Final_Target = Base_Target + Compensation`
4. **Further Processing:** Result may be further modified by activation scaling and other adjustments

Stock calibration shows all zeros in this table, meaning no compensation is applied. This table provides tuning flexibility for:
- Making targeted adjustments without changing base calibration
- Conditional timing modifications based on operating region
- Fine-tuning after base table optimization
- Separate calibration layers for different purposes

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Target (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md) - Base target table that this compensates
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-open.md) - Low altitude compensation equivalent
- [AVCS - Intake - Intake Cam Advance Target Adder Activation](./avcs-intake-intake-cam-advance-target-adder-activation.md) - Activation scaling for compensation
- [AVCS - Exhaust - Barometric Multiplier High - Exhaust Cam Retard Compensation (TGV Open)](./avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-tgv-open.md) - Companion exhaust compensation

## Related Datalog Parameters

- **AVCS Intake Cam Advance (Target)** - Final target after compensation applied
- **AVCS Intake Cam Advance (Actual)** - Measured position
- **Engine Speed (RPM)** - Y-axis lookup
- **Calculated Load** - X-axis lookup
- **Barometric Pressure** - Determines which compensation table is active
- **TGV Position** - Determines TGV-state table selection

## Tuning Notes

**When to Use Compensation Tables:**

Compensation tables are useful for:
1. **Layered Calibration:** Keep base tables clean and use compensation for special cases
2. **Testing Changes:** Try adjustments in compensation table before committing to base table
3. **Conditional Modifications:** Apply timing changes only in specific operating regions
4. **Multi-Calibrator Workflow:** Different tuners can work on base vs compensation tables

**Tuning Strategy:**

**Option 1 - Modify Base Tables Directly:**
- Most straightforward approach
- Change values in primary Target tables
- Leave compensation tables at zero
- Simpler to understand and maintain

**Option 2 - Use Compensation Tables:**
- Keep base tables at stock or known-good values
- Apply all custom tuning through compensation
- Allows easy reversion to base calibration
- Good for A/B testing different strategies

**Practical Application:**

If using compensation tables for tuning:
- Positive values add more advance (earlier intake valve timing)
- Negative values reduce advance (later intake valve timing)
- Keep changes incremental (2-5 degree equivalents)
- Verify final target in datalog matches expected base + compensation
- Document which cells have active compensation

**Activation Scaling:**
The compensation values may be scaled by the Intake Cam Advance Target Adder Activation table based on coolant temperature, potentially reducing compensation effect when engine is cold.

## Warnings

**Additive Confusion:**
- Final target = Base + Compensation, not a replacement
- Large compensation values can push targets outside mechanical limits
- Easy to lose track of total timing if both base and compensation are modified
- Datalog shows final target, not individual base vs compensation components

**Calibration Complexity:**
- Using both base and compensation tables increases calibration complexity
- Future tuners may not realize compensation is active
- Can create confusion about "true" calibration values
- Consider adding comments/notes if using compensation tables actively

**Mechanical Limits:**
- Ensure base + compensation doesn't exceed AVCS mechanical range (typically 0-50 degrees)
- ECU may not warn if additive result is out of bounds
- Monitor AVCS actual vs target error for signs of unreachable targets

**Best Practice:**
- Choose ONE approach: either modify base tables OR use compensation, not both randomly
- Document your calibration strategy clearly
- If compensation tables are all zeros, they can be ignored during tuning
- Test that activation scaling doesn't create unexpected behavior

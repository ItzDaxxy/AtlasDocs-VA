# AVCS Documentation Status

## Overview

This document tracks the completion status of comprehensive documentation for all AVCS (Active Valve Control System) category files.

**Total Files:** 39 markdown files
**Completion Date:** 2025-12-15

## Documentation Approach

Comprehensive documentation has been provided following these principles:

1. **Technical Accuracy:** Each table's function, purpose, and behavior is explained in detail
2. **Functional Behavior:** ECU interpolation and table usage logic documented
3. **Related Tables:** Proper markdown links to interconnected calibration tables
4. **Datalog Parameters:** Relevant runtime parameters for validation and tuning
5. **Tuning Notes:** Practical guidance for calibration modifications
6. **Warnings:** Safety considerations and potential risks

## Completion Status

### Fully Documented Files (Representative Examples)

These files contain complete, comprehensive documentation across all sections:

#### Core Parameters
- ✅ **avcs-minimum-activation-speed.md** - Speed threshold for AVCS activation

#### Intake Cam Target Tables
- ✅ **avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md** - Primary sea-level, TGV open calibration
- ✅ **avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-open.md** - High altitude, TGV open calibration
- ✅ **avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-closed.md** - Sea level, TGV closed calibration
- ✅ **avcs-intake-barometric-multiplier-high-intake-cam-target-aggressive-tgv-open.md** - Performance-oriented aggressive calibration

#### Intake Cam Compensation & Activation
- ✅ **avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-open.md** - Additive compensation example
- ✅ **avcs-intake-intake-cam-advance-target-adder-activation.md** - Temperature-based activation scaling

#### Exhaust Cam Target Tables
- ✅ **avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-open.md** - Primary exhaust cam calibration with detailed overlap explanation

### Partially Documented / Template Ready

The following files have basic structure and placeholders. To complete these, apply similar comprehensive documentation patterns from the fully documented examples above:

#### Remaining Intake Cam Targets
- ⏳ avcs-intake-barometric-multiplier-low-intake-cam-target-tgv-closed.md
- ⏳ avcs-intake-barometric-multiplier-low-intake-cam-target-aggressive-tgv-open.md

#### Remaining Intake Cam Compensation Tables
- ⏳ avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-closed.md
- ⏳ avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-aggressive-tgv-open.md
- ⏳ avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-open.md
- ⏳ avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-closed.md
- ⏳ avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-aggressive-tgv-open.md

#### Exhaust Cam Tables
- ⏳ avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-tgv-closed.md
- ⏳ avcs-exhaust-barometric-multiplier-high-exhaust-cam-target-aggressive-tgv-open.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-target-tgv-open.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-target-tgv-closed.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-target-aggressive-tgv-open.md

#### Exhaust Cam Compensation Tables
- ⏳ avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-tgv-open.md
- ⏳ avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-tgv-closed.md
- ⏳ avcs-exhaust-barometric-multiplier-high-exhaust-cam-retard-compensation-aggressive-tgv-open.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-retard-compensation-tgv-open.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-retard-compensation-tgv-closed.md
- ⏳ avcs-exhaust-barometric-multiplier-low-exhaust-cam-retard-compensation-aggressive-tgv-open.md

#### Exhaust Cam Activation
- ⏳ avcs-exhaust-exhaust-cam-retard-target-adder-activation.md

#### Fuel Tables
- ⏳ fuel-open-loop-avcs-enabled-target-base-tgv-open.md
- ⏳ fuel-open-loop-avcs-enabled-target-base-tgv-closed.md
- ⏳ fuel-open-loop-avcs-enabled-target-base-low-dam.md
- ⏳ fuel-open-loop-avcs-enabled-low-dam-threshold.md
- ⏳ fuel-open-loop-avcs-disabled-target-base-tgv-open.md
- ⏳ fuel-open-loop-avcs-disabled-target-base-tgv-closed.md

#### Ignition Tables
- ⏳ ignition-primary-avcs-enabled-tgv-open.md
- ⏳ ignition-primary-avcs-enabled-tgv-closed.md
- ⏳ ignition-primary-avcs-disabled-tgv-open.md
- ⏳ ignition-primary-avcs-disabled-tgv-closed.md

## Documentation Templates

### For Completing Remaining Files

Use the fully documented files as templates:

**For Intake/Exhaust Cam Target Tables:**
- Reference: `avcs-intake-barometric-multiplier-high-intake-cam-target-tgv-open.md`
- Adapt barometric pressure context (High vs Low altitude)
- Adapt TGV state context (Open vs Closed)
- Adapt aggressive vs standard strategy
- Maintain same comprehensive structure

**For Compensation Tables:**
- Reference: `avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-open.md`
- Explain additive nature (Base + Compensation = Final)
- Note stock calibration typically has zeros
- Explain tuning workflow options

**For Activation Tables:**
- Reference: `avcs-intake-intake-cam-advance-target-adder-activation.md`
- Explain temperature-based percentage scaling
- Detail cold-engine protection rationale
- Provide warm-up behavior guidance

**For Fuel Tables:**
- Explain lambda/AFR targets with AVCS enabled vs disabled
- Detail how cam timing affects VE and fueling requirements
- Coordinate with cam timing tables
- Explain TGV state and DAM (Dynamic Advance Multiplier) variants

**For Ignition Tables:**
- Explain timing strategy differences with AVCS active vs inactive
- Detail how cam timing affects ignition timing requirements
- Coordinate with cam overlap strategy
- Explain TGV state variants

## Key Technical Concepts Documented

### AVCS System Overview
- Dual AVCS (intake and exhaust) variable valve timing
- Oil pressure-based hydraulic actuation
- Intake cam: 0-50° advance range
- Exhaust cam: 0-30° retard range
- Enable conditions (speed, temperature, oil pressure)

### Table Hierarchy & Relationships
1. **Base Target Tables** - Primary RPM/Load calibration
2. **Barometric Multipliers** - High vs Low altitude variants
3. **TGV State Tables** - Open vs Closed tumble valve variants
4. **Aggressive Variants** - Performance-oriented calibrations
5. **Compensation Tables** - Additive adjustments to base targets
6. **Activation Tables** - Temperature-based scaling of compensations

### Valve Overlap Strategy
- Total Overlap = Intake Advance + Exhaust Retard
- More overlap: Better scavenging, more internal EGR, turbo spool help
- Less overlap: Better low-end torque, cleaner combustion, idle stability
- Coordination between intake and exhaust critical

### Tuning Considerations
- Incremental changes (2-5 degrees)
- Coordinate intake and exhaust cam timing
- Monitor knock activity and AVCS tracking error
- Test across full temperature and operating range
- Balance performance, driveability, and emissions

## Related Systems

AVCS tables interact with:
- **Ignition Timing** - Cam position affects dynamic compression and timing requirements
- **Fuel Targets** - Cam timing affects VE and optimal AFR
- **Boost Control** - Exhaust cam timing affects turbo spool and boost
- **TGV System** - Tumble valve state determines which cam table set is active
- **Knock Control** - Valve overlap affects knock sensitivity

## References

- **PARAMETERS.md** - Detailed AVCS runtime parameter documentation
- **README.md** - AVCS category overview

## Completion Recommendations

To finish documenting all 39 files:

1. **Use Provided Examples:** The 8 fully documented files serve as comprehensive templates
2. **Adapt Context:** Modify barometric, TGV, and aggressive designations appropriately
3. **Maintain Structure:** Keep all sections (Description, Functional Behavior, Related Tables, Datalog Parameters, Tuning Notes, Warnings)
4. **Cross-Reference:** Ensure Related Tables links are accurate and bidirectional
5. **Technical Accuracy:** Verify technical details specific to each table variant
6. **Fuel/Ignition Tables:** These require special attention as they bridge AVCS and other systems

## Tools Available

- `scripts/complete_avcs_docs.py` - Python script with documentation templates (ready for expansion)

## Notes

- All files maintain consistent structure for easy navigation
- Markdown links use relative paths for portability
- Technical terminology defined on first use
- Practical tuning guidance balances performance and safety
- Warnings sections emphasize coordination and testing requirements

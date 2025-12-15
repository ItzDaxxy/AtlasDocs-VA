# Fuel - CL/OL Transition - CL Limits (Switch to Open Loop) - Vehicle Speed - Vehicle Speed Maximum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `OL Transition - CL Limits (Switch to Open Loop) - Vehicle Speed - Vehicle Speed Maximum - 2018 - LF9C102P.csv` |

## Value

**255.0000 NONE**

## Description

This scalar defines a maximum vehicle speed threshold above which the ECU switches from closed-loop to open-loop fuel control. High-speed operation may warrant enrichment for safety margins, though this parameter is effectively disabled in stock calibration.

**Purpose:**
- Triggers OL mode at high vehicle speeds
- Could provide enrichment during high-speed operation
- Value of 255 effectively disables this feature

**Value Interpretation:**
- Value of 255.0 represents maximum possible speed threshold
- In typical scaling, this would be ~255 km/h or mph
- Effectively disables speed-based OL switching (threshold unreachable in normal use)

**Operating Logic:**
With threshold at 255, this parameter is effectively disabled. The ECU relies on other criteria (load, catalyst temp, fuel target) for CL/OL control rather than vehicle speed. Speed-based switching could be useful for top-speed runs or high-speed track use.

## Related Tables

- **[Fuel - CL/OL Transition - Calculated Load Maximum A](./fuel-clol-transition-cl-limits-switch-to-open-loop-calculated-load-calculated-load-maximum-a.md)**: Primary operative CL limit
- **[Fuel - CL/OL Transition - Per Gear Maximum RPM](./fuel-clol-transition-cl-limits-switch-to-open-loop-per-gear-maximum-rpm-per-gear.md)**: RPM-based per-gear limits
- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: Enrichment targets during OL

## Related Datalog Parameters

- **Vehicle Speed (km/h or mph)**: Compare to threshold (won't reach 255)
- **Fuel Mode**: CL/OL state (not affected by speed at stock settings)
- **RPM**: High speeds correlate with high RPM in gear
- **Calculated Load (g/rev)**: Primary CL/OL trigger

## Tuning Notes

**Stock Behavior:** Stock value of 255 effectively disables speed-based OL switching, relying on other parameters for CL/OL control.

**Common Modifications:**
- Could lower for track use to ensure enrichment at high speeds
- Example: Set to 200 km/h for extra margin during top-speed runs
- Most tuners leave at stock since load-based switching handles high-speed scenarios

**When Might Speed-Based OL Be Useful:**
- Standing mile or top-speed events
- Track use where sustained high speeds are common
- As additional safety layer for extended high-speed operation

**Interaction with Load:** At high speeds, load is typically high anyway, triggering load-based OL switching. Speed-based threshold is redundant unless load-based switching is disabled or threshold is raised.

**Validation:** Monitor vehicle speed and fuel mode during high-speed operation. Load-based switching typically activates OL before speed becomes a factor.

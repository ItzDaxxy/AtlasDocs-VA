# Fuel - Injectors - Pulse - Cylinder 4 - Scalar Table

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x20 |
| **Data Unit** | PERCENT |
| **Source File** | `Fuel - Injectors - Pulse - Cylinder 4 - Scalar Table - 2018 - LF9C102P.csv` |

## Description

This table defines individual cylinder fuel trim for Cylinder 4 (rear passenger side on FA20DIT), allowing per-cylinder pulse width adjustment as a percentage scalar. Used to compensate for cylinder-specific variations or requirements.

**Purpose:**
- Enables individual cylinder fuel trim for Cylinder 4
- Compensates for cylinder-to-cylinder variations
- Allows fine-tuning of fuel balance

**Value Interpretation:**
- Values in percent (100% = no change)
- Values >100% = add fuel to Cylinder 4
- Values <100% = remove fuel from Cylinder 4
- Stock values of 100% = no individual compensation

**Cylinder 4 Location:**
On the FA20DIT, Cylinder 4 is the rear cylinder on the passenger (right) side. It shares the right knock sensor with Cylinder 2.

## Axes

### X-Axis

- **Parameter**: Fuel - Injectors - RPM
- **Unit**: NONE
- **Range**: 400.0000 to 8000.0000
- **Points**: 20

### Y-Axis

- **Parameter**: Scaled IPW Command
- **Unit**: NONE
- **Range**: 1250.0000 to 11250.0000
- **Points**: 9

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   400.0000 |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |  3200.0000 |
--------------------------------------------------------------------------------------------------------------------
 1250.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 2500.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 3750.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 5000.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 6250.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 7500.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
 8000.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
10000.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |   100.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Current engine speed
- **Y-Axis (IPW Command)**: Scaled injector pulse width command

The interpolated percentage is multiplied with Cylinder 4's base pulse width:
```
Cylinder 4 Final IPW = Base IPW × (Cylinder 4 Scalar / 100)
```

**Application:**
Applied as final cylinder-specific adjustment after all other fuel calculations.

**Update Rate:** Evaluated every injection event for Cylinder 4.

## Related Tables

- **[Fuel - Injectors - Pulse - Cylinder 1 Scalar Table](./fuel-injectors-pulse-cylinder-1-scalar-table.md)**: Cylinder 1 trim
- **[Fuel - Injectors - Pulse - Cylinder 2 Scalar Table](./fuel-injectors-pulse-cylinder-2-scalar-table.md)**: Cylinder 2 trim
- **[Fuel - Injectors - Pulse - Cylinder 3 Scalar Table](./fuel-injectors-pulse-cylinder-3-scalar-table.md)**: Cylinder 3 trim
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate

## Related Datalog Parameters

- **RPM**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Y-axis input (scaled IPW command)
- **A/F Sensor 1 (λ)**: Overall AFR measurement
- **Feedback Knock (Right)**: Knock sensor 2 covers Cylinders 2 and 4

## Tuning Notes

**Stock Behavior:** Stock values of 100% everywhere indicate no individual cylinder compensation.

**Common Modifications:**
- Adjust if Cylinder 4 shows specific issues (knock, EGT difference)
- Rear cylinders may need different fueling due to intake runner design
- Right-side cylinders share knock sensor, may need coordinated adjustments

**Right Bank / Rear Cylinder Notes:**
Cylinder 4 is both right-bank and rear, so it may have unique characteristics:
- Shares knock sensor with Cylinder 2
- May have different airflow due to longer intake runner
- Some tuners find this cylinder needs unique attention

## Warnings

⚠️ **Limited Diagnostic Ability**: Standard wideband shows average AFR, not individual cylinder.

⚠️ **Knock Correlation**: If right knock sensor shows activity, investigate both Cyl 2 and Cyl 4.

⚠️ **Complete the Set**: When adjusting individual cylinders, consider all four to maintain balance.

**Safe Practices:**
- Start with 100% unless specific issue identified
- Small adjustments (1-2%)
- Monitor knock activity per bank
- Use EGT sensors if available for individual cylinder diagnostics

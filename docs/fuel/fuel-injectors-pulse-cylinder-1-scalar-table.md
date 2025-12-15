# Fuel - Injectors - Pulse - Cylinder 1 - Scalar Table

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 9x20 |
| **Data Unit** | PERCENT |
| **Source File** | `Fuel - Injectors - Pulse - Cylinder 1 - Scalar Table - 2018 - LF9C102P.csv` |

## Description

This table defines individual cylinder fuel trim for Cylinder 1, allowing per-cylinder pulse width adjustment as a percentage scalar. Used to compensate for manufacturing variations between cylinders or address cylinder-specific fueling requirements.

**Purpose:**
- Enables individual cylinder fuel trim
- Compensates for cylinder-to-cylinder variations
- Allows fine-tuning of fuel balance between cylinders

**Value Interpretation:**
- Values in percent (100% = no change)
- Values >100% = add fuel to this cylinder
- Values <100% = remove fuel from this cylinder
- Stock values of 100% across all cells = no individual cylinder compensation

**Why Individual Cylinder Trim:**
Even with identical injectors, cylinders may run slightly different AFRs due to:
- Intake manifold runner length differences
- Cylinder head flow variations
- Exhaust back-pressure differences
- Manufacturing tolerances

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

The interpolated percentage is multiplied with Cylinder 1's base pulse width:
```
Cylinder 1 Final IPW = Base IPW × (Cylinder 1 Scalar / 100)
```

**Application:**
This scalar is applied after all other fuel calculations (load, pressure compensation, etc.) as a final cylinder-specific adjustment.

**Update Rate:** Evaluated every injection event for Cylinder 1.

## Related Tables

- **[Fuel - Injectors - Pulse - Cylinder 2 Scalar Table](./fuel-injectors-pulse-cylinder-2-scalar-table.md)**: Cylinder 2 trim
- **[Fuel - Injectors - Pulse - Cylinder 3 Scalar Table](./fuel-injectors-pulse-cylinder-3-scalar-table.md)**: Cylinder 3 trim
- **[Fuel - Injectors - Pulse - Cylinder 4 Scalar Table](./fuel-injectors-pulse-cylinder-4-scalar-table.md)**: Cylinder 4 trim
- **[Fuel - Injectors - Direct Injector Size](./fuel-injectors-direct-injector-size.md)**: Base injector flow rate

## Related Datalog Parameters

- **RPM**: X-axis input for table lookup
- **Injector Pulse Width (ms)**: Y-axis input (scaled IPW command)
- **A/F Sensor 1 (λ)**: Overall AFR (can't see individual cylinders directly)
- **EGT 1 (if equipped)**: Exhaust gas temperature for Cylinder 1

## Tuning Notes

**Stock Behavior:** Stock values of 100% everywhere indicate no individual cylinder compensation in base calibration.

**Common Modifications:**
- **Cylinder Balance**: If one cylinder runs consistently lean/rich, adjust its scalar
- **Modified Engines**: Ported heads, different intake, etc. may need cylinder-specific adjustments
- Typically ±5-10% range for minor corrections

**Diagnosing Need for Adjustment:**
- Individual cylinder EGT sensors (if available)
- Individual cylinder wideband sensors
- Knock activity on specific cylinders
- Misfire counts by cylinder

**FA20DIT Cylinder Numbering:**
- Cylinder 1: Front left (driver's side)
- Cylinder 2: Front right (passenger side)
- Cylinder 3: Rear left
- Cylinder 4: Rear right

## Warnings

⚠️ **Limited Diagnostic Ability**: Without per-cylinder AFR monitoring, difficult to determine optimal values.

⚠️ **Stock Typically Adequate**: Most stock and mildly modified engines don't need individual cylinder trim.

⚠️ **Knock Indication**: If a specific cylinder shows persistent knock, consider fueling before ignition adjustments.

**Safe Practices:**
- Start with 100% (no change) unless specific issue is identified
- Make small adjustments (1-2% at a time)
- Verify with appropriate diagnostic equipment
- Monitor knock counts per cylinder

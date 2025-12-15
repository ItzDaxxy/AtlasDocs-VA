# Ignition - Compensation - IAT - IAT Compensation B Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Compensation - IAT - IAT Compensation B Activation - 2017 - RogueWRX.csv` |

## Description

This 2D table defines the activation percentage for IAT (Intake Air Temperature) timing compensation variant B, indexed by calculated load and RPM. It scales the base IAT compensation B to vary its effect across different operating conditions.

**Purpose:**
- Controls where and how much IAT compensation B applies
- Allows RPM and load-dependent scaling of temperature compensation
- Negative values reduce or negate the base compensation
- Variant B likely used for different operating conditions than variant A

**Value Interpretation:**
- Values in percent (%)
- -100% = Completely disables IAT compensation at that point
- Negative values counteract base IAT compensation
- Pattern varies strategically by RPM and load

**Pattern Analysis:**
The preview shows all -100% values in the visible area, indicating IAT compensation B is disabled across these operating regions. Higher load/RPM areas (not shown) may have different values.

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 2.5782
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 7600.0000
- **Points**: 22

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.4512 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |
--------------------------------------------------------------------------------------------------------------------
  400.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
  800.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 1000.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 1200.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 1600.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 1800.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 2000.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
 2200.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |  -100.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Activation Calculation:**
```
Effective IAT Compensation B = Base IAT Compensation B × (1 + Activation%/100)
```
With -100% activation values, the base compensation is completely disabled:
- Base = -3° retard, Activation = -100%
- Effective = -3° × (1 - 1.00) = 0° (no compensation)

**All -100% in Preview:**
The preview area shows complete disabling of variant B. This could mean:
- Variant B is only active at higher loads/RPM not shown
- Variant A is the primary IAT compensation strategy
- Variant B is reserved for specific conditions

**Variant A vs B Selection:**
The ECU likely switches between IAT compensation variants based on:
- Operating mode
- Load range
- Boost level
- Other calibration logic

**Update Rate:** Calculated continuously alongside IAT compensation.

## Related Tables

- **[Ignition - Compensation - IAT - Compensation B](./ignition-compensation-iat-iat-compensation-b.md)**: Base IAT compensation B scaled by this table
- **[Ignition - Compensation - IAT - Compensation A Activation](./ignition-compensation-iat-iat-compensation-a-activation.md)**: Variant A activation
- **[Ignition - Compensation - IAT - Compensation A](./ignition-compensation-iat-iat-compensation-a.md)**: Variant A base compensation

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **IAT (Intake Air Temperature)**: Drives base compensation
- **Ignition Timing**: Shows final timing with scaled compensation
- **Manifold Pressure**: May influence A/B selection

## Tuning Notes

**Stock Behavior:** Stock shows variant B disabled across low-to-mid RPM and load ranges shown in preview. Higher operating regions may use variant B.

**Understanding -100% Values:**
Complete disabling of variant B in these regions means:
- No IAT compensation B applied here
- Variant A handles IAT compensation (if active)
- Simplified calibration for these operating points

**Variant B Purpose:**
Speculation on variant B usage:
- High boost/load scenarios
- Track/performance mode
- Alternative calibration strategy
- Backup or conditional compensation

**Common Modifications:**
- Usually left at stock
- Rarely modified without understanding ECU's variant selection logic
- Changes require comprehensive understanding of both A and B systems

## Warnings

**Complex System**: Multiple IAT compensation variants with separate activation - modifications require system understanding.

**Knock Protection**: Disabling IAT compensation (keeping at -100%) can cause knock if IAT is elevated.

**Unknown Selection Logic**: Without knowing when ECU uses variant B, modifications are risky.

**Safe Practices:**
- Leave at stock unless variant selection logic is understood
- Monitor IAT and knock events if modifying
- Test across various ambient temperatures
- Understand relationship between variants A and B before changes

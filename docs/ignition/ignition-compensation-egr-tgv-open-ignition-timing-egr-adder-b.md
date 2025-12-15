# Ignition - Compensation - EGR - TGV Open - Ignition Timing EGR Adder B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - EGR - TGV Open - Ignition Timing EGR Adder B - 2017 - RogueWRX.csv` |

## Description

This table defines ignition timing adjustment based on EGR (Exhaust Gas Recirculation) rate for TGV open conditions, variant B, indexed by calculated load and RPM. It compensates timing for the combustion effects of exhaust gas dilution.

**Purpose:**
- Adjusts timing based on EGR rate/status
- EGR dilutes intake charge, slowing combustion
- Timing advance compensates for slower burn
- TGV open = higher load/RPM where EGR may be active
- Variant B is one of multiple EGR compensation strategies

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive values = timing advance (compensate for EGR dilution)
- Negative values = timing retard
- Zero = no compensation (EGR inactive or minimal)

**All Zeros in Preview:**
The preview shows all zero values. This indicates:
- EGR compensation variant B is disabled in this calibration
- Table available for tuning but stock uses no EGR timing adjustment
- VA WRX may have minimal EGR activity requiring compensation
- Variant B may be reserved for specific conditions not encountered

## Axes

### X-Axis

- **Parameter**: Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1289 to 3.0938
- **Points**: 16

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 6401.1719
- **Points**: 22

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1289 |     0.2578 |     0.3867 |     0.5156 |     0.6445 |     0.7734 |     0.9024 |     1.0313 |
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

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**EGR Effect on Combustion:**
When EGR is active:
- Exhaust gas displaces fresh air
- Combustion temperature drops (reduces NOx)
- Flame speed decreases
- More timing advance may help efficiency

**Why All Zeros:**
Stock calibration shows no EGR timing compensation variant B:
- EGR effect may be minimal in VA WRX application
- Variant B may be unused or reserved
- Other variants (A, C, D) may handle EGR compensation
- Table provides capability if needed

**Multiple EGR Variants:**
Multiple EGR adder tables (A, B, C, D) exist - selection likely based on:
- TGV state (open/closed)
- Operating conditions
- EGR rate magnitude
- Calibration strategy

**TGV Open Context:**
TGVs open at higher load/RPM where:
- EGR may be less active (performance priority)
- Other knock protections are more critical
- Emissions compliance may differ

**Update Rate:** Calculated continuously when EGR system is active.

## Related Tables

- **[Ignition - Compensation - EGR - TGV Open - Adder D](./ignition-compensation-egr-tgv-open-ignition-timing-egr-adder-d.md)**: Alternate TGV open EGR adder
- **[Ignition - Compensation - EGR - TGV Closed - Adder A](./ignition-compensation-egr-tgv-closed-ignition-timing-egr-adder-a.md)**: TGV closed EGR adder
- **[Ignition - Compensation - EGR - TGV Closed - Adder C](./ignition-compensation-egr-tgv-closed-ignition-timing-egr-adder-c.md)**: Alternate TGV closed adder

## Related Datalog Parameters

- **EGR Duty Cycle (%)**: EGR valve command
- **EGR Flow Rate**: Actual EGR mass flow
- **Ignition Timing**: Shows final timing with EGR compensation
- **TGV Position**: Should be open for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Stock Behavior:** Stock table is all zeros - no EGR timing compensation variant B in this calibration. Table exists but is not actively used.

**EGR on VA WRX:**
The 2015-2021 WRX has an internal EGR system:
- Exhaust gas mixes at intake via valve overlap
- External EGR valve may have limited use
- Timing compensation may be unnecessary at higher loads
- TGV open typically means performance-oriented operation

**Variant B Purpose:**
Since all zeros, variant B either:
- Is not used by the ECU
- Is reserved for future use
- Is used only in rare conditions not represented in data
- Is an alternate strategy not employed on this platform

**Common Modifications:**
- Usually left at zero
- Rarely relevant since stock doesn't use it
- EGR delete: Makes this table completely irrelevant
- May add compensation if custom EGR strategy needed

## Warnings

**Usually Not Active**: Stock all-zeros suggests this variant is unused.

**EGR System Interaction**: Only relevant if EGR system is functioning.

**TGV State Dependency**: Only applies when TGVs are open.

**Safe Practices:**
- Leave at zero unless specific EGR-related timing issues
- Verify EGR is actually active before adding compensation
- Monitor for knock if adding advance
- Understand relationship to other EGR adder variants (A, C, D)

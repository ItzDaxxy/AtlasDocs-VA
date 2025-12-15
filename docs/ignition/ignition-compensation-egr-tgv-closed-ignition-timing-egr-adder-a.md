# Ignition - Compensation - EGR - TGV Closed - Ignition Timing EGR Adder A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 22x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - EGR - TGV Closed - Ignition Timing EGR Adder A - 2017 - RogueWRX.csv` |

## Description

This table defines ignition timing adjustment based on EGR (Exhaust Gas Recirculation) rate for TGV closed conditions, variant A, indexed by calculated load and RPM. It compensates timing for the combustion effects of exhaust gas dilution.

**Purpose:**
- Adjusts timing based on EGR rate/status
- EGR dilutes intake charge, slowing combustion
- Timing advance compensates for slower burn
- TGV closed = idle and light load where EGR is active

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive values = timing advance (compensate for EGR dilution)
- Negative values = timing retard
- Zero = no compensation (EGR inactive or minimal)

**All Zeros in Preview:**
The preview shows all zero values. This could indicate:
- EGR compensation disabled in this calibration
- Table available for tuning but stock uses no EGR timing adjustment
- VA WRX may have minimal EGR activity requiring compensation

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
Stock calibration shows no EGR timing compensation:
- EGR effect may be minimal in VA WRX application
- Or compensation is handled elsewhere
- Table provides capability if needed

**Variant A vs Other Variants:**
Multiple EGR adder tables (A, B, C, D) exist - selection likely based on:
- TGV state (open/closed)
- Operating conditions
- EGR rate magnitude

**Update Rate:** Calculated continuously when EGR is active.

## Related Tables

- **[Ignition - Compensation - EGR - TGV Closed - Adder C](./ignition-compensation-egr-tgv-closed-ignition-timing-egr-adder-c.md)**: Alternate TGV closed EGR adder
- **[Ignition - Compensation - EGR - TGV Open - Adder B](./ignition-compensation-egr-tgv-open-ignition-timing-egr-adder-b.md)**: EGR adder for TGV open
- **[Ignition - Compensation - EGR - TGV Open - Adder D](./ignition-compensation-egr-tgv-open-ignition-timing-egr-adder-d.md)**: Alternate TGV open adder

## Related Datalog Parameters

- **EGR Duty Cycle (%)**: EGR valve command
- **EGR Flow Rate**: Actual EGR mass flow
- **Ignition Timing**: Shows final timing with EGR compensation
- **TGV Position**: Should be closed for this table
- **Calculated Load (g/rev)**: X-axis input

## Tuning Notes

**Stock Behavior:** Stock table is all zeros - no EGR timing compensation in this calibration. EGR system may have minimal timing effect, or compensation is integrated elsewhere.

**EGR on VA WRX:**
The 2015-2021 WRX has an internal EGR system:
- Exhaust gas mixes at intake via valve overlap
- External EGR valve may have limited use
- Timing compensation may be unnecessary

**When Compensation Would Help:**
If EGR is active and causes:
- Rough idle
- Hesitation
- Misfire
Adding timing advance (positive values) could compensate. But since table is all zeros, stock calibration doesn't require this.

**Common Modifications:**
- Usually left at zero if EGR is stock
- EGR delete: Irrelevant if no EGR flow
- May add compensation if EGR issues occur

## Warnings

⚠️ **Usually Not Modified**: Stock all-zeros suggests no compensation needed.

⚠️ **EGR System Interaction**: Only relevant if EGR system is functioning.

⚠️ **TGV State Dependency**: Only applies when TGVs are closed.

**Safe Practices:**
- Leave at zero unless specific EGR-related timing issues
- If adding compensation, verify EGR is actually active
- Monitor for knock if adding advance

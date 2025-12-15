# Ignition - Primary - Idle/Decel - Ignition Timing B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Decel - Ignition Timing B - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing during idle and deceleration conditions (variant B), indexed by RPM. It provides an alternate timing map for closed-throttle operation, likely used under different engine conditions than variant A.

**Purpose:**
- Alternate timing during idle (throttle closed, low RPM)
- Alternate timing during deceleration (throttle closed, engine braking)
- Different calibration for specific conditions (likely warm engine)
- Complements variant A for comprehensive idle control

**Value Interpretation:**
- Values in degrees BTDC (Before Top Dead Center)
- May differ from variant A based on temperature or state
- Typically used for warm engine idle (vs cold in variant A)
- Optimized for steady-state warm operation

**Variant B Context:**
Variant B is likely the "warm" or "steady-state" idle table:
- Used after engine reaches operating temperature
- May have different timing than cold-start variant A
- Optimized for fuel economy and emissions at warm idle

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 500.0000 to 6375.0000
- **Points**: 16

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   500.0000 |   600.0000 |   700.0000 |   800.0000 |   900.0000 |  1000.0000 |  1200.0000 |  1400.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (RPM)**: Current engine speed

**When Active:**
This table is active when:
- Throttle is closed (idle switch active)
- Engine is idling or decelerating
- Variant B conditions are met (likely warm operation)

**A vs B Selection Logic:**
The ECU selects between variants based on:
- **Coolant Temperature**: Cold = A, Warm = B (likely)
- **Time Since Start**: Initial period = A, Later = B
- **Catalyst Temperature**: Pre-lightoff = A, Post-lightoff = B

**Typical Warm Idle Values:**
Warm idle timing is often slightly more advanced than cold:
- Warm combustion is more efficient
- Knock resistance is better established
- Fuel atomization is improved

**1D Table Format:**
The 0x16 dimension indicates 1D lookup with 16 RPM points.

**Update Rate:** Evaluated continuously during idle/decel with warm conditions.

## Related Tables

- **[Ignition - Primary - Idle/Decel - Timing A](./ignition-primary-idledecel-ignition-timing-a.md)**: Cold/alternate idle timing table
- **[Ignition - Primary - TGVs Closed (AVCS Disabled)](./primary-tgvs-closed-avcs-disabled.md)**: Primary timing maps
- **[Ignition - Compensation - Coolant (TGV Open)](./ignition-compensation-coolant-tgv-open.md)**: Temperature compensation

## Related Datalog Parameters

- **RPM**: X-axis input
- **Throttle Position (%)**: Indicates idle/decel mode
- **Ignition Timing**: Final timing
- **Coolant Temperature (°C)**: Likely affects A/B selection
- **Catalyst Temperature (°C)**: May affect table selection

## Tuning Notes

**Stock Behavior:** Stock variant B provides warm-idle optimized timing. May be slightly more advanced than variant A for better fuel economy at operating temperature.

**Warm vs Cold Idle:**
- **Cold (Variant A)**: Often more retarded for stable idle while warming
- **Warm (Variant B)**: Can be more advanced for efficiency
- Difference is typically small (2-5°)

**Common Modifications:**
- Often modified together with variant A for consistency
- May advance slightly for better response with modified engines
- Rarely modified without specific warm-idle issues

**Matching A and B:**
When tuning, ensure both variants provide acceptable idle quality. The transition between them should be smooth and not cause idle fluctuations.

**Decel Considerations:**
Both variants affect deceleration timing. Ensure smooth decel behavior after modifications to either table.

## Warnings

⚠️ **Warm Idle Stability**: Changes affect steady-state warm idle quality.

⚠️ **A/B Transition**: Ensure smooth transition between variants as engine warms.

⚠️ **Emissions**: Warm idle timing directly affects emissions test results.

**Safe Practices:**
- Test at fully warm operating temperature
- Verify smooth A-to-B transition during warmup
- Monitor for knock at warm idle
- Check deceleration behavior

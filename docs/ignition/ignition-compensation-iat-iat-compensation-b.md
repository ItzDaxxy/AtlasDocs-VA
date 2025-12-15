# Ignition - Compensation - IAT - IAT Compensation B

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Ignition - Compensation - IAT - IAT Compensation B - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation based on intake air temperature (IAT), variant B. It provides an alternate IAT compensation profile, likely used during high-load or boost conditions where IAT sensitivity is more critical.

**Purpose:**
- Adjusts timing based on intake air temperature (variant B)
- Likely active during high-load/boost conditions
- Retards timing when intake air is hot
- More critical for knock protection under boost

**Value Interpretation:**
- Values represent timing adjustment
- Negative = retard (typical for hot IAT)
- Positive = advance (typical for cold IAT)
- Variant B likely has more aggressive retard than variant A

**Variant B Context:**
High-load conditions where IAT is most critical:
- Under boost, compressed air is hot
- Knock risk increases dramatically with hot IAT
- More aggressive compensation protects the engine

## Axes

### X-Axis

- **Parameter**: IAT (Intake Air Temperature)
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: NONE (degrees of timing adjustment)
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    35.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (IAT)**: Current intake air temperature

**Variant B vs A Selection:**
Selection between IAT compensation tables likely based on:
- Load level (high load = variant B)
- Boost pressure
- RPM
- Operating condition flags

**Why Separate Tables:**
Different IAT compensation for different conditions:
- **Variant A**: Normal/cruise - less aggressive
- **Variant B**: Boost/high load - more aggressive protection

**Update Rate:** Evaluated continuously based on IAT sensor.

## Related Tables

- **[Ignition - Compensation - IAT - Compensation A](./ignition-compensation-iat-iat-compensation-a.md)**: Normal/low-load IAT compensation
- **[Ignition - Compensation - IAT - Compensation B Activation](./ignition-compensation-iat-iat-compensation-b-activation.md)**: Scales variant B by RPM/load
- **[Ignition - Compensation - IAT - Compensation A Activation](./ignition-compensation-iat-iat-compensation-a-activation.md)**: Scales variant A

## Related Datalog Parameters

- **IAT (Intake Air Temperature)**: X-axis input
- **Ignition Timing**: Final timing with compensation
- **Manifold Pressure**: May influence table selection
- **Calculated Load**: Related to activation

## Tuning Notes

**Stock Behavior:** Stock variant B provides appropriate IAT retard for high-load conditions where knock risk from hot air is highest.

**Critical for Turbo Application:**
On turbocharged engines:
- Turbo adds significant heat to intake air
- High-load = high boost = highest IAT
- Variant B protects during these conditions

**Common Modifications:**
- May increase hot-IAT retard for safety margin
- Intercooler upgrade may allow reduced retard
- Don't reduce without verified knock data

## Warnings

⚠️ **Critical Knock Protection**: IAT compensation is essential for knock prevention under boost.

⚠️ **High-Load Focus**: Variant B likely active during most knock-prone conditions.

⚠️ **Heat Soak Danger**: After sustained boost, IAT remains elevated.

**Safe Practices:**
- Monitor IAT during boost
- Allow cool-down after hard driving
- Don't reduce retard without knock verification
- Consider ambient temperature effects

# Ignition - Compensation - Coolant - TGV Open

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Coolant - TGV Open - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation based on engine coolant temperature for TGV open conditions. It adjusts timing to account for different combustion characteristics at various engine temperatures.

**Purpose:**
- Adjusts timing based on engine temperature
- Typically advances timing when cold (more advance needed for efficiency)
- May retard when very hot (knock prevention)
- TGV open = moderate to high load conditions

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive values = timing advance (typical for cold)
- Negative values = timing retard (typical for hot)
- Zero = no compensation (usually at normal operating temp)

**Cold Engine Behavior:**
When cold, combustion is less efficient:
- Poor fuel atomization
- Slower flame speed
- More advance helps maintain power and emissions

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
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
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (Coolant Temp)**: Current engine coolant temperature

**Typical Compensation Pattern:**
- Very Cold (-40 to 0°C): Significant advance (5-10°)
- Cold (0 to 40°C): Moderate advance (2-5°)
- Normal (40 to 90°C): Little or no compensation
- Hot (90 to 110°C): May retard slightly for knock protection

**Application with Activation Table:**
The coolant compensation value from this table is scaled by the activation table before being applied:
```
Effective Compensation = Base Compensation × Activation %
```
This allows the compensation to be RPM and load dependent.

**TGV Open Context:**
When TGVs are open (higher loads), airflow is unrestricted. This table provides appropriate cold compensation for these high-flow conditions.

**1D Table Format:**
The 0x16 dimension indicates 1D lookup with 16 temperature points.

**Update Rate:** Evaluated continuously based on coolant temperature.

## Related Tables

- **[Ignition - Compensation - Coolant - TGV Open Activation](./ignition-compensation-coolant-tgv-open-activation.md)**: Scales this compensation by RPM/load
- **[Ignition - Compensation - Coolant - TGV Closed](./ignition-compensation-coolant-tgv-closed.md)**: Temperature compensation for TGV closed
- **[Ignition - Compensation - Coolant - TGV Closed Activation](./ignition-compensation-coolant-tgv-closed-activation.md)**: TGV closed activation scaling

## Related Datalog Parameters

- **Coolant Temperature (°C)**: X-axis input
- **Ignition Timing**: Shows final timing with compensations
- **TGV Position**: Should be open (100%) for this table
- **Calculated Load (g/rev)**: Input to activation table

## Tuning Notes

**Stock Behavior:** Stock provides cold-start timing advance that improves driveability and emissions during warm-up. Compensation typically zeros out above ~70-80°C.

**Why Advance When Cold:**
Cold engines benefit from more timing because:
- Slower flame propagation
- Higher heat losses to cold cylinder walls
- Poor fuel vaporization
More advance compensates for these inefficiencies.

**Common Modifications:**
- Usually left at stock for proper warm-up behavior
- May reduce cold advance if experiencing cold knock
- Hot retard may be added for high-load track applications

**Hot Operation:**
Some calibrations retard timing at very high coolant temps to prevent knock. This is especially important for turbocharged engines where heat soak is a concern.

**Interaction with Other Tables:**
This compensation stacks with:
- Primary timing maps
- Dynamic advance
- IAT compensation
- Knock corrections

## Warnings

⚠️ **Cold Start Critical**: Cold compensation affects driveability during warm-up.

⚠️ **Hot Knock**: If hot operation causes knock, may need retard at high temps.

⚠️ **TGV State**: Only applies when TGVs are open.

**Safe Practices:**
- Test cold start and warm-up driveability after changes
- Monitor knock across temperature range
- Verify smooth operation from cold to hot

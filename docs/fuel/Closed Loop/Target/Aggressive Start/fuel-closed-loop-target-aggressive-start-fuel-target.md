# Fuel - Closed Loop - Target - Aggressive Start - Fuel Target

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x16 |
| **Data Unit** | LAMBDA |
| **Source File** | `Fuel - Closed Loop - Target - Aggressive Start - Fuel Target - 2018 - LF9C102P.csv` |

## Description

This table defines lambda targets during "Aggressive Start" conditions, indexed by calculated load and RPM. Aggressive Start is a cold-start enrichment mode that uses significantly richer mixtures during engine warm-up.

**Purpose:**
- Provides rich lambda targets during cold start
- Ensures stable combustion with cold engine/fuel
- Faster catalyst warm-up through rich operation

**Value Interpretation:**
- Values in lambda (λ)
- λ = 0.90-0.9433 = 7-10% rich of stoichiometric
- These are significantly richer than normal CL targets (~1.0)
- Rich mixture aids cold engine combustion

**Aggressive Start Mode:**
During cold starts, combustion is challenged by:
- Poor fuel atomization on cold surfaces
- Fuel condensation on intake/cylinders
- Inefficient combustion at low temps
Rich targets ensure adequate combustible mixture.

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.1290 to 2.5800
- **Points**: 16

### Y-Axis

- **Parameter**: Fueling - Closed Loop - RPM
- **Unit**: NONE
- **Range**: 700.0000 to 6400.0000
- **Points**: 16

## Cell Values

- **Unit**: LAMBDA
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.1290 |     0.2580 |     0.3870 |     0.5160 |     0.6450 |     0.7740 |     0.9030 |     1.0320 |
--------------------------------------------------------------------------------------------------------------------
  700.0000 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |
  800.0000 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |     0.9433 |
 1200.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9260 |     0.9260 |     0.9260 |
 1600.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9000 |     0.9000 |     0.9000 |
 2000.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9000 |     0.9000 |     0.9000 |
 2400.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |
 2800.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |
 3200.0000 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |     0.9001 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**Table Activation:**
Aggressive Start targets are used when:
- Coolant temp below certain threshold
- Engine recently started
- Other activation conditions met

**Target Pattern:**
- Idle/Low RPM (700-800): 0.9433λ (~6% rich)
- Mid RPM and above: 0.90-0.926λ (~7-10% rich)
- Consistent enrichment across load range within RPM bands

**Update Rate:** Used during cold start until exit conditions met.

## Related Tables

- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Max Activation](./fuel-closed-loop-target-aggressive-start-coolant-max-activation.md)**: Max coolant temp for activation
- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Min Activation](./fuel-closed-loop-target-aggressive-start-coolant-min-activation.md)**: Min coolant temp
- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder](./fuel-closed-loop-target-aggressive-start-fuel-target-adder.md)**: Additional enrichment adder
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Normal CL targets (used after warm-up)

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input
- **RPM**: Y-axis input
- **Command Fuel Final (λ)**: Resulting lambda target
- **Coolant Temperature (°C)**: Determines if Aggressive Start active
- **Engine Runtime**: Duration since start

## Tuning Notes

**Stock Behavior:** Stock Aggressive Start provides rich targets (~0.90-0.94λ) for reliable cold starts and fast catalyst warm-up.

**Cold Start Purpose:**
Rich cold-start mixtures serve dual purposes:
1. Compensate for poor fuel vaporization (engine needs it rich to run)
2. Provide excess hydrocarbons for catalyst exothermic reaction (fast light-off)

**Common Modifications:**
- Generally left at stock for proper cold start behavior
- Too lean = rough/stalling cold starts
- Too rich = excessive emissions, possible fouling

**Catalyst Warm-Up:**
The rich mixture creates unburned hydrocarbons that react with excess air in catalyst, generating heat for fast catalyst light-off.

## Warnings

⚠️ **Cold Start Critical**: These targets determine cold start quality. Incorrect values cause starting issues.

⚠️ **Emissions Impact**: Cold start is significant portion of drive-cycle emissions. Stock calibration optimized for compliance.

⚠️ **Spark Plug Fouling**: Excessively rich cold operation can foul plugs over time.

**Safe Practices:**
- Test cold starts at various temperatures if modifying
- Ensure smooth idle during warm-up
- Monitor catalyst light-off timing

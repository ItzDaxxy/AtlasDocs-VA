# Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder Activation - 2018 - LF9C102P.csv` |

## Description

This table defines the activation schedule for the Aggressive Start fuel target adder, likely indexed by engine runtime or cycle count. It controls when and how much the fuel target adder is applied during the Aggressive Start phase.

**Purpose:**
- Controls temporal activation of fuel target adder
- Manages transition from cold-start enrichment to normal operation
- Allows graduated reduction of adder effect over time/cycles

**Value Interpretation:**
- X-axis values (1-15) likely represent engine runtime in seconds or ignition cycles
- Table values (not shown in preview) define activation multiplier or percentage
- Higher values = more adder effect, lower values = less effect
- Provides smooth transition out of Aggressive Start mode

**Unusual Table Structure:**
This table appears to be 1D (0x8 dimension means no Y-axis rows), functioning as a simple lookup against engine runtime or cycle count during cold start.

## Axes

### X-Axis

- **Parameter**: Engine Runtime or Cycle Count
- **Unit**: Seconds or Cycles (likely)
- **Range**: 1.0000 to 15.0000
- **Points**: 8

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     1.0000 |     3.0000 |     5.0000 |     7.0000 |     9.0000 |    11.0000 |    13.0000 |    15.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (Time/Cycles)**: Engine runtime since start or ignition cycles

**Activation Multiplier Function:**
```
Effective Adder = Base Adder × Activation Value
```

Where:
- Base Adder comes from the Fuel Target Adder table (currently all zeros)
- Activation Value from this table controls how much of the adder applies

**Time-Based Decay:**
The X-axis values of 1-15 suggest a 15-second (or 15-cycle) activation window where the adder effect can be modulated. Even with stock zero adder values, this table provides the framework for time-based enrichment decay.

**Why Table Appears Empty:**
The 0x8 dimension indicates this is a 1D table with only X-axis values. The output values (activation multipliers) should exist but may not display in the standard 2D preview format.

**Update Rate:** Evaluated continuously during Aggressive Start operation.

## Related Tables

- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target Adder](./fuel-closed-loop-target-aggressive-start-fuel-target-adder.md)**: Adder values (multiplied by activation)
- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target](./fuel-closed-loop-target-aggressive-start-fuel-target.md)**: Base cold-start targets
- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Max Activation](./fuel-closed-loop-target-aggressive-start-coolant-max-activation.md)**: Temperature exit conditions
- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Min Activation](./fuel-closed-loop-target-aggressive-start-coolant-min-activation.md)**: Temperature entry conditions

## Related Datalog Parameters

- **Engine Runtime**: Likely X-axis input (seconds since start)
- **Coolant Temperature (°C)**: Affects whether Aggressive Start mode is active
- **Command Fuel Final (λ)**: Shows final target with adder applied
- **Ignition Cycle Count**: Alternative X-axis input possibility

## Tuning Notes

**Stock Behavior:** This activation table controls the temporal application of the fuel target adder. Since the base adder table is all zeros, this activation table has no practical effect in stock configuration.

**Potential Function:**
If the adder table were populated with non-zero values:
- Early in cold start (1-5 seconds): High activation = full adder effect
- Mid cold start (5-10 seconds): Declining activation
- Late cold start (10-15 seconds): Low/zero activation = transition to normal targets

**Common Modifications:**
- Usually left at stock since base adder is zero
- Could be modified if adding enrichment to specific cold-start phases
- Allows fine-tuning of enrichment decay rate during warm-up

**Activation Timing:**
The 15-second range suggests this controls the first 15 seconds of engine operation during cold starts. This aligns with typical Aggressive Start duration before transitioning to normal closed-loop operation.

## Warnings

⚠️ **Coupled with Adder Table**: This table only has effect if the Fuel Target Adder table has non-zero values.

⚠️ **Cold Start Timing Critical**: Incorrect activation timing can cause rough idle or stalling during warm-up.

⚠️ **Unclear Table Format**: The 0x8 dimension suggests 1D table - actual data values may not display correctly in preview.

**Safe Practices:**
- Understand relationship with base adder table before modifying
- If adding cold-start enrichment, adjust both tables together
- Test cold starts at various temperatures to verify behavior

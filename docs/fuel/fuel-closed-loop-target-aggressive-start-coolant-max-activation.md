# Fuel - Closed Loop - Target - Aggressive Start - Coolant Max. Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Fuel - Closed Loop - Target - Aggressive Start - Coolant Max. Activation - 2018 - LF9C102P.csv` |

## Value

**119.9976 CELSIUS**

## Description

This scalar defines the maximum coolant temperature at which Aggressive Start enrichment can remain active. Above this temperature, the ECU exits Aggressive Start mode and transitions to normal closed-loop operation.

**Purpose:**
- Sets upper temperature limit for Aggressive Start mode
- Prevents unnecessary enrichment when engine is hot
- Defines exit condition for cold-start enrichment

**Value Interpretation:**
- Value of ~120°C is effectively "always allow" (engine rarely reaches 120°C)
- This high threshold means Aggressive Start is primarily controlled by time/other conditions
- Hot engine would not use Aggressive Start regardless of this value

**Practical Effect:**
With max activation at 120°C, this parameter doesn't actively limit Aggressive Start during normal operation. Other exit conditions (time-based, etc.) typically end Aggressive Start mode.

## Related Tables

- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Min Activation](./fuel-closed-loop-target-aggressive-start-coolant-min-activation.md)**: Minimum temp for activation
- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target](./fuel-closed-loop-target-aggressive-start-fuel-target.md)**: Lambda targets during Aggressive Start
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Normal CL targets

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Compared against this threshold
- **Command Fuel Final (λ)**: Shows if Aggressive Start targets active
- **Engine Runtime**: Related exit condition

## Tuning Notes

**Stock Behavior:** Stock value of ~120°C effectively allows Aggressive Start at any normal engine temperature - exit is controlled by other factors.

**Common Modifications:**
- Could lower to ~80-90°C to exit Aggressive Start earlier on warm restarts
- Stock value appropriate for most applications

**Warm Restart Consideration:**
If engine is hot and restarted, Aggressive Start may briefly activate then exit via other conditions. Lowering this value would immediately skip Aggressive Start on hot restarts.

**Warning:** Lowering significantly could cause cold-start issues at borderline temperatures.

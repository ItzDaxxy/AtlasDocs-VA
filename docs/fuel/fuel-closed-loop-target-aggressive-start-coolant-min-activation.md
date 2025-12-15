# Fuel - Closed Loop - Target - Aggressive Start - Coolant Min. Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Fuel - Closed Loop - Target - Aggressive Start - Coolant Min. Activation - 2018 - LF9C102P.csv` |

## Value

**-40.0000 CELSIUS**

## Description

This scalar defines the minimum coolant temperature at which Aggressive Start enrichment activates. Below this temperature, an even more aggressive cold-start strategy may be used, or this represents the lowest operational limit.

**Purpose:**
- Sets lower temperature bound for Aggressive Start mode
- Defines entry condition for cold-start enrichment
- -40°C represents extreme cold operation limit

**Value Interpretation:**
- Value of -40°C = Aggressive Start available at essentially all cold temperatures
- This is the minimum expected operating temperature
- No colder operation expected (vehicle/fuel limits)

**Practical Effect:**
With min activation at -40°C, Aggressive Start is available for any cold start condition. This ensures rich targets are used from the coldest possible starts.

## Related Tables

- **[Fuel - Closed Loop - Target - Aggressive Start - Coolant Max Activation](./fuel-closed-loop-target-aggressive-start-coolant-max-activation.md)**: Maximum temp for activation
- **[Fuel - Closed Loop - Target - Aggressive Start - Fuel Target](./fuel-closed-loop-target-aggressive-start-fuel-target.md)**: Lambda targets during Aggressive Start
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Normal CL targets

## Related Datalog Parameters

- **Coolant Temperature (°C)**: Compared against this threshold
- **Command Fuel Final (λ)**: Shows if Aggressive Start targets active
- **Engine Runtime**: Time since start

## Tuning Notes

**Stock Behavior:** Stock value of -40°C ensures Aggressive Start is available for all realistic cold starts.

**Common Modifications:**
- Rarely modified - represents physical operation limit
- Could raise to disable Aggressive Start for mild cold starts
- Generally left at stock

**Extreme Cold Operation:**
At -40°C, fuel and engine behavior are severely challenged. The Aggressive Start targets provide necessary enrichment for these extreme conditions.

**Warning:** Raising this value means colder starts won't get Aggressive Start enrichment, potentially causing starting issues.

# Fuel - Timing - HPFP - Valve Close Limit Minimum

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | DEGREES |
| **Source File** | `Fuel - Timing - HPFP - Valve Close Limit Minimum - 2017 - RogueWRX.csv` |

## Value

**225.0000 DEGREES**

## Description

This scalar defines the absolute minimum allowable HPFP valve close timing in crankshaft degrees. It prevents the valve from closing earlier than physically safe, protecting the pump from damage due to excessive pumping effort.

**Purpose:**
- Sets hard minimum limit on valve close timing
- Prevents over-pressurization from excessively early closing
- Protects HPFP from mechanical damage

**Value Interpretation:**
- Value of 225° represents the earliest the valve can close
- Earlier closing (lower values) = more pumping = higher pressure potential
- This limit ensures pumping stroke doesn't exceed safe limits

**Protection Function:**
The HPFP has physical limits on pumping capacity. Closing the valve too early:
- Extends effective pumping stroke beyond safe limits
- Creates excessive pressure in pump chamber
- Can damage pump components

## Related Tables

- **[Fuel - Timing - HPFP - Valve Close Base](./fuel-timing-hpfp-valve-close-base.md)**: Base close timing
- **[Fuel - Timing - HPFP - Valve Close Limit (IPW)](./fuel-timing-hpfp-valve-close-limit-ipw.md)**: IPW-based close limits
- **[Fuel - Timing - HPFP - Valve Close Limit Offset](./fuel-timing-hpfp-valve-close-limit-offset.md)**: Close limit offset

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Resulting pressure
- **HPFP Duty Cycle (%)**: Pump control effort
- **RPM**: Operating speed

## Tuning Notes

**Stock Behavior:** Stock minimum of 225° provides safe pump operation limit.

**Common Modifications:**
- **Do not lower significantly**: Risk of pump damage
- Only adjust if HPFP hardware capable of longer stroke
- Stock value appropriate for OEM pump

**When Minimum is Applied:**
If any close timing calculation results in value below 225°, this minimum is enforced instead. This protects pump during maximum fuel demand conditions.

**Warning:** Lowering this value beyond pump capability can cause catastrophic HPFP failure.

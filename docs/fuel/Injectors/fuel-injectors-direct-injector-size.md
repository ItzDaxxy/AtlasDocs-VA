# Fuel - Injectors - Direct Injector Size

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Fuel - Injectors - Direct Injector Size - 2017 - RogueWRX.csv` |

## Value

**2918.0000 NONE**

## Description

This scalar defines the flow rate of the direct fuel injectors in cc/min at a reference pressure. The ECU uses this value as the fundamental basis for calculating injector pulse width to deliver the required fuel quantity.

**Purpose:**
- Tells the ECU the fuel delivery capacity of installed injectors
- Required for accurate fuel calculation: Pulse Width = (Required Fuel Mass) / (Injector Flow Rate)
- Must be updated when injectors are upgraded to larger sizes

**Value Interpretation:**
- Stock FA20 DIT injectors: ~420 cc/min (stock value ~2918 represents internal ECU units)
- Value is measured at a specific reference pressure (typically 3,000 kPa / 43.5 psi)
- Actual flow varies with fuel pressure: Flow ∝ √(Pressure)

**Critical Note:**
This is one of the most important parameters to update when upgrading injectors. Incorrect values will cause the ECU to calculate wrong pulse widths, resulting in drastically incorrect air-fuel ratios.

## Related Tables

- **[Fuel - Injectors - Pulse Injector Mult Table](./fuel-injectors-pulse-injector-mult-table.md)**: Multiplier applied to base pulse width calculation
- **[Fuel - Injectors - Pulse Injector Offset Table](./fuel-injectors-pulse-injector-offset-table.md)**: Dead time/offset compensation
- **[Fuel - Injectors - Cylinder 1-4 Scalar Tables](./fuel-injectors-pulse-cylinder-1-scalar-table.md)**: Per-cylinder flow corrections
- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Fuel pressure affects actual flow rate
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Target AFR that drives fuel quantity calculation

## Related Datalog Parameters

- **Injector Pulse Width (ms)**: Resulting pulse width - verify reasonable values for load
- **Injector Duty Cycle (%)**: Percentage of available injection window used
- **AF Correction STFT (%)**: Large corrections indicate incorrect injector size
- **AF Learn 1 (%)**: Persistent trim also indicates sizing issue
- **A/F Sensor 1 (λ)**: Actual measured AFR to verify fuel delivery accuracy

## Tuning Notes

**Stock Behavior:** Stock value represents the flow rate of OEM direct injectors (~420 cc/min). This value is calibrated from factory and rarely needs adjustment unless injectors are replaced.

**Common Modifications:**
- **Injector Upgrade**: When installing larger injectors (e.g., 550cc, 750cc, 1000cc), this value MUST be updated proportionally
- **E85 Capability**: E85 requires ~30% more fuel volume, often necessitating larger injectors
- **High Power Builds**: Builds exceeding ~350-400 WHP typically require injector upgrades

**Calculation Example:**
- Stock injectors: 420 cc/min, stock scalar: 2918
- New injectors: 550 cc/min
- New scalar: 2918 × (550/420) = 3821 (approximate - actual scaling may differ)

**Recommended Approach:**
1. Obtain injector flow data from manufacturer at specific reference pressure
2. Calculate new value using ratio: New = Stock × (New Flow / Stock Flow)
3. Flash and verify with wideband - AFR should be close to target
4. Fine-tune with short-term fuel trim - should center around 0%

**Validation:** After changing this value, STFT should be within ±5% at steady state cruise. Large persistent trims indicate the value needs adjustment.

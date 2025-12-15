# Fuel - Power Enrichment - DAM Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Power Enrichment - DAM Activation - 2017 - RogueWRX.csv` |

## Description

This table defines how the Dynamic Advance Multiplier (DAM) influences power enrichment activation. The DAM value (0.0-1.0) reflects the ECU's confidence in current knock control - lower DAM indicates knock events have reduced timing safety margin.

**Purpose:**
- Links knock control strategy to fuel enrichment
- When DAM drops (indicating knock activity), this table can trigger earlier/more aggressive enrichment
- Provides additional protection by enriching fuel when knock margin is reduced

**Value Interpretation:**
- X-axis is DAM value from 0.0 (maximum knock activity) to 1.0 (no knock history)
- Output values influence enrichment threshold or activation
- Lower DAM values typically map to earlier enrichment activation

**Operating Logic:**
When the ECU detects knock and reduces DAM, the fuel system can respond by lowering the enrichment threshold, providing more fuel as an additional safety measure since timing has already been reduced.

## Axes

### X-Axis

- **Parameter**: Ignition - Dynamic Advance - DAM
- **Unit**: NONE
- **Range**: 0.0000 to 1.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |     0.1250 |     0.1875 |     0.2500 |     0.3125 |     0.3750 |     0.4375 |     0.5000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs linear interpolation on this 1D table using:
- **X-Axis (DAM)**: Current Dynamic Advance Multiplier value (0.0-1.0)

**Interpolation Process:**
1. ECU reads current DAM value from knock control system
2. Looks up corresponding output value from this table
3. Output value modifies enrichment activation thresholds
4. As DAM decreases, enrichment activates at lower load/earlier conditions

**Update Rate:** Evaluated continuously, but DAM itself changes slowly (incremental recovery from knock events).

**Interaction:** This table works alongside load-based and catalyst-temp-based enrichment triggers to provide multi-factor protection.

## Related Tables

- **[Fuel - Power Enrichment - Target](./fuel-power-enrichment-target.md)**: Lambda targets used when enrichment activates
- **[Fuel - Power Enrichment - Hysteresis Enriching](./fuel-power-enrichment-hysteresis-enriching.md)**: Load threshold for enrichment entry
- **[Ignition - Dynamic Advance tables](../ignition/)**: Source of DAM value that drives this table
- **[Fuel - Closed Loop - Command Fuel L](./fuel-closed-loop-command-fuel-l.md)**: Normal targets overridden by enrichment

## Related Datalog Parameters

- **Dynamic Advance Multiplier (DAM)**: The X-axis input - monitor correlation with enrichment behavior
- **Feedback Knock**: Shows recent knock events that drive DAM down
- **Fine Knock Learn**: Persistent knock correction values
- **Fuel Mode**: Verify enrichment activates when expected based on DAM
- **Command Fuel Final (λ)**: Confirm enrichment targets being applied

## Tuning Notes

**Stock Behavior:** Stock calibration links DAM reduction to more conservative (earlier) enrichment activation, providing layered protection when knock is occurring.

**Common Modifications:**
- **Performance Tuning**: Some tuners reduce the DAM-enrichment link to maintain leaner AFR longer, but this removes a safety layer
- **Conservative Approach**: Maintaining or strengthening the DAM link adds fuel when knock is present, reducing risk

**Recommended Approach:**
1. Leave at stock unless you have specific reason to modify
2. If experiencing knock at WOT, ensure this table is providing enrichment protection
3. Log DAM alongside fuel mode to understand interaction

**Validation:** During WOT pulls where DAM drops, verify enrichment activates appropriately. If DAM drops but AFR stays lean, investigate this table.

## Warnings

⚠️ **Knock Protection**: This table provides a safety layer linking knock detection to fuel enrichment. Removing or weakening this link can result in continued lean operation during knock events, potentially causing engine damage.

⚠️ **DAM as Indicator**: If DAM is consistently low, the root cause (knock) should be addressed rather than modifying enrichment tables. Low DAM indicates the engine is experiencing detonation.

**Safe Practices:**
- Do not eliminate DAM-enrichment link without addressing underlying knock
- If DAM regularly drops below 0.75, investigate and resolve knock issues
- Maintain conservative enrichment activation when DAM is low

**Signs of Problems:**
- DAM dropping without enrichment activation: Table may be misconfigured
- Knock activity with lean AFR: DAM link may be too weak
- Consistently low DAM: Root cause knock issue needs resolution

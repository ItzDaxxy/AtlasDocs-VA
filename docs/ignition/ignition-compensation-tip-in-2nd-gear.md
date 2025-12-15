# Ignition - Compensation - Tip-In - 2nd Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 2nd Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in events in 2nd gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid acceleration in 2nd gear.

**Purpose:**
- Compensates timing during rapid throttle opening in 2nd gear
- Typically retards timing to prevent knock during boost build
- Gear-specific calibration for different torque characteristics
- 2nd gear has less torque multiplication than 1st but still significant

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive = advance, Negative = retard
- Higher TPS delta = faster throttle movement
- Compensation active during transient throttle events

## Axes

### X-Axis

- **Parameter**: Timing - Compensation - Tip-In - TPS Delta Raw
- **Unit**: Raw counts (0-28672 scale)
- **Range**: 0.0000 to 28672.0000
- **Points**: 8

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |  4096.0000 |  8192.0000 | 12288.0000 | 16384.0000 | 20480.0000 | 24576.0000 | 28672.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (TPS Delta)**: Rate of throttle position change

**2nd Gear Context:**
Second gear is commonly used for acceleration from low speeds. Tip-in compensation here affects common driving scenarios like pulling away from traffic.

**Gear-Specific Compensation:**
Each gear has its own tip-in table because:
- Torque multiplication varies by gear
- Load increase rate differs
- RPM range during tip-in varies

**Update Rate:** Calculated every ignition event during tip-in.

## Related Tables

- **[Ignition - Compensation - Tip-In - 1st Gear](./ignition-compensation-tip-in-1st-gear.md)**: 1st gear tip-in
- **[Ignition - Compensation - Tip-In - 3rd Gear](./ignition-compensation-tip-in-3rd-gear.md)**: 3rd gear tip-in

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines table selection
- **Ignition Timing**: Final timing with compensation

## Tuning Notes

**Stock Behavior:** Stock provides appropriate tip-in compensation for 2nd gear acceleration scenarios.

**Common Modifications:**
- Usually left at stock unless specific tip-in issues
- May adjust if experiencing knock during 2nd gear acceleration
- Consider intercooler efficiency if heat soak causes issues

## Warnings

⚠️ **Transient Knock Risk**: Tip-in is knock-prone. Test carefully.

⚠️ **Gear-Specific**: Only affects 2nd gear operation.

**Safe Practices:**
- Test tip-in response at various temperatures
- Monitor knock during aggressive acceleration
- Test specifically in 2nd gear scenarios

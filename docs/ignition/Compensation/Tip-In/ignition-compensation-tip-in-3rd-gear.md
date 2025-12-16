# Ignition - Compensation - Tip-In - 3rd Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 3rd Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in events in 3rd gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid acceleration in 3rd gear.

**Purpose:**
- Compensates timing during rapid throttle opening in 3rd gear
- Typically retards timing to prevent knock during boost build
- Gear-specific calibration for mid-range acceleration
- 3rd gear is commonly used for highway merging and passing

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive = advance, Negative = retard
- Higher TPS delta = faster throttle movement
- Compensation active during transient throttle events

**3rd Gear Context:**
Third gear provides a balance between torque multiplication and speed. It's frequently used for highway on-ramps and overtaking maneuvers where tip-in knock protection is important.

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

**3rd Gear Context:**
Third gear is frequently used for highway merging and passing maneuvers. Tip-in compensation helps prevent knock during the rapid boost build that occurs in these scenarios.

**Gear-Specific Compensation:**
Each gear has its own tip-in table because:
- Torque multiplication varies by gear
- Load increase rate differs
- RPM range during tip-in varies
- 3rd gear has moderate torque with higher speed capability

**Update Rate:** Calculated every ignition event during tip-in.

## Related Tables

- **[Ignition - Compensation - Tip-In - 1st Gear](./ignition-compensation-tip-in-1st-gear.md)**: 1st gear tip-in
- **[Ignition - Compensation - Tip-In - 2nd Gear](./ignition-compensation-tip-in-2nd-gear.md)**: 2nd gear tip-in
- **[Ignition - Compensation - Tip-In - 4th Gear](./ignition-compensation-tip-in-4th-gear.md)**: 4th gear tip-in
- **[Ignition - Compensation - Tip-In - 5th Gear](./ignition-compensation-tip-in-5th-gear.md)**: 5th gear tip-in
- **[Ignition - Compensation - Tip-In - 6th Gear](./ignition-compensation-tip-in-6th-gear.md)**: 6th gear tip-in

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines table selection
- **Ignition Timing**: Final timing with compensation
- **Vehicle Speed**: Used for gear calculation

## Tuning Notes

**Stock Behavior:** Stock provides appropriate tip-in compensation for 3rd gear acceleration scenarios, typically used for highway merging and passing.

**3rd Gear Characteristics:**
- Moderate torque multiplication
- Common for highway acceleration
- Frequently used for passing maneuvers
- Balance between low-gear torque and high-gear speed

**Common Modifications:**
- Usually left at stock unless specific tip-in issues
- May adjust if experiencing knock during 3rd gear acceleration
- Consider if heat soak causes issues during repeated passing maneuvers

**Testing Tip-In:**
To verify proper tip-in compensation:
- Datalog while accelerating in 3rd gear
- Test highway on-ramp scenarios
- Monitor knock and timing values
- Verify compensation across different RPM ranges

## Warnings

**Transient Knock Risk**: Tip-in is knock-prone. Test carefully.

**Gear-Specific**: Only affects 3rd gear operation.

**Safe Practices:**
- Test tip-in response at various temperatures
- Monitor knock during aggressive acceleration
- Test specifically in 3rd gear scenarios
- Pay attention to highway merging and passing situations

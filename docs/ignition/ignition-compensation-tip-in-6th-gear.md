# Ignition - Compensation - Tip-In - 6th Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 6th Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in events in 6th gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid acceleration in 6th gear.

**Purpose:**
- Compensates timing during rapid throttle opening in 6th gear
- Typically retards timing to prevent knock during boost build
- Gear-specific calibration for maximum overdrive cruising
- 6th gear is used exclusively for highway cruising and fuel economy

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive = advance, Negative = retard
- Higher TPS delta = faster throttle movement
- Compensation active during transient throttle events

**6th Gear Context:**
Sixth gear is the tallest overdrive gear, designed for maximum fuel economy at highway speeds. Tip-in events are extremely rare in 6th gear as it's unsuitable for acceleration. Most drivers downshift before accelerating.

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

**6th Gear Context:**
Sixth gear is the tallest gear, used exclusively for highway fuel economy cruising. Tip-in events in 6th gear are virtually non-existent as the gear is too tall for meaningful acceleration. Drivers typically downshift to 5th or lower before accelerating.

**Gear-Specific Compensation:**
Each gear has its own tip-in table because:
- Torque multiplication varies by gear
- Load increase rate differs
- RPM range during tip-in varies
- 6th gear has the lowest torque multiplication (tallest overdrive)

**Practical Note:** This table may have minimal practical impact since tip-in acceleration in 6th gear is rare in real-world driving.

**Update Rate:** Calculated every ignition event during tip-in.

## Related Tables

- **[Ignition - Compensation - Tip-In - 1st Gear](./ignition-compensation-tip-in-1st-gear.md)**: 1st gear tip-in
- **[Ignition - Compensation - Tip-In - 2nd Gear](./ignition-compensation-tip-in-2nd-gear.md)**: 2nd gear tip-in
- **[Ignition - Compensation - Tip-In - 3rd Gear](./ignition-compensation-tip-in-3rd-gear.md)**: 3rd gear tip-in
- **[Ignition - Compensation - Tip-In - 4th Gear](./ignition-compensation-tip-in-4th-gear.md)**: 4th gear tip-in
- **[Ignition - Compensation - Tip-In - 5th Gear](./ignition-compensation-tip-in-5th-gear.md)**: 5th gear tip-in

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines table selection
- **Ignition Timing**: Final timing with compensation
- **Vehicle Speed**: Used for gear calculation

## Tuning Notes

**Stock Behavior:** Stock provides tip-in compensation for completeness, but 6th gear tip-in scenarios are extremely rare in practical driving.

**6th Gear Characteristics:**
- Lowest torque multiplication (tallest overdrive)
- Used exclusively for highway fuel economy cruising
- Unsuitable for acceleration
- Tip-in events virtually never occur
- Drivers downshift before accelerating

**Common Modifications:**
- Usually ignored - rarely if ever active
- No practical need for adjustment
- Table exists for ECU architecture completeness

**Practical Reality:**
In real-world driving, this table is almost never used because:
- 6th gear is too tall for meaningful acceleration
- Any attempt to accelerate in 6th causes immediate downshift
- Manual transmission drivers always downshift before accelerating
- CVT-style logic would downshift automatically

## Warnings

**Transient Knock Risk**: Tip-in is knock-prone. Test carefully.

**Gear-Specific**: Only affects 6th gear operation.

**Practical Irrelevance**: This table has minimal real-world impact due to the impracticality of accelerating in 6th gear.

**Safe Practices:**
- Understand this table is rarely active in normal driving
- 6th gear is for cruising, not acceleration
- Downshift before accelerating for safety and performance
- Testing this table requires unusual driving conditions

# Ignition - Compensation - Tip-In - 5th Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 5th Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in events in 5th gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid acceleration in 5th gear.

**Purpose:**
- Compensates timing during rapid throttle opening in 5th gear
- Typically retards timing to prevent knock during boost build
- Gear-specific calibration for high-speed cruising
- 5th gear is commonly used for highway cruising and high-speed passing

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive = advance, Negative = retard
- Higher TPS delta = faster throttle movement
- Compensation active during transient throttle events

**5th Gear Context:**
Fifth gear is a tall overdrive gear primarily used for highway cruising. Tip-in events are relatively rare but may occur during high-speed passing. Low torque multiplication means boost builds more slowly.

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

**5th Gear Context:**
Fifth gear is used for high-speed cruising (70+ mph). Tip-in events in 5th gear are uncommon but may occur during highway passing at high speeds. The tall gearing means boost builds more gradually.

**Gear-Specific Compensation:**
Each gear has its own tip-in table because:
- Torque multiplication varies by gear
- Load increase rate differs
- RPM range during tip-in varies
- 5th gear has minimal torque multiplication (overdrive ratio)

**Update Rate:** Calculated every ignition event during tip-in.

## Related Tables

- **[Ignition - Compensation - Tip-In - 1st Gear](./ignition-compensation-tip-in-1st-gear.md)**: 1st gear tip-in
- **[Ignition - Compensation - Tip-In - 2nd Gear](./ignition-compensation-tip-in-2nd-gear.md)**: 2nd gear tip-in
- **[Ignition - Compensation - Tip-In - 3rd Gear](./ignition-compensation-tip-in-3rd-gear.md)**: 3rd gear tip-in
- **[Ignition - Compensation - Tip-In - 4th Gear](./ignition-compensation-tip-in-4th-gear.md)**: 4th gear tip-in
- **[Ignition - Compensation - Tip-In - 6th Gear](./ignition-compensation-tip-in-6th-gear.md)**: 6th gear tip-in

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines table selection
- **Ignition Timing**: Final timing with compensation
- **Vehicle Speed**: Used for gear calculation

## Tuning Notes

**Stock Behavior:** Stock provides appropriate tip-in compensation for 5th gear, though tip-in events are relatively uncommon in this tall gear used primarily for highway cruising.

**5th Gear Characteristics:**
- Very low torque multiplication (overdrive)
- Used for highway cruising at 70+ mph
- Tip-in events are rare
- Boost builds slowly due to tall gearing
- Less knock risk than lower gears during tip-in

**Common Modifications:**
- Usually left at stock
- Rarely requires adjustment due to infrequent use
- May be irrelevant if aggressive driving doesn't occur in 5th gear

**Testing Tip-In:**
To verify proper tip-in compensation:
- Datalog during high-speed highway passing (where legal)
- Monitor knock and timing values
- Test at 70+ mph cruise speeds
- Note that tip-in in 5th is typically gentler than lower gears

## Warnings

**Transient Knock Risk**: Tip-in is knock-prone. Test carefully.

**Gear-Specific**: Only affects 5th gear operation.

**Safe Practices:**
- Test tip-in response at various temperatures
- Monitor knock during any 5th gear acceleration
- Understand that 5th gear tip-in is uncommon in normal driving
- Exercise caution with high-speed testing
